"""Compare stream bytes, not message boundaries or speed."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab_support import connect, free_port, receive, running

payload = bytes(range(256)) * 80  # 20,480 bytes, including NULs.
for binary, kind in zip(sys.argv[1:], ('snodec', 'asio')):
    port = free_port()
    args = ([str(port)] if kind == 'asio' else
            ['echoserver', 'local', '--host=127.0.0.1', f'--port={port}'])
    with running(binary, args) as (process, _):
        with connect(port, process) as peer:
            peer.sendall(payload[:17])
            assert receive(peer, 17) == payload[:17]
            peer.sendall(payload[17:])
            assert receive(peer, len(payload) - 17) == payload[17:]
        # EOF of one session must not prevent a later connection.
        with connect(port, process) as peer:
            peer.sendall(b'again')
            assert receive(peer, 5) == b'again'
    print(f'PASS: {kind}: 20480 binary bytes unchanged; next connection also works')
