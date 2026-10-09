"""Hold the protocol fixed; observe family-specific identities and owned cleanup."""
import socket
import sys
import tempfile
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab_support import receive, running

payload = b'900,23.5\n2,24.0\ninvalid\x00measurement'
for mode, binary in zip(sys.argv[1::2], sys.argv[2::2]):
    family = {'ipv4': socket.AF_INET, 'ipv6': socket.AF_INET6, 'unix': socket.AF_UNIX}[mode]
    with tempfile.TemporaryDirectory(prefix='endpoint-lab-') as directory:
        base = Path(directory)
        sentinel = base / 'keep.txt'
        sentinel.write_text('unrelated file')
        if mode == 'unix':
            address = str(base / 'service.sock')
            own = str(base / 'producer.sock')
            args = ['endpoint', 'local', f'--sun-path={address}']
        else:
            host = '127.0.0.1' if mode == 'ipv4' else '::1'
            with socket.socket(family) as reservation:
                reservation.bind((host, 0))
                address = (host, reservation.getsockname()[1])
            args = ['endpoint', 'local', f'--host={host}', f'--port={address[1]}']
        identity_log = base / 'identity.log'
        identity_log.touch()
        with identity_log.open('wb') as identities, running(binary, args, stderr=identities) as (process, log):
            deadline = time.monotonic() + 8
            while True:
                peer = socket.socket(family)
                peer.settimeout(3)
                if mode == 'unix':
                    peer.bind(own)
                try:
                    peer.connect(address)
                    break
                except (ConnectionRefusedError, FileNotFoundError):
                    peer.close()
                    if mode == 'unix':
                        Path(own).unlink()
                    if process.poll() is not None or time.monotonic() >= deadline:
                        raise RuntimeError(f'{mode}: endpoint did not become ready')
                    time.sleep(0.03)
            with peer:
                local, remote = peer.getsockname(), peer.getpeername()
                peer.sendall(payload)
                assert receive(peer, len(payload)) == payload
                deadline = time.monotonic() + 3
                while not any(line.startswith('IDENTITY\t') for line in identity_log.read_text().splitlines()):
                    if time.monotonic() > deadline:
                        raise RuntimeError('Server did not report connection identities')
                    time.sleep(0.02)
                identity = next(line for line in identity_log.read_text().splitlines() if line.startswith('IDENTITY\t'))
                _, server_local, server_remote = identity.split('\t')
                if mode == 'unix':
                    assert (server_local, server_remote) == (address, own)
                    assert remote == address
                else:
                    for rendered, observed in [(server_local, remote), (server_remote, local)]:
                        host_text, port_text = rendered.rsplit(':', 1)
                        candidates = socket.getaddrinfo(host_text.strip('[]'), int(port_text), family, socket.SOCK_STREAM)
                        assert observed[:2] in {item[4][:2] for item in candidates}
                    assert remote[:2] == address
                print(identity)
                print(f'{mode}: producer local={local}, service={remote}')
            if mode == 'unix':
                Path(own).unlink()  # The Python client owns its bind path.
                assert Path(address).is_socket()
        if mode == 'unix':
            assert not Path(address).exists(), 'Server-owned socket path survived shutdown'
        assert sentinel.read_text() == 'unrelated file'
        print(f'PASS: {mode}: exact measurement bytes, matching identities, owned cleanup')
