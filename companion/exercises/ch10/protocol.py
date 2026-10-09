"""Observe canonical LineProtocol at the peer boundary, independently of send segmentation."""
import contextlib
from pathlib import Path
import select
import socket
import sys
import tempfile
import time
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab_support import connect, free_port, receive, running

@contextlib.contextmanager
def server(binary, family):
    with tempfile.TemporaryDirectory(prefix='line-lab-') as temp:
        if family == 'ip':
            endpoint = free_port()
            args = ['lineprotocolserver', 'local', '--host=127.0.0.1', f'--port={endpoint}']
        else:
            endpoint = str(Path(temp) / 'line.sock')
            args = ['lineprotocolserver', 'local', f'--sun-path={endpoint}']
        with running(binary, args) as (process, log):
            def open_peer():
                if family == 'ip':
                    return connect(endpoint, process)
                deadline = time.monotonic() + 8
                while True:
                    peer = socket.socket(socket.AF_UNIX)
                    peer.settimeout(3)
                    try:
                        peer.connect(endpoint)
                        return peer
                    except (FileNotFoundError, ConnectionRefusedError):
                        peer.close()
                        if process.poll() is not None or time.monotonic() > deadline:
                            raise RuntimeError('Unix listener did not become ready')
                        time.sleep(0.03)
            yield open_peer, endpoint
        if family == 'unix':
            assert not Path(endpoint).exists(), 'Server socket path survived shutdown'

def ready(open_peer):
    peer = open_peer()
    try:
        assert receive(peer, 6) == b'READY\n'
    except BaseException:
        peer.close()
        raise
    return peer

def quiet(peer):
    assert not select.select([peer], [], [], 0.1)[0], 'Response before a complete command'

def conversation(open_peer):
    expected = b'PONG\nOK\nERR unknown command\nPONG\n'
    command = b'PING\nSTATUS\nBOGUS\n\nPING\r\n'
    observed = []
    # Every two-piece split plus a coalesced input, on fresh contexts.
    for split in range(len(command) + 1):
        with ready(open_peer) as peer:
            peer.sendall(command[:split])
            peer.sendall(command[split:])
            reply = receive(peer, len(expected))
            assert reply == expected
            observed.append(reply)
            peer.sendall(b'QUIT\n')
            assert peer.recv(1) == b''
    with ready(open_peer) as peer:
        peer.sendall(b'PI')
        quiet(peer)
        peer.sendall(b'NG\nSTATUS\n')
        assert receive(peer, 8) == b'PONG\nOK\n'
    with ready(open_peer) as peer:
        peer.sendall(b'QUIT\nPING\n')
        assert peer.recv(1) == b'', 'Reply after coalesced QUIT; PONG must not be sent'
    print(f'PASS: {len(observed)} segmentations, CRLF/empty/unknown commands, QUIT, partial-prefix silence')
    return observed

def limits(open_peer):
    for payload in [b'x'*4096+b'\n', b'x'*4095+b'\r\n']:
        with ready(open_peer) as peer:
            peer.sendall(payload)
            assert receive(peer, 20) == b'ERR unknown command\n'
            peer.sendall(b'PING\n')
            assert receive(peer, 5) == b'PONG\n'
    for suffix in [b'x', b'x\n']:
        with ready(open_peer) as peer:
            peer.sendall(b'x'*4096)
            quiet(peer)
            peer.sendall(suffix)
            diagnostic = bytearray()
            while part := peer.recv(64):
                diagnostic.extend(part)
                assert b'ERR line too long\n'.startswith(diagnostic)
            # Immediate close need not flush the queued diagnostic; EOF is required.
            print(f'Overlong input: closed; diagnostic bytes delivered={len(diagnostic)}')
    print('PASS: 4096 bytes accepted including optional CR; 4097 closes with or without delimiter')

def isolation(open_peer):
    with ready(open_peer) as first, ready(open_peer) as second:
        first.sendall(b'PI'); quiet(first)
        second.sendall(b'STATUS\n'); assert receive(second, 3) == b'OK\n'
        first.close()  # Abandon an incomplete line, then create a new context.
        with ready(open_peer) as replacement:
            replacement.sendall(b'NG\n'); assert receive(replacement, 20) == b'ERR unknown command\n'
            replacement.sendall(b'PING\n'); assert receive(replacement, 5) == b'PONG\n'
        second.sendall(b'PING\n'); assert receive(second, 5) == b'PONG\n'
    print('PASS: independent pending buffers; replacement starts fresh; surviving peer progresses')

mode, binary = sys.argv[1:3]
if mode == 'transfer':
    outputs=[]
    for family, executable in [('ip', binary), ('unix', sys.argv[3])]:
        with server(executable, family) as (open_peer, endpoint):
            outputs.append(conversation(open_peer)); print(f'Observed {family}: {endpoint}')
    assert outputs[0] == outputs[1]
    print('PASS: Part IV checkpoint: identical reconstructed replies over IPv4 and Unix; owned cleanup')
else:
    with server(binary, 'unix' if mode == 'endpoint-failure' else 'ip') as (open_peer, endpoint):
        if mode in ('framing', 'limits', 'isolation'):
            {'framing': conversation, 'limits': limits, 'isolation': isolation}[mode](open_peer)
        elif mode == 'refusal':
            with open_peer() as peer:
                assert peer.recv(1) == b'', 'Refused creation produced bytes instead of closure'
            with ready(open_peer) as peer:
                peer.sendall(b'PING\n'); assert receive(peer, 5) == b'PONG\n'
            print('PASS: null factory result closes before READY; later valid context replies')
        elif mode == 'endpoint-failure':
            with ready(open_peer) as peer:
                with socket.socket(socket.AF_UNIX) as wrong:
                    wrong.settimeout(3)
                    try: wrong.connect(endpoint + '.missing')
                    except FileNotFoundError: pass
                    else: raise AssertionError('Unexpected missing-path connection')
                peer.sendall(b'BOGUS\n'); assert receive(peer, 20) == b'ERR unknown command\n'
                peer.sendall(b'PING\n'); assert receive(peer, 5) == b'PONG\n'
            print('PASS: missing path fails before protocol; valid peer reports command error and remains usable')
        else:
            raise ValueError(mode)
