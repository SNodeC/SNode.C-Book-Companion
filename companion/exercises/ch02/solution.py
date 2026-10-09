"""Build the canonical external consumer; diagnose a temporary component typo."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab_support import connect, free_port, receive, running

mode = sys.argv[1]
assert mode in ('consumer', 'component')
selected_package = Path(sys.argv[2]).resolve()
source = Path(__file__).resolve().parents[2] / 'examples' / 'EchoPair'
with tempfile.TemporaryDirectory(prefix='snodec-environment-lab-') as temporary:
    work = Path(temporary)
    build = work / 'build'
    if mode == 'component':
        source = Path(shutil.copytree(source, work / 'EchoPair'))
        cmake = source / 'CMakeLists.txt'
        original = cmake.read_text()
        assert 'net-in-stream-legacy' in original
        cmake.write_text(original.replace('net-in-stream-legacy', 'net-in-stream-missing'))
    configure = ['cmake', '-S', str(source), '-B', str(build),
                 f'-Dsnodec_DIR={selected_package}', '-DCMAKE_BUILD_TYPE=Debug',
                 '-DCMAKE_EXE_LINKER_FLAGS=-Wl,--disable-new-dtags']
    if mode == 'component':
        failed = subprocess.run(configure, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True, timeout=40)
        print(failed.stdout)
        assert failed.returncode != 0 and 'net-in-stream-missing' in failed.stdout
        assert not (build / 'echoserver').exists()
        print('PASS: missing component stops configuration before any runtime endpoint exists')
        cmake.write_text(original)
    subprocess.run(configure, check=True, timeout=40)
    cache = (build / 'CMakeCache.txt').read_text().splitlines()
    package = next(line.split('=', 1)[1] for line in cache if line.startswith('snodec_DIR:'))
    assert Path(package).resolve() == selected_package, package
    print(f'PASS: snodec_DIR selects the requested installation: {package}')
    subprocess.run(['cmake', '--build', str(build), '--parallel', '2'], check=True, timeout=90)
    port = free_port()
    args = ['echoserver', 'local', '--host=127.0.0.1', f'--port={port}']
    with running(str(build / 'echoserver'), args) as (process, log):
        with connect(port, process) as peer:
            payload = b'environment-ready\n'
            peer.sendall(payload)
            assert receive(peer, len(payload)) == payload
    print('PASS: canonical EchoPair builds and its server reflects environment-ready unchanged')
