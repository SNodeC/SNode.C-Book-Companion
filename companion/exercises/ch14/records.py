"""Public solution: observe the canonical standalone logger without fabricated network identity."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab_support import environment


def observe(binary, env):
    result = subprocess.run([str(binary)], env=env, capture_output=True, text=True,
                            timeout=10, check=True)
    records = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
    assert len(records) == 4, records
    for record in records:
        for key, expected in {'origin': 'application', 'boundary': 'application',
                              'component': 'gateway.measurements', 'instance': 'measurement-input'}.items():
            assert record.get(key) == expected, record
        assert 'connection' not in record and 'role' not in record, record
    assert [r['level'] for r in records] == ['info', 'info', 'debug', 'warn'], records
    assert records[1]['event'] == 'measurement.accepted'
    assert records[3]['error']['code'] and 'no file operation' in records[3]['message']
    print('PASS: four semantic records; component Debug overrides global Info; event and typed error; no invented peer')
    return result.stdout


if __name__ == '__main__':
    with tempfile.TemporaryDirectory(prefix='logging-lab-') as home:
        print(observe(sys.argv[1], environment(home)), end='')
