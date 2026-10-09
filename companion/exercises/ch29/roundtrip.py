import math
import socket
import statistics
import time

payload = bytes(range(256))
samples = []
with socket.create_connection(("127.0.0.1", 18093), timeout=3) as peer:
    peer.settimeout(3)
    for index in range(220):
        started = time.perf_counter_ns()
        peer.sendall(payload)
        received = bytearray()
        while len(received) < len(payload):
            chunk = peer.recv(len(payload) - len(received))
            if not chunk:
                raise RuntimeError("echo closed before the complete reply")
            received.extend(chunk)
        elapsed_us = (time.perf_counter_ns() - started) / 1000
        assert bytes(received) == payload
        if index >= 20:
            samples.append(elapsed_us)
ordered = sorted(samples)
print(f"samples={len(samples)} bytes={len(payload)} connections=1")
print(f"median_us={statistics.median(samples):.2f}")
print(f"p95_us={ordered[math.ceil(0.95 * len(ordered)) - 1]:.2f}")
