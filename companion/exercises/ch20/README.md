# Chapter 20 — solutions and discussion

## 1. Review (O1)

The HTTP upgrade name `websocket` selects a socket-context upgrade factory. The
subprotocol name `echo` selects application message behavior within that carrier.
Both names must resolve on the relevant role side. Upgrade keeps the underlying
connection, peer identity, TLS state where present and runtime lifecycle; it
changes the protocol context interpreting subsequent bytes. A missing upgrade
factory and a missing subprotocol factory are different selection failures.

## 2. Review (O2, O3)

Text and binary messages can contain identical bytes with different meaning.
Counted byte ranges preserve embedded NUL, and the typed send overload preserves
the opcode. Echo reconstructs a message and need not repeat its original frame
boundaries. A finite frame limit alone cannot bound a many-frame message;
accumulated bytes and fragment count need distinct bounds. Resource rejection
uses close 1009, while content validation and authorization remain application
responsibilities. Receive-policy snapshots do not set output fragmentation policy.

## 3. Lab (O1, O2)

Use [the common lab configuration](../README.md), then:

```sh
cmake --build build/labs --target ch20-lab
ctest --test-dir build/labs -R '^exercise-ch20-negotiation$' --output-on-failure -V
```

CMake derives lab entry points from `HttpUpgrade-Server` and `HttpUpgrade-Client`:
it adds the relevant echo-factory header and an explicit selector `link("echo", ...)`
call on each role side. It compiles the canonical echo subprotocol sources without
editing them. This exercises the linked-factory path described in the chapter;
no installation into the framework prefix is required. The original example
executables still support the separately documented dynamic module deployment.

The canonical client must receive `hello` and close. An independent request then
asks for `unavailable-lab-protocol`. Expect no accepted upgrade and no additional
echo attachment; the fixture prints the returned status (404 in the local run).
It does not assume every subprotocol rejection must have that same status.
Success of an HTTP request alone is insufficient evidence of a selected subprotocol.

## 4. Lab (O1, O2, O3): Part VII checkpoint

```sh
ctest --test-dir build/labs -R '^exercise-ch20-part-checkpoint$' --output-on-failure -V
```

The checkpoint first reuses the public SSE observer solution. Two observers see
the same initial snapshot and first accepted POST result. After one disconnects,
a second POST must advance the sequence and reach the remaining observer. Each
POST's status is 200, and its JSON equals the event JSON and ID. This example has
no separate `/status` resource; POST results and stream snapshots expose its
accepted measurement. These wire observations do not measure memory reclamation.
The explicit unsubscribe path explains the independent observer lifetimes.

A separate WebSocket connection then checks HTTP 101, the selected `echo` name and
the accept-key response, followed by exact message types and bytes: text, binary
with NUL/non-UTF8 bytes, empty text and binary, sequential messages and a longer
binary message. Fragmented text and binary each include an interleaved ping whose
pong must match. Finally, close code 1000 is returned and the stream ends.
`wire.py` holds this independent observer once; the repository lifetime check
imports the same assertions for its dynamically deployed examples.

The checkpoint distinguishes shared accepted SSE state from WebSocket's echo
contract. Echo is not another measurement model, and neither a selected protocol
nor restored connectivity establishes delivery of earlier state changes. The
fixtures use local peers, isolated configuration and bounded waits. They do not
exercise all invalid-frame/resource-limit cases, authentication or deployment TLS.

## 5. Design (O1, O3)

SSE plus POST separates one-way accepted-state observation from explicit commands.
A WebSocket subprotocol fits an ongoing bidirectional message conversation, but
needs a message schema, validation, correlation and recovery contract. State who
owns accepted data in either design; observers must not become competing stores.

Choose finite frame, assembled-message and fragment limits for untrusted input,
plus separate output bounds and slow-peer policy. If commands may be replayed,
define idempotency or operation identifiers and acknowledgment semantics. For SSE,
bound history and define a gap response for expired event IDs. Select linked or
dynamic factories according to deployment needs, retaining the same role/name
contract, and keep TLS identity and application authorization explicit.
