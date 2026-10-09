import argparse
import pathlib
import tempfile
import subprocess
import ssl
import socket
import threading
import os
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from lab_support import isolated_xdg
parser = argparse.ArgumentParser(description='Check the book TLS policy against controlled local certificate identities.')
parser.add_argument('--client', type=pathlib.Path, required=True)
parser.add_argument('--openssl', default='openssl')
args = parser.parse_args()
executable = args.client
with tempfile.TemporaryDirectory(prefix='snodec-book-tls-') as directory:
    root=pathlib.Path(directory)
    for name in ('sensor.example','wrong.example','unrelated.example'):
        subprocess.run([args.openssl,'req','-x509','-newkey','rsa:2048','-nodes','-days','1',
                        '-subj',f'/CN={name}','-addext',f'subjectAltName=DNS:{name}',
                        '-keyout',str(root/f'{name}.key'),'-out',str(root/f'{name}.pem')],
                       check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    for label,identity,trust,expected in [
        ('trusted matching name','sensor.example','sensor.example',True),
        ('trusted wrong name','wrong.example','wrong.example',False),
        ('untrusted matching name','sensor.example','unrelated.example',False)]:
        context=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(root/f'{identity}.pem', root/f'{identity}.key')
        with socket.socket() as listener:
            listener.bind(('127.0.0.1',0));listener.listen(1);listener.settimeout(10)
            failures=[]
            def serve():
                try:
                    with listener.accept()[0] as peer:
                        peer.settimeout(5)
                        try:
                            with context.wrap_socket(peer,server_side=True) as stream:
                                stream.recv(1)
                        except ssl.SSLError:
                            if expected: raise
                except Exception as e: failures.append(repr(e))
            thread=threading.Thread(target=serve);thread.start()
            env=dict(os.environ, **isolated_xdg(root))
            result=subprocess.run([str(executable),'probe','remote','--host','127.0.0.1',
                '--port',str(listener.getsockname()[1]),'tls','--ca-cert',str(root/f'{trust}.pem'),
                '--ca-cert-dir-use-default=false','--ca-cert-accept-unknown=false'],env=env,
                capture_output=True,text=True,timeout=15)
            thread.join(timeout=10)
            if result.returncode or failures or f'early_ssl_null=1 ready={int(expected)} result=0' not in result.stdout:
                raise RuntimeError((label,result.returncode,result.stdout,result.stderr,failures))
            print(f'PASS: {label}; early SSL is null; ready={int(expected)}')
