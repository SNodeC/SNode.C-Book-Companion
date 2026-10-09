"""Controlled peers distinguish failed activation retry from post-connection recovery."""
from pathlib import Path
import json
import socket
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab_support import receive, running
from ch15.tls import policy


def records(path):
    text = path.read_text()
    complete = text[:text.rfind('\n') + 1]
    return [json.loads(line) for line in complete.splitlines() if line.startswith('{')]


def wait_for(process, path, predicate):
    deadline = time.monotonic() + 8
    while time.monotonic() < deadline:
        rows = records(path)
        if predicate(rows):
            return rows
        if process.poll() is not None:
            raise RuntimeError('Client exited before expected observation')
        time.sleep(.03)
    raise TimeoutError('Client observation timed out')


def arguments(port, reconnect=False):
    return ['--log-level=6', '--log-format=json', 'echoclient', 'remote',
            '--host=127.0.0.1', f'--port={port}', 'socket', '--retry=true',
            '--retry-timeout=.2', '--retry-base=1', '--retry-jitter=0',
            f'--retry-tries={20 if reconnect else 1}',
            f'--reconnect={str(reconnect).lower()}', '--reconnect-time=.2']


def failed(rows):
    return [r for r in rows if r.get('component') == 'echo' and r.get('level') == 'error']


def attached(rows):
    return [r for r in rows if r.get('message') == 'Echo context attached']


def retry(client):
    # Bind without listen: reserve the endpoint while causing connection refusal.
    with socket.socket() as reserved:
        reserved.bind(('127.0.0.1', 0))
        with running(client, arguments(reserved.getsockname()[1])) as (process, log):
            process.wait(timeout=8)
            rows = records(log)
            assert len(failed(rows)) == 2, rows
            assert not attached(rows), rows
            print('PASS: initial attempt plus one retry; two error statuses; no context attachment; natural exit')
            for row in failed(rows):
                print(json.dumps(row))


def checkpoint(client, tls_client):
    policy(tls_client, 'openssl')
    with socket.socket() as reserved:
        reserved.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        reserved.bind(('127.0.0.1', 0))
        port = reserved.getsockname()[1]
        with running(client, arguments(port, True)) as (process, log):
            first = wait_for(process, log, lambda rows: len(failed(rows)) >= 1)
            assert not attached(first)
            reserved.listen(1)
            reserved.settimeout(8)
            greeting = b'Hello peer! Nice to see you!!!'
            with reserved.accept()[0] as peer:
                peer.settimeout(5)
                assert receive(peer, len(greeting)) == greeting
                established = wait_for(process, log, lambda rows: len(attached(rows)) == 1)
            # Stop the listener as well as the established peer, then observe a failed
            # new activation before restarting. This avoids inferring recovery from timers.
            reserved.close()
            failed_before = len(failed(established))
            wait_for(process, log, lambda rows: len(failed(rows)) > failed_before)
            with socket.socket() as restarted:
                restarted.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                restarted.bind(('127.0.0.1', port))
                restarted.listen(1)
                restarted.settimeout(8)
                with restarted.accept()[0] as peer:
                    peer.settimeout(5)
                    assert receive(peer, len(greeting)) == greeting
                    peer.sendall(b'recovered')
                    assert receive(peer, 9) == b'recovered'
                    rows = wait_for(process, log, lambda rows: len(attached(rows)) == 2)
                    assert any(r.get('message') == 'Echo context detached: connection close' for r in rows), rows
                    identities = [r.get('connection') for r in attached(rows)]
                    assert all(identities) and len(set(identities)) == 2, attached(rows)
                    print('PASS: retry before first attachment; peer stop/restart; two connection identities; fresh greeting and exact echo')
                    for row in rows:
                        if row in failed(rows) or row in attached(rows) or 'detached' in row.get('message', ''):
                            print(json.dumps(row))


if __name__ == '__main__':
    {'retry': retry, 'checkpoint': checkpoint}[sys.argv[1]](*sys.argv[2:])
