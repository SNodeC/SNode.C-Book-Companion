"""A listener failure belongs to endpoint setup; the existing owner still echoes."""
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab_support import connect, free_port, receive, running

port = free_port()
args = ['--log-level=5', 'echoserver', 'local', '--host=127.0.0.1', f'--port={port}']
with running(sys.argv[1], args) as (first, _):
    with connect(port, first) as peer:
        with running(sys.argv[1], args) as (second, log):
            deadline = time.monotonic() + 5
            while 'Address already in use' not in log.read_text():
                if time.monotonic() > deadline:
                    raise TimeoutError('Second listener did not report the occupied endpoint')
                time.sleep(0.02)
            peer.sendall(b'original owner')
            assert receive(peer, 14) == b'original owner'
print('PASS: second listener reports occupied endpoint; original owner still reflects bytes')
