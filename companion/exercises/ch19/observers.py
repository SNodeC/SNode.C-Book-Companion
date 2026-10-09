"""Live observers share accepted data but have independent connection lifetimes."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab_support import connect, event, events, free_port, request, running

port = free_port()
with running(sys.argv[1], ['legacy', 'local', '--host=127.0.0.1', f'--port={port}']) as (process, _):
    with connect(port, process):
        pass
    with events(port) as remaining:
        initial = event(remaining)
        with events(port) as departing:
            assert event(departing) == initial
            status, body = request(port, 'POST', '/simulate')
            assert status == 200
            accepted = json.loads(body)
            assert accepted['sequence'] == initial['sequence'] + 1
            assert event(remaining) == event(departing) == accepted
        status, body = request(port, 'POST', '/simulate')
        assert status == 200
        latest = json.loads(body)
        assert latest['sequence'] == accepted['sequence'] + 1
        assert event(remaining) == latest
print('PASS: both observers see the same acceptance; remaining observer continues after peer closes')
