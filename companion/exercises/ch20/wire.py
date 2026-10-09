"""Independent WebSocket wire observations shared by public labs and lifetime checks."""
import base64
import hashlib
import struct
import socket

def exact(peer, size):
    result = bytearray()
    while len(result) < size:
        chunk = peer.recv(size - len(result))
        assert chunk, 'WebSocket closed inside a frame'
        result.extend(chunk)
    return bytes(result)


def send_frame(peer, opcode, payload, final=True):
    mask = b'book'
    header = bytes([(128 if final else 0) | opcode])
    if len(payload) < 126:
        header += bytes([128 | len(payload)])
    else:
        header += b'\xfe' + struct.pack('!H', len(payload))
    peer.sendall(header + mask + bytes(value ^ mask[i % 4] for i, value in enumerate(payload)))


def frame(peer):
    first, second = exact(peer, 2)
    assert not second & 128, 'Server must not mask frames'
    size = second & 127
    if size == 126:
        size = struct.unpack('!H', exact(peer, 2))[0]
    elif size == 127:
        size = struct.unpack('!Q', exact(peer, 8))[0]
    return bool(first & 128), first & 15, exact(peer, size)


def message(peer):
    final, opcode, payload = frame(peer)
    while not final:
        final, continuation, chunk = frame(peer)
        assert continuation == 0
        payload += chunk
    return opcode, payload


def echo_exchange(peer):
    port = peer.getpeername()[1]
    key = base64.b64encode(b'book-echo-test!!').decode()
    peer.sendall((f'GET /ws HTTP/1.1\r\nHost: localhost:{port}\r\nUpgrade: websocket\r\n'
                  f'Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n'
                  'Sec-WebSocket-Protocol: echo\r\n\r\n').encode())
    response = bytearray()
    while not response.endswith(b'\r\n\r\n'):
        response.extend(exact(peer, 1))
    assert b' 101 ' in response and b'sec-websocket-protocol: echo' in response.lower()
    accepted = base64.b64encode(hashlib.sha1((key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode()).digest())
    assert accepted in response
    for opcode, payload in [(1, b'hello'), (2, b'\x00\xff\x80binary\x00'), (1, b''),
                            (2, b''), (1, b'after binary'), (2, bytes(range(256)) * 32)]:
        send_frame(peer, opcode, payload)
        assert message(peer) == (opcode, payload), f'Type/payload mismatch for opcode {opcode}'
    for opcode, payload in [(1, 'fragmented \u20ac message'.encode()), (2, b'\x00\xfffragmented\x80')]:
        split = 12 if opcode == 1 else 3
        send_frame(peer, opcode, payload[:split], final=False)
        send_frame(peer, 9, b'ping')
        assert message(peer) == (10, b'ping')
        send_frame(peer, 0, payload[split:])
        assert message(peer) == (opcode, payload)
    send_frame(peer, 8, struct.pack('!H', 1000))
    opcode, payload = message(peer)
    assert opcode == 8 and payload[:2] == struct.pack('!H', 1000)
    peer.shutdown(socket.SHUT_WR)
    assert peer.recv(1) == b''
