"""Controlled WebSocket peer for the installed MQTT adapter, not a broker."""
from pathlib import Path
import base64
import hashlib
import os
import socket
import struct
import sys
import tempfile
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'ch21'))
from lab_support import receive, running
from mqtt import field, packet, role_packets, send, wait_log


class Peer:
    def __init__(self, socket):
        self.socket = socket
        self.buffer = bytearray()

    def frame(self):
        first, second = receive(self.socket, 2)
        assert second & 128, 'Client frames must be masked'
        size = second & 127
        if size == 126:
            size = struct.unpack('!H', receive(self.socket, 2))[0]
        elif size == 127:
            size = struct.unpack('!Q', receive(self.socket, 8))[0]
        assert size <= 4096
        mask = receive(self.socket, 4)
        data = receive(self.socket, size)
        return first & 15, bytes(v ^ mask[i % 4] for i, v in enumerate(data))

    def recv(self, size):
        if not self.buffer:
            opcode, data = self.frame()
            assert opcode == 2, (opcode, data)
            self.buffer.extend(data)
        out = bytes(self.buffer[:size]); del self.buffer[:size]
        return out

    def frame_send(self, opcode, payload, final=True):
        assert len(payload) < 126
        self.socket.sendall(bytes([(128 if final else 0) | opcode, len(payload)]) + payload)

    def sendall(self, payload):
        self.frame_send(2, payload)


def run(mode, client):
    with socket.socket() as listener:
        listener.bind(('127.0.0.1', 0)); listener.listen(1); listener.settimeout(8)
        args = ['--log-level=6', 'legacy', 'remote', '--host=127.0.0.1', f'--port={listener.getsockname()[1]}']
        with running(client, args) as (_, log), listener.accept()[0] as socket_peer:
            socket_peer.settimeout(5)
            request = bytearray()
            while not request.endswith(b'\r\n\r\n'):
                assert len(request) < 8192
                request.extend(receive(socket_peer, 1))
            headers = dict(line.split(b':', 1) for line in bytes(request).split(b'\r\n')[1:-2])
            headers = {k.lower():v.strip() for k,v in headers.items()}
            assert headers[b'sec-websocket-protocol'] == b'mqtt'
            accepted = base64.b64encode(hashlib.sha1(headers[b'sec-websocket-key'] + b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11').digest())
            socket_peer.sendall(b'HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Protocol: mqtt\r\nSec-WebSocket-Accept: ' + accepted + b'\r\n\r\n')
            peer = Peer(socket_peer)
            assert packet(peer) == (0x10, field('MQTT') + b'\x04\x02\x00\x3c' + field('sensor-client-1'))
            print('PASS: HTTP 101, mqtt selection and binary MQTT CONNECT observed', flush=True)
            connack = b'\x20\x02\x00\x00'
            if mode == 'text':
                peer.frame_send(1, connack)
                opcode, payload = peer.frame()
                assert opcode == 8 and payload[:2] == struct.pack('!H', 1002), (opcode, payload)
                peer.frame_send(8, payload)
                wait_log(log, 'Wrong Opcode: 1 (TEXT)')
                print('PASS: same packet bytes in text trigger protocol-error close 1002')
            else:
                peer.frame_send(2, connack[:2], False)
                peer.frame_send(0, connack[2:])
                role_packets(peer)
                send(peer, 0x30, field('sensors/temperature/command') + b'adapter-command')
                wait_log(log, 'MQTT command on sensors/temperature/command: adapter-command')
                print('PASS: fragmented binary CONNACK admits MQTT flow; binary command reaches canonical role')


if __name__ == '__main__':
    with tempfile.TemporaryDirectory(prefix='mqtt-ws-state-') as state:
        os.chdir(state)
        run(*sys.argv[1:])
