"""Inspect the canonical echo configuration and correlate it with bounded runtime work."""
from contextlib import ExitStack
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab_support import connect, environment, free_port, receive, running


def invoke(binary, args, home):
    result = subprocess.run([binary, *args], env=environment(home), capture_output=True,
                            text=True, timeout=10)
    output = result.stdout + result.stderr
    assert result.returncode == 2, (result.returncode, output)
    return output


def port_value(output):
    rows = re.findall(r'^\s*(#\s*)?echoserver\.local\.port\s*=\s*(\d+)\s*$', output, re.M)
    assert rows, output
    active = [int(value) for comment, value in rows if not comment]
    assert len(active) <= 1, rows
    return active[0] if active else int(rows[-1][1])


def precedence(binary, home, selected=18092):
    path = Path(home) / 'echo.conf'
    contents = 'echoserver.local.port = 18091\n'
    path.write_text(contents)
    args = ['--config-file', str(path)]
    observed = [port_value(invoke(binary, ['--show-config'], home)),
                port_value(invoke(binary, [*args, '--show-config'], home)),
                port_value(invoke(binary, [*args, '--show-config', 'echoserver', 'local',
                                          f'--port={selected}'], home))]
    assert observed == [8080, 18091, selected], observed
    assert path.read_text() == contents, 'Inspection/override changed persistent configuration'
    print(f'PASS: source/file/CLI ports {observed}; file unchanged; inspection status 2')
    return args


def discovery(binary, home):
    for args, expected in [(['--help'], 'echoserver'),
                           (['echoserver', '--help'], 'local'),
                           (['echoserver', 'local', '--help'], '--port')]:
        output = invoke(binary, args, home)
        assert expected in output, output
    output = invoke(binary, ['echoserver', 'local', '--port=70000'], home)
    assert '[ValidationError]' in output and '--port' in output and '65535' in output, output
    assert 'listening on' not in output, output
    print('PASS: help narrows application/instance/local; invalid --port rejected; local help identifies its scope')


def checkpoint(binary, home):
    port = free_port()
    args = precedence(binary, home, port)
    discovery(binary, home)
    histories = []
    for scoped in [False, True]:
        policy = ['--log-level=2', '--log-format=json']
        if scoped:
            policy += ['--log-component-level=echo=info', '--log-instance-level=echoserver=debug']
        with ExitStack() as readers:
            with running(binary, [*args, *policy, 'echoserver', 'local', '--host=127.0.0.1',
                                  f'--port={port}']) as (process, log):
                # Retain the log across the harness's temporary-directory cleanup.
                completed_log = readers.enter_context(log.open())
                with connect(port, process) as peer:
                    payload = b'part-v-checkpoint'
                    peer.sendall(payload)
                    assert receive(peer, len(payload)) == payload
            # Normal shutdown drains asynchronous records before we inspect them.
            histories.append([json.loads(line) for line in completed_log])
    assert not histories[0], histories[0]
    records = histories[1]
    assert any(r['component'] == 'echo' and r['level'] == 'info'
               and str(port) in r['message'] for r in records), records
    context = [r for r in records if r.get('instance') == 'echoserver'
               and r.get('boundary') == 'context' and r.get('origin') == 'application']
    assert any(r['level'] == 'debug' and 'part-v-checkpoint' in r['message']
               and r.get('connection') for r in context), context
    print('PASS: Part V checkpoint: CLI-selected listener echoes; narrow overrides reveal role/context records')
    print('Global Error run: 0 records; scoped run:', json.dumps(records, sort_keys=True))


if __name__ == '__main__':
    mode, binary = sys.argv[1:]
    with tempfile.TemporaryDirectory(prefix='config-lab-') as home:
        {'precedence': precedence, 'discovery': discovery, 'checkpoint': checkpoint}[mode](binary, home)
