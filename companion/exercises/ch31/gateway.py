"""Independent peers for the canonical extended gateway; no second application model."""
from contextlib import contextmanager, ExitStack
import json
from pathlib import Path
import socket
import sys
import tempfile
import time
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab_support import connect, event, events, free_port, request, running


@contextmanager
def gateway(binary):
    with tempfile.TemporaryDirectory(prefix='gateway-lab-') as temp, socket.socket() as unavailable:
        unavailable.bind(('127.0.0.1', 0))  # Reserve a refused MQTT endpoint.
        path = Path(temp)/'input.sock'
        port = free_port()
        args = ['web', 'local', '--host=127.0.0.1', f'--port={port}',
                'measurement-input', 'local', f'--sun-path={path}',
                'mqtt-uplink', 'remote', '--host=127.0.0.1',
                f'--port={unavailable.getsockname()[1]}']
        with running(binary, args) as (process, _):
            with connect(port, process):
                pass
            def current(sequence=None):
                deadline = time.monotonic() + 5
                while True:
                    code, body = request(port, 'GET', '/status')
                    assert code == 200
                    measurement = json.loads(body)
                    if sequence is None or measurement['sequence'] == sequence:
                        return measurement
                    assert measurement['sequence'] < sequence, measurement
                    assert time.monotonic() < deadline, measurement
                    time.sleep(.02)
            def open_input():
                deadline = time.monotonic() + 5
                while True:
                    peer = socket.socket(socket.AF_UNIX)
                    peer.settimeout(5)
                    try:
                        peer.connect(str(path))
                        return peer
                    except (FileNotFoundError, ConnectionRefusedError):
                        peer.close()
                        assert process.poll() is None and time.monotonic() < deadline
                        time.sleep(.02)
            assert current()['sequence'] == 0
            assert request(port, 'GET', '/health')[0] == 200
            yield port, open_input, current
        assert not path.exists(), 'Owned Unix socket survived gateway shutdown'


def framing(binary):
    with gateway(binary) as (_, open_input, current):
        with open_input() as peer:
            line = b'21.5,43.0,3.72,9000\n'
            peer.sendall(line)
            first = current(1)
            assert first == {'temperature': 21.5, 'humidity': 43.0, 'voltage': 3.72, 'sequence': 1}
            peer.sendall(line[:8]); peer.sendall(line[8:])
            second = current(2)
            assert second == first | {'sequence': 2}
            invalid = [b'not-a-number,43,3.72', b'nan,43,3.72', b'21,43',
                       b'21,43,3.72,9junk', b'21,43,3.72,9,extra']
            # The following valid record is a barrier: all earlier records on this
            # stream must have been parsed without advancing the model.
            peer.sendall(b'\n'.join(invalid) + b'\n' + line)
            assert current(3) == first | {'sequence': 3}
            bounded = b'22,44,3.8' + b' ' * (4095 - len(b'22,44,3.8')) + b'\r'
            assert len(bounded) == 4096
            peer.sendall(bounded + b'\n')
            accepted = current(4)
            assert accepted['temperature'] == 22
        # An overlong line must close without treating its valid-looking suffix
        # as another record. Exercise coalesced and separated writes.
        for chunks in ([b'x' * 4097 + line], [b'x' * 4096, b'x', line]):
            with open_input() as peer:
                for chunk in chunks:
                    try:
                        peer.sendall(chunk)
                    except (BrokenPipeError, ConnectionResetError):
                        break
                try:
                    assert peer.recv(1) == b''
                except ConnectionResetError:
                    pass
            assert current() == accepted
        with open_input() as peer:
            peer.sendall(line)
            assert current(5) == first | {'sequence': 5}
    print('PASS: whole/fragmented records agree; malformed records do not advance order; producer 9000 becomes local order; 4096-byte CR record accepted; both overlong forms close without suffix acceptance')


def mixed(binary):
    with gateway(binary) as (port, open_input, current):
        with events(port) as survivor, ExitStack() as old_observer, open_input() as peer:
            first = old_observer.enter_context(events(port))
            code, body = request(port, 'POST', '/simulate')
            accepted = json.loads(body)
            assert code == 200 and accepted['sequence'] == 1
            assert event(first) == event(survivor) == current(1) == accepted
            peer.sendall(b'23,44,3.8,9000\n')
            accepted = current(2)
            assert accepted == {'temperature': 23, 'humidity': 44, 'voltage': 3.8, 'sequence': 2}
            assert event(first) == event(survivor) == accepted
            old_observer.close()
            peer.sendall(b'bad,44,3.8\n24,45,3.9\n')
            accepted = current(3)
            assert accepted['temperature'] == 24
            assert event(survivor) == accepted
            with events(port, last_id=1) as reconnected:
                # This endpoint offers a current snapshot, not a Last-Event-ID log.
                assert event(reconnected) == accepted
                code, body = request(port, 'POST', '/simulate')
                accepted = json.loads(body)
                assert code == 200 and accepted['sequence'] == 4
                assert event(survivor) == event(reconnected) == current(4) == accepted
    # New process, same canonical sources: in-memory sequence resets.
    with gateway(binary) as (_, _, current):
        assert current()['sequence'] == 0
    print('PASS: MQTT unavailable; HTTP/Unix input share order 1–4; malformed CSV adds no acceptance; surviving observer continues; reconnect gets current 3 then live 4; restart resets to zero')


if __name__ == '__main__':
    mode, binary = sys.argv[1:]
    {'framing': framing, 'mixed': mixed}[mode](binary)
