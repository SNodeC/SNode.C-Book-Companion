"""Observe the changed greeting in a real pair, then check bytes with a controlled peer."""
import socket
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab_support import connect, free_port, receive, running

server, client = sys.argv[1:]
port = free_port()
with running(server, ['--log-level=5', 'echoserver', 'local', '--host=127.0.0.1', f'--port={port}']) as (process, log):
    with connect(port, process):
        pass
    with running(client, ['greeting-client', 'remote', '--host=127.0.0.1', f'--port={port}']):
        deadline = time.monotonic() + 5
        while b'Learning by echo' not in log.read_bytes():
            if time.monotonic() > deadline:
                raise TimeoutError('EchoPair did not observe the changed greeting')
            time.sleep(0.02)
    with connect(port, process) as active, connect(port, process) as idle:
        payload = b'sensor-a,21.5\nsensor-a,not-a-number\n'
        active.sendall(payload)
        assert receive(active, len(payload)) == payload
        idle.sendall(b'sensor-b,18.0\n')
        assert receive(idle, len(b'sensor-b,18.0\n')) == b'sensor-b,18.0\n'
        idle.close()
        active.sendall(payload)
        assert receive(active, len(payload)) == payload
print('PASS: EchoPair receives Learning by echo')
print('PASS: independent measurement peers reflect even invalid values; closing one leaves the other usable')

with socket.socket() as listener:
    listener.bind(('127.0.0.1', 0))
    listener.listen(1)
    listener.settimeout(8)
    port = listener.getsockname()[1]
    with running(client, ['greeting-client', 'remote', '--host=127.0.0.1', f'--port={port}']):
        peer, _ = listener.accept()
        with peer:
            peer.settimeout(5)
            assert receive(peer, len(b'Learning by echo')) == b'Learning by echo'
            payload = b'a\x00b\xff\n' * 1000
            peer.sendall(payload)
            assert receive(peer, len(payload)) == payload
print('PASS: changed greeting and unchanged binary reflection with a controlled peer')
