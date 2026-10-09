"""Local peers for the public labs. No broker or framework source checkout needed."""
import contextlib
import http.client
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import tempfile
import time


def free_port():
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]


def isolated_xdg(root):
    """Keep configuration, state and runtime files under one private lab root."""
    result = {}
    for variable, name in (('XDG_CONFIG_HOME', 'config'), ('XDG_STATE_HOME', 'state'),
                           ('XDG_RUNTIME_DIR', 'runtime')):
        path = Path(root).resolve() / name
        path.mkdir(mode=0o700, parents=True, exist_ok=True)
        path.chmod(0o700)
        result[variable] = str(path)
    return result


def environment(config_home):
    return dict(os.environ, **isolated_xdg(config_home))


@contextlib.contextmanager
def running(executable, args, *, stderr=subprocess.STDOUT):
    with tempfile.TemporaryDirectory(prefix='snodec-lab-') as temp:
        env = environment(temp)
        path = Path(temp) / 'process.log'
        with path.open('wb') as output:
            process = subprocess.Popen([executable, *args], env=env, stdout=output,
                                       stderr=stderr, stdin=subprocess.DEVNULL)
            try:
                yield process, path
            except BaseException:
                print(path.read_text(errors='replace')[-8000:])
                raise
            finally:
                interrupted = process.poll() is None
                if interrupted:
                    process.send_signal(signal.SIGINT)
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait()
                        raise RuntimeError('Process did not stop after SIGINT')
                # SNode.C start() returns -stopsig: handled SIGINT is shell status 254.
                # Accept it only when this harness actually requested that shutdown.
                expected = (0, 254) if interrupted else (0,)
                if process.returncode not in expected:
                    raise RuntimeError(f'Process exited {process.returncode}: {path.read_text(errors="replace")[-4000:]}')


def connect(port, process):
    deadline = time.monotonic() + 8
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError('Server exited before connection')
        try:
            peer = socket.create_connection(('127.0.0.1', port), timeout=0.25)
            peer.settimeout(5)
            return peer
        except ConnectionRefusedError:
            time.sleep(0.03)
    raise TimeoutError('Server did not accept a connection')


def receive(peer, size):
    data = bytearray()
    while len(data) < size:
        part = peer.recv(size - len(data))
        if not part:
            raise RuntimeError(f'EOF after {len(data)} of {size} bytes')
        data.extend(part)
    return bytes(data)


def request(port, method, path, headers=None):
    conn = http.client.HTTPConnection('127.0.0.1', port, timeout=5)
    try:
        conn.request(method, path, headers=headers or {})
        response = conn.getresponse()
        return response.status, response.read()
    finally:
        conn.close()


@contextlib.contextmanager
def events(port, last_id=None):
    conn = http.client.HTTPConnection('127.0.0.1', port, timeout=5)
    headers = {'Accept': 'text/event-stream'}
    if last_id is not None:
        headers['Last-Event-ID'] = str(last_id)
    try:
        conn.request('GET', '/events', headers=headers)
        response = conn.getresponse()
        assert response.status == 200
        assert response.getheader('Content-Type') == 'text/event-stream'
        try:
            yield response
        finally:
            response.close()
    finally:
        conn.close()


def event(response):
    fields = {}
    while True:
        line = response.readline()
        if not line:
            raise RuntimeError('Event stream ended before a record')
        line = line.decode().rstrip('\r\n')
        if not line and 'data' in fields:
            assert fields['event'] == 'measurement'
            payload = json.loads(fields['data'])
            assert int(fields['id']) == payload['sequence']
            return payload
        if ':' in line:
            key, value = line.split(':', 1)
            fields[key] = value.lstrip(' ')
