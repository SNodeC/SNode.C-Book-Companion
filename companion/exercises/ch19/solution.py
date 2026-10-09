"""Observe exact request validation, live events, and current-state reconnect."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab_support import connect, event, events, free_port, request, running

port = free_port()
with running(sys.argv[1], ['legacy', 'local', '--host=127.0.0.1', f'--port={port}']) as (process, _):
    with connect(port, process):
        pass
    assert request(port, 'GET', '/events', {'Accept': 'text/event-stream;q=0'})[0] == 406
    with events(port) as stream:
        initial = event(stream)
        previous = initial['sequence']
        for _ in range(2):
            status, body = request(port, 'POST', '/simulate')
            assert status == 200
            accepted = json.loads(body)
            assert accepted['sequence'] == previous + 1
            assert event(stream) == accepted
            previous = accepted['sequence']
    with events(port, initial['sequence']) as stream:
        assert event(stream) == accepted
print('PASS: 406 on restricted Accept; two matching live events; reconnect starts at current state')
