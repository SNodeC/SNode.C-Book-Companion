"""Observe HTTP admission and Express dispatch using a single public fixture."""
from pathlib import Path
import http.client
import socket
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab_support import connect, free_port, running


def response(peer):
    reply = http.client.HTTPResponse(peer)
    reply.begin()
    return reply.status, dict(reply.getheaders()), reply.read()


def exchange(port, process, data):
    with connect(port, process) as peer:
        peer.sendall(data)
        return response(peer)


def run(mode, binary):
    port = free_port()
    args = ['lab', 'local', '--host=127.0.0.1', f'--port={port}']
    if mode == 'limits':
        args += ['http', 'parser', '--maximum-header-line-bytes=40']
    with running(binary, args) as (process, log):
        with connect(port, process):
            pass
        request = b'GET /api/status HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n'
        if mode == 'framing':
            with connect(port, process) as peer:
                peer.sendall(request)
                peer.settimeout(.2)
                try:
                    data = peer.recv(1)
                    raise AssertionError(f'Response before complete headers: {data!r}')
                except socket.timeout:
                    pass
                assert 'APP ' not in log.read_text()
                peer.settimeout(5)
                peer.sendall(b'\r\n')
                status, _, body = response(peer)
                assert status == 200 and body == b'app-before,router-before,handler'
            assert log.read_text().count('HANDLER') == 1
            print('PASS: incomplete headers produce no handler/response; completing headers produces one 200')
        elif mode == 'limits':
            status, _, _ = exchange(port, process, request + b'\r\n')
            assert status == 200
            for data in [b'not-http\r\n\r\n', request + b'X-Large: ' + b'x' * 50 + b'\r\n\r\n']:
                status, _, _ = exchange(port, process, data)
                assert 400 <= status < 500, status
                print(f'PASS: rejected input returns {status}')
            assert log.read_text().count('APP ') == 1
            print('PASS: only valid request entered application dispatch')
        elif mode == 'order':
            status, headers, body = exchange(port, process, request + b'\r\n')
            assert status == 200 and body == b'app-before,router-before,handler'
            assert headers.get('X-Trace') == body.decode(), headers
            assert exchange(port, process, request.replace(b'/api/status', b'/outside') + b'\r\n')[0] == 404
            output = log.read_text()
            assert output.count('APP ') == 2 and output.count('ROUTER') == output.count('HANDLER') == 1, output
            print('PASS: mounted route visits app,router,handler; outside path visits only app and returns 404')
        else:
            status, headers, body = exchange(port, process, request.replace(b'/api/status', b'/blocked') + b'\r\n')
            assert status == 403 and body == b'middleware stopped request'
            assert headers.get('X-Trace') == 'app-before,stop', headers
            output = log.read_text()
            assert output.count('STOP') == 1 and 'HANDLER' not in output, output
            print('PASS: middleware returns 403 and ends dispatch; following handler never runs')


if __name__ == '__main__':
    run(*sys.argv[1:])
