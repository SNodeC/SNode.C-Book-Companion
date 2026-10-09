"""Negotiation and the Part VII state/observer checkpoint, using canonical examples."""
from pathlib import Path
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab_support import connect, environment, free_port, running
from wire import echo_exchange


def run(mode, server, other):
    if mode == 'checkpoint':
        with tempfile.TemporaryDirectory() as config:
            subprocess.run([sys.executable, str(Path(__file__).resolve().parents[1] / 'ch19/observers.py'), other],
                           env=environment(config), check=True, timeout=35)
    port = free_port()
    with running(server, ['--log-level=6', 'legacy', 'local', '--host=127.0.0.1', f'--port={port}']) as (process, log):
        if mode == 'negotiation':
            with connect(port, process):
                pass
            with tempfile.TemporaryDirectory() as config:
                result = subprocess.run([other, '--log-level=6', 'legacy', 'remote', '--host=127.0.0.1', f'--port={port}'],
                                        env=environment(config), capture_output=True, text=True, timeout=10)
            assert result.returncode == 0, result.stdout + result.stderr
            assert 'WebSocket echo client received: hello' in result.stdout + result.stderr
            before = log.read_text().count('WebSocket echo server connected')
            with connect(port, process) as peer:
                peer.sendall((f'GET /ws HTTP/1.1\r\nHost: localhost:{port}\r\nUpgrade: websocket\r\n'
                              'Connection: Upgrade\r\nSec-WebSocket-Key: Ym9vay1lY2hvLXRlc3QhIQ==\r\n'
                              'Sec-WebSocket-Version: 13\r\nSec-WebSocket-Protocol: unavailable-lab-protocol\r\n\r\n').encode())
                response = bytearray()
                while b'\r\n\r\n' not in response:
                    chunk = peer.recv(1024)
                    assert chunk, response
                    response.extend(chunk)
                assert not response.startswith(b'HTTP/1.1 101'), response
                assert b'Sec-WebSocket-Protocol: echo' not in response
                print('PASS: unsupported subprotocol rejected:', bytes(response).split(b'\r\n')[0].decode())
            assert before == 1 and log.read_text().count('WebSocket echo server connected') == before
            print('PASS: canonical client negotiates echo, receives hello and closes; unsupported name never attaches echo')
        else:
            with connect(port, process) as peer:
                echo_exchange(peer)
            print('PASS: Part VII checkpoint: shared accepted SSE state survives one observer disconnect; separate WebSocket type/bytes/fragment/control/close checks pass')


if __name__ == '__main__':
    run(*sys.argv[1:])
