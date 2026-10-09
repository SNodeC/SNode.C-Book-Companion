"""Public TLS observations, reusing the existing policy probe and EchoPair context."""
from pathlib import Path
import ssl
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab_support import connect, environment, free_port, receive, running


def policy(client, openssl):
    fixture = Path(__file__).with_name('run-tls.py')
    with tempfile.TemporaryDirectory(prefix='tls-policy-lab-') as temp:
        subprocess.run([sys.executable, str(fixture), '--client', client, '--openssl', openssl],
                       env=environment(temp), check=True, timeout=50)


def echo(server, openssl):
    with tempfile.TemporaryDirectory(prefix='tls-echo-lab-') as temp:
        cert, key = Path(temp) / 'cert.pem', Path(temp) / 'key.pem'
        subprocess.run([openssl, 'req', '-x509', '-newkey', 'rsa:2048', '-nodes', '-days', '1',
                        '-subj', '/CN=sensor.example', '-addext', 'subjectAltName=DNS:sensor.example',
                        '-keyout', str(key), '-out', str(cert)], check=True, timeout=15,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        context = ssl.create_default_context(cafile=str(cert))
        port = free_port()
        with running(server, ['echoserver', 'local', '--host=127.0.0.1', f'--port={port}',
                              'tls', f'--cert={cert}', f'--cert-key={key}']) as (process, log):
            with connect(port, process) as peer:
                with context.wrap_socket(peer, server_hostname='sensor.example') as stream:
                    payload = b'part-vi\x00secure-echo\xff'
                    stream.sendall(payload)
                    assert receive(stream, len(payload)) == payload
                    # unwrap waits for the reciprocal TLS close_notify, not just TCP EOF.
                    with stream.unwrap():
                        pass
            print('PASS: trusted sensor.example; exact binary echo; reciprocal close_notify')


if __name__ == '__main__':
    {'policy': policy, 'echo': echo}[sys.argv[1]](*sys.argv[2:])
