# Chapter 24 — solutions and discussion

## 1. Review (O1)

A connection, pending sequence and cached measurement live in the client process.
A committed InnoDB row belongs to the database and survives that client. A cache
may represent a durable fact, but only a declared synchronization/recovery policy
connects the two. Connection establishment and command submission establish no
commit. Report acceptance according to the promised boundary, not the first
successful callback encountered.

## 2. Review (O2, O3)

Chaining appends commands to the returned sequence. An asynchronous call inside a
callback creates another sequence queued behind the current one. If commit is
already chained, rollback queued from the insert error callback does not jump in
front of it. Command-level SQL errors can leave the connection usable and allow
the remaining sequence to advance. Enqueue a dependent commit or rollback only
after observing the required result, with transaction ownership preventing
unrelated work from interleaving on that connection.

`affectedRows` and `fieldCount` instead read metadata already available from the
completed operation. Called inside its callback, they observe that operation
before later SQL advances. These callback-shaped metadata reads are not arbitrary
blocking database queries. Recovery also needs a way to resolve an uncertain write;
reconnecting alone cannot decide whether replay would duplicate it.

## 3. Lab (O1, O2)

**Equipped database lab.** In addition to the common installed SNode.C setup, install
MariaDB server and client tools. On Debian/Ubuntu the packages are `mariadb-server`
and `mariadb-client`; the lab finds `mariadbd`, `mariadb-install-db` and `mariadb`.
Run as an ordinary user. No existing service, administrative password or network
listener is used. Missing tools fail explicitly rather than silently skipping.

```sh
cmake --build build/labs --target ch24-lab
ctest --test-dir build/labs -R '^exercise-ch24-durable$' --output-on-failure -V
```

CMake derives the fixture from the unchanged `MariaDB-Minimal/main.cpp`. Only the
private connection details and selected SQL statement vary; its command chain,
metadata and result/error callbacks remain the printed example. The generated
program refuses to run without `BOOK_DB_SOCKET` and `BOOK_DB_SQL`. The runner sets
these only around its child process, using its own newly initialized database.

`database.py` initializes a private temporary data directory, starts MariaDB with
networking disabled, waits for a successful query and creates the `book` schema
and InnoDB `measurements` table. The Unix socket lives inside the private directory.
The fresh server's root account has no password; directory isolation and disabled
networking confine this fixture. It is not a deployment credential policy.

The observer confirms autocommit and InnoDB flush-on-commit are enabled, and the
initial row count is zero. The canonical insert must report one affected row and
`temperature = 23.5`. After stopping that client, an independent MariaDB CLI query
must return the same row. Restart the generated client with `DO 0` instead of the
insert: its unchanged query must read the existing row, and the independent count
must remain one. The write was committed by the server's autocommit mode; the test
does not exercise the chapter's explicit transaction sketch or crash recovery.

Before initialization the lab requires at least 512 MiB free temporary space.
Its fixture uses an 8 MiB InnoDB redo log and a 32 MiB buffer pool. Setup, readiness,
queries and shutdown have time bounds. The private SQL `SHUTDOWN` command stops the
server before directory removal; if shutdown fails, live state is retained and
its path reported. No schema, user or file in an existing database is modified.

## 4. Lab (O2, O3)

```sh
ctest --test-dir build/labs -R '^exercise-ch24-error$' --output-on-failure -V
```

A new disposable database starts empty. Replace only the fixture statement with
an insert into `book.no_such_table`. Expect error 1146, then `measurement query
complete` from the still-chained query. The independent observer must see zero
rows. This tests a command-level SQL error with a usable connection, not a dropped
connection, rollback or a transaction that was already committed.

Without database server tools, the local alternative is the public gateway outage
observation (`exercise-ch23-unavailable-output`). It shows accepted in-memory state
and restart reset, but supplies no durable-state evidence and cannot substitute
for the equipped database exit check. To run local alternatives without the equipped
labs, use `ctest --test-dir build/labs -LE equipped --output-on-failure`.

## 5. Design (O1, O3)

One service owns the database client and transaction lifetime. The input handler
validates a measurement; a domain operation assigns its stable identity. If success
promises durability, send that success only after the required commit callback.
Choose a finite pending-work limit and reject, coalesce or apply upstream feedback
at that limit; event integration does not supply an unlimited safe queue.

Use an idempotency key and a queryable outcome to resolve an interrupted write
before replay. Serialize work sharing a transaction connection; decide commit or
rollback from observed results. Stop accepting new work during shutdown, then
finish or report pending operations according to the contract. A healthy HTTP
handler can report database degradation truthfully without claiming storage success.
The local labs do not implement a production transaction/retry service.
