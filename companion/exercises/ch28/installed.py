"""A fresh canonical consumer installation, bounded public observations and cleanup."""
from contextlib import contextmanager
import json
import os
from pathlib import Path
import platform
import re
import socket
import subprocess
import sys
import tempfile
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab_support import connect, environment, free_port, receive, running


def checked(command):
    subprocess.run(list(map(str, command)), check=True, timeout=90)


@contextmanager
def installed():
    selected_package = Path(sys.argv[2]).resolve()
    source = Path(__file__).resolve().parents[2] / 'examples/EchoPair'
    with tempfile.TemporaryDirectory(prefix='installed-echo-') as temporary:
        work = Path(temporary); build = work/'build'; destination = work/'install'
        checked(['cmake', '-S', source, '-B', build, '-DCMAKE_BUILD_TYPE=Release',
                 f'-Dsnodec_DIR={selected_package}', f'-DCMAKE_INSTALL_PREFIX={destination}',
                 '-DCMAKE_FIND_USE_PACKAGE_REGISTRY=OFF', '-DCMAKE_FIND_USE_SYSTEM_PACKAGE_REGISTRY=OFF',
                 '-DCMAKE_INSTALL_BINDIR=bin', '-DCMAKE_EXE_LINKER_FLAGS=-Wl,--disable-new-dtags',
                 f'-DCMAKE_INSTALL_RPATH={sys.argv[3]}'])
        cache = (build/'CMakeCache.txt').read_text().splitlines()
        package = next(s.split('=', 1)[1] for s in cache if s.startswith('snodec_DIR:'))
        assert Path(package).resolve() == selected_package, package
        checked(['cmake', '--build', build, '--parallel', '2'])
        checked(['cmake', '--install', build])
        binary = destination/'bin/echoserver'; assert binary.is_file()
        print(f'PASS: fresh external Release consumer installed at {binary}; snodec_DIR={package}', flush=True)
        # Installed paths must work without the developer harness supplying a loader path.
        clean = {k: v for k, v in os.environ.items() if k not in {'LD_LIBRARY_PATH', 'LD_PRELOAD'}}
        with patch.dict(os.environ, clean, clear=True):
            yield str(binary), work


def configuration(work, port):
    config = work/'echo.conf'
    config.write_text('daemonize=false\nlog-level=4\nlog-format=json\n'
                      f'echoserver.local.host=127.0.0.1\nechoserver.local.port={port}\n')
    return ['--config-file', str(config)]


def exchange(binary, args, port):
    with running(binary, args) as (process, log):
        with connect(port, process) as peer:
            payload = b'installed-consumer\x00\xff\n' * 64
            peer.sendall(payload); assert receive(peer, len(payload)) == payload
        identity = process.pid
    # Normal harness shutdown has completed before checking that the listener is gone.
    try:
        with socket.create_connection(('127.0.0.1', port), timeout=1):
            raise AssertionError('Listener still accepts after shutdown')
    except ConnectionRefusedError:
        pass
    print(f'PASS: installed process {identity} echoed exact binary bytes and stopped; new connection refused', flush=True)
    return identity


def lifecycle(binary, work):
    port = free_port(); args = configuration(work, port)
    first = exchange(binary, args, port); second = exchange(binary, args, port)
    assert first != second
    print('PASS: restart changes process identity and preserves the configured echo contract; no loader environment override', flush=True)


def invalid_configuration(binary, work):
    args = configuration(work, 'not-a-port')
    result = subprocess.run([binary, *args], env=environment(work), capture_output=True, text=True, timeout=10)
    output = result.stdout + result.stderr
    assert result.returncode == 2 and '--port' in output, (result.returncode, output)
    assert 'listening on' not in output
    print(output, flush=True)
    print('PASS: invalid configured port stops startup with configuration status 2', flush=True)
    port = free_port(); exchange(binary, configuration(work, port), port)
    print('PASS: restoring the configuration restores the installed public exchange', flush=True)


def diagnose(binary, work, measure=False):
    port = free_port(); args = configuration(work, port)
    with running(binary, args) as (process, log):
        with connect(port, process) as peer:
            peer.sendall(b'correct endpoint'); assert receive(peer, 16) == b'correct endpoint'
        # Reserve an unused local port without listening, so no other peer can take it.
        with socket.socket() as closed:
            closed.bind(('127.0.0.1', 0))
            try:
                with socket.create_connection(closed.getsockname(), timeout=1):
                    raise AssertionError('Non-listening endpoint unexpectedly accepted')
            except ConnectionRefusedError:
                print('PASS: wrong endpoint is refused after a successful build; correct endpoint echoes', flush=True)
        if measure:
            source = Path(__file__).resolve().parents[1]/'ch29/roundtrip.py'
            program = source.read_text(); address = '("127.0.0.1", 18093)'
            assert program.count(address) == 1
            program = program.replace(address, repr(('127.0.0.1', port)))
            result = subprocess.run([sys.executable, '-c', program], capture_output=True, text=True, timeout=15)
            assert result.returncode == 0, result.stderr
            assert 'samples=200 bytes=256 connections=1' in result.stdout, result.stdout
            values = dict(re.findall(r'(median_us|p95_us)=([0-9.]+)', result.stdout))
            assert 0 < float(values['median_us']) <= float(values['p95_us'])
            print(json.dumps({'platform': platform.platform(), 'build': 'Release', 'logging': 'Info / JSON to temporary file',
                              'endpoint': f'127.0.0.1:{port}', 'loader_override': False, 'warmup': 20}), flush=True)
            print(result.stdout, end='', flush=True)
            print('PASS: Part X checkpoint: fresh build/install, endpoint diagnosis, 200 exact-payload latency samples; no capacity claim', flush=True)


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode in {'diagnosis', 'checkpoint'}:
        checked([sys.executable, Path(__file__).resolve().parents[1]/'ch02/solution.py', 'component', sys.argv[2]])
    with installed() as (binary, work):
        if mode == 'lifecycle': lifecycle(binary, work)
        elif mode == 'configuration': invalid_configuration(binary, work)
        elif mode in {'diagnosis', 'checkpoint'}: diagnose(binary, work, mode == 'checkpoint')
        else: raise ValueError(mode)
