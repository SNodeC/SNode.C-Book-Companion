"""One idle or closed connection must not stop another peer's byte reflection."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab_support import connect, free_port, receive, running

for binary, kind in zip(sys.argv[1:], ('snodec', 'asio')):
    port = free_port()
    args = ([str(port)] if kind == 'asio' else
            ['echoserver', 'local', '--host=127.0.0.1', f'--port={port}'])
    with running(binary, args) as (process, _):
        with connect(port, process) as active:
            with connect(port, process):  # Keep a second peer idle.
                active.sendall(b'other\x00peer')
                assert receive(active, 10) == b'other\x00peer'
            active.sendall(b'still here')
            assert receive(active, 10) == b'still here'
    print(f'PASS: {kind}: active peer works while another is idle and after it closes')
