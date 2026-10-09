"""Disposable Unix-socket MariaDB; independent queries distinguish acceptance from storage."""
from contextlib import contextmanager
from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile
import time
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab_support import running


def program(name):
    path = shutil.which(name) or next((str(p) for p in [Path('/usr/sbin')/name, Path('/usr/local/sbin')/name] if p.is_file()), None)
    if not path:
        raise RuntimeError(f'Equipped lab needs {name}; install MariaDB server and client packages (see README).')
    return path


@contextmanager
def database():
    server, install, client = (program(n) for n in ['mariadbd', 'mariadb-install-db', 'mariadb'])
    if shutil.disk_usage(tempfile.gettempdir()).free < 512 * 1024 * 1024:
        raise RuntimeError('Private database lab requires at least 512 MiB free temporary space before initialization.')
    storage = ['--innodb-log-file-size=8M', '--innodb-undo-tablespaces=0', '--innodb-buffer-pool-size=32M']
    root = Path(tempfile.mkdtemp(prefix='book-db-'))
    process = None
    try:
        socket = root/'server.sock'; data = root/'data'
        setup = subprocess.run([install, '--no-defaults', f'--datadir={data}',
                                '--auth-root-authentication-method=normal', '--skip-test-db', *storage],
                               capture_output=True, text=True, timeout=45)
        assert setup.returncode == 0, setup.stdout + setup.stderr
        def query(sql):
            result = subprocess.run([client, '--no-defaults', '--protocol=socket', f'--socket={socket}',
                                     '--user=root', '--batch', '--skip-column-names', '-e', sql],
                                    capture_output=True, text=True, timeout=8)
            assert result.returncode == 0, result.stderr
            return result.stdout.strip()
        with (root/'server.log').open('w') as log:
            process = subprocess.Popen([server, '--no-defaults', f'--datadir={data}', f'--socket={socket}',
                                        '--skip-networking', f'--pid-file={root / "server.pid"}',
                                        '--innodb-flush-log-at-trx-commit=1', *storage],
                                       stdout=log, stderr=subprocess.STDOUT)
            try:
                deadline = time.monotonic() + 15
                while True:
                    assert process.poll() is None, (root/'server.log').read_text()
                    if socket.exists():
                        try:
                            assert query('SELECT 1') == '1'; break
                        except AssertionError:
                            pass
                    assert time.monotonic() < deadline, (root/'server.log').read_text()
                    time.sleep(.05)
                assert query('SELECT @@autocommit, @@innodb_flush_log_at_trx_commit') == '1\t1'
                query('CREATE DATABASE book; CREATE TABLE book.measurements (sensor VARCHAR(64) NOT NULL, value DOUBLE NOT NULL) ENGINE=InnoDB')
                yield str(socket), query
            finally:
                if process.poll() is None:
                    query('SHUTDOWN')
                    process.wait(timeout=15)
                assert process.returncode == 0, (root/'server.log').read_text()
    finally:
        if process is None or process.poll() is not None:
            shutil.rmtree(root)
        else:
            print(f'Database shutdown failed; live server state retained at {root}', file=sys.stderr)


def client_run(client, socket, sql, expected):
    # Only this child receives the private socket and selected fixture statement.
    previous = {k: os.environ.get(k) for k in ['BOOK_DB_SOCKET', 'BOOK_DB_SQL']}
    os.environ.update(BOOK_DB_SOCKET=socket, BOOK_DB_SQL=sql)
    try:
        with running(client, ['--log-level=6']) as (process, log):
            deadline = time.monotonic() + 10
            while 'measurement query complete' not in log.read_text():
                assert process.poll() is None, log.read_text()
                assert time.monotonic() < deadline, log.read_text()
                time.sleep(.02)
            output = log.read_text()
            for message in expected:
                assert message in output, output
    finally:
        for key, value in previous.items():
            if value is None: os.environ.pop(key, None)
            else: os.environ[key] = value


def observe(mode, client):
    with database() as (socket, query):
        assert query('SELECT COUNT(*) FROM book.measurements') == '0'
        if mode == 'error':
            client_run(client, socket, 'INSERT INTO book.no_such_table VALUES (1)', ['insert error 1146', 'measurement query complete'])
            assert query('SELECT COUNT(*) FROM book.measurements') == '0'
            print('PASS: SQL error 1146 leaves the connection usable; the chained query completes and independent row count stays zero', flush=True)
        else:
            client_run(client, socket, "INSERT INTO measurements(sensor, value) VALUES ('temperature', 23.5)", ['insert affected rows: 1', 'measurement: temperature = 23.5'])
            assert query('SELECT sensor, value FROM book.measurements') == 'temperature\t23.5'
            print('PASS: autocommitted insert survives client shutdown; independent query reads temperature=23.5', flush=True)
            client_run(client, socket, 'DO 0', ['measurement: temperature = 23.5'])
            assert query('SELECT COUNT(*) FROM book.measurements') == '1'
            print('PASS: restarted canonical client reads the same row without adding another; committed state outlives the client', flush=True)


if __name__ == '__main__':
    mode, client, *rest = sys.argv[1:]
    observe(mode, client)
    if mode == 'checkpoint':
        subprocess.run([sys.executable, str(Path(__file__).resolve().parents[1]/'ch30/solution.py'), rest[0]], check=True, timeout=40)
        print('PASS: Part IX checkpoint contrasts database read-back with the separate in-memory gateway restart; apply the README MQTTStore outcome map')
