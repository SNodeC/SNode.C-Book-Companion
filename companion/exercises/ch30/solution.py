"""Local state remains observable while the configured MQTT endpoint refuses connections."""
import json
import socket
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab_support import connect, event, events, free_port, request, running

with socket.socket() as unavailable:
    unavailable.bind(('127.0.0.1', 0))  # Reserve an endpoint without listening.
    mqtt_port = unavailable.getsockname()[1]
    for iteration in range(2):
        port = free_port()
        args = ['web', 'local', '--host=127.0.0.1', f'--port={port}',
                'mqtt-uplink', 'remote', '--host=127.0.0.1', f'--port={mqtt_port}']
        with running(sys.argv[1], args) as (process, _):
            with connect(port, process):
                pass
            assert request(port, 'GET', '/health')[0] == 200
            status, body = request(port, 'GET', '/status')
            assert status == 200 and json.loads(body)['sequence'] == 0
            if iteration == 0:
                with events(port) as stream:
                    for sequence in (1, 2):
                        status, body = request(port, 'POST', '/simulate')
                        assert status == 200
                        accepted = json.loads(body)
                        assert accepted['sequence'] == sequence
                        assert event(stream) == accepted
                        status, body = request(port, 'GET', '/status')
                        assert status == 200 and json.loads(body) == accepted
print('PASS: HTTP/status/SSE agree without MQTT; restart resets sequence to zero')
