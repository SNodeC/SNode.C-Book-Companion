"""Bounded MQTT peers: packet observations and delivery through a real local broker."""
from pathlib import Path
import os
import socket
import struct
import subprocess
import sys
import tempfile
import time
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab_support import connect, free_port, receive, running


def packet(peer):
    kind = receive(peer, 1)[0]
    remaining = 0
    for shift in range(0, 28, 7):
        digit = receive(peer, 1)[0]
        remaining |= (digit & 127) << shift
        if digit < 128:
            assert remaining <= 4096, 'Fixture packet exceeds its observation bound'
            return kind, receive(peer, remaining)
    raise AssertionError('Invalid MQTT remaining length')


def field(value):
    value = value.encode() if isinstance(value, str) else value
    return struct.pack('!H', len(value)) + value


def send(peer, kind, body):
    assert len(body) < 128
    peer.sendall(bytes([kind, len(body)]) + body)


def session(peer):
    send(peer, 0x10, field('MQTT') + b'\x04\x02\x00\x3c' + field('book-observer'))
    assert packet(peer) == (0x20, b'\x00\x00')
    print('PASS: observer session accepted by CONNACK', flush=True)


def subscribe(peer, topic, identity=1):
    token = struct.pack('!H', identity)
    send(peer, 0x82, token + field(topic) + b'\x00')
    assert packet(peer) == (0x90, token + b'\x00')
    print('PASS: subscriber receives SUBACK granting QoS 0', flush=True)


def wait_log(path, value):
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        if value in path.read_text():
            return
        time.sleep(.02)
    raise AssertionError(f'Missing {value!r}: {path.read_text()}')


def role_packets(peer):
    kind, body = packet(peer)
    assert kind == 0x82 and body[2:] == field('sensors/+/command') + b'\x00'
    send(peer, 0x90, body[:2] + b'\x00')
    assert packet(peer) == (0x30, field('sensors/temperature/value') + b'23.5')


def wire(client):
    with socket.socket() as listener:
        listener.bind(('127.0.0.1', 0)); listener.listen(1); listener.settimeout(8)
        args = ['--log-level=6', 'mqtt', 'remote', '--host=127.0.0.1', f'--port={listener.getsockname()[1]}']
        with running(client, args) as (_, log), listener.accept()[0] as peer:
            peer.settimeout(5)
            kind, body = packet(peer)
            assert kind == 0x10 and body == field('MQTT') + b'\x04\x02\x00\x3c' + field('sensor-client-1')
            peer.settimeout(.2)
            try:
                data = peer.recv(1)
                raise AssertionError(f'Packet before CONNACK: {data!r}')
            except socket.timeout:
                pass
            peer.settimeout(5)
            send(peer, 0x20, b'\x00\x00')
            role_packets(peer)
            send(peer, 0x30, field('sensors/temperature/command') + b'wire-command')
            wait_log(log, 'MQTT command on sensors/temperature/command: wire-command')
            print('PASS: CONNECT first; no subscription/publication before acceptance; accepted session produces SUBSCRIBE/PUBLISH and receives command')


def delivery(client, broker):
    port = free_port()
    with running(broker, ['--log-level=6', 'broker', 'local', '--host=127.0.0.1', f'--port={port}']) as (server, _):
        with connect(port, server) as observer:
            session(observer); subscribe(observer, 'sensors/temperature/value')
            with running(client, ['--log-level=6', 'mqtt', 'remote', '--host=127.0.0.1', f'--port={port}']) as (_, log):
                assert packet(observer) == (0x30, field('sensors/temperature/value') + b'23.5')
                print('PASS: independent subscriber receives exact topic sensors/temperature/value and payload 23.5', flush=True)
                send(observer, 0x30, field('sensors/temperature/command') + b'broker-command')
                wait_log(log, 'MQTT command on sensors/temperature/command: broker-command')
                print('PASS: broker routes command to canonical client role', flush=True)
            send(observer, 0xe0, b'')


if __name__ == '__main__':
    with tempfile.TemporaryDirectory(prefix='mqtt-lab-state-') as state:
        os.chdir(state)  # Contain the canonical role's relative session filename.
        mode, client, broker, *rest = sys.argv[1:]
        if mode == 'wire':
            wire(client)
        else:
            delivery(client, broker)
            if mode == 'checkpoint':
                subprocess.run([sys.executable, str(Path(__file__).resolve().parents[1]/'ch30/solution.py'), rest[0]], check=True, timeout=40)
                print('PASS: Part VIII checkpoint: broker-delivery evidence and separate HTTP/status/SSE acceptance with unavailable MQTT; see README boundary map')
