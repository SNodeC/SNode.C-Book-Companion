# Appendix A — solutions and discussion

## 1. Review (O1)

Begin with `companion/examples/EchoPair/echoserver.cpp` and the public
`net/in/stream/legacy/SocketServer.h` it includes. In the framework source,
`src/net/in/stream/legacy/SocketServer.h` aliases the IPv4 stream server with a
legacy acceptor and the selected configuration. Its template still takes the
application factory. Follow `src/net/in/stream/SocketServer.h` to the generic
`src/core/socket/stream/SocketServer.h`: the public listen operation creates its
flow and calls `startFlow(...)`. Configuration and endpoint callbacks remain
shared across those activations.

Back in the companion, `EchoSocketContext.h` declares the factory;
`EchoServerSocketContextFactory::create(...)` in `EchoSocketContext.cpp` creates an
`EchoSocketContext` with the server role. `EchoSocketContext.cpp` supplies receive
and reflection behavior. The alias selects family, transport and connection
machinery; it does not decide the echo protocol or give the context global
application ownership. The accepted connection owns its context. Distinguish
endpoint configuration, the listening flow and each later peer connection while
following the files.

## 2. Review (O3)

An option in the configuration tree is a value, not an update mechanism for every
object that once read it. State when the value is captured and which consumer
reads it again. A connection may intentionally keep a policy snapshot until it
ends; a listener might require an explicit controlled restart. Define validation,
failure and rollback behavior before promising an immediate transition.

`SNodeC::reconfigure()` reparses registered configuration. It does not recreate
active connection policy, restart listeners or repeat logging bootstrap.
Parsing/lifecycle regressions and a scenario with an already-active consumer
answer different questions. Avoid adding a second policy owner to compensate for
an unspecified lifetime.

## 3. Lab (O1, O2)

Use [the common installed environment](../README.md), then:

```sh
cmake --build ../build/labs --target appendix-a-lab
ctest --test-dir ../build/labs -R '^exercise-appendix-a-source-consumer$' --output-on-failure -V
```

The registered lab reuses the public external-consumer experiment. It configures
and builds the canonical EchoPair in a fresh temporary directory, asserts that
`snodec_DIR` matches the enclosing build’s selected package, then exchanges `environment-ready`
with an independent peer. Expect package-selection and byte-equality PASS lines.
The private server is stopped and its temporary files are removed on exit.
No framework modifications, broker, database or radio hardware are needed.

Before running it, complete this source-reading record using the framework source
prepared for the book and the companion files. From the framework source root,
these bounded searches provide entry points; read the surrounding declarations
and implementation, not just the matching lines:

```sh
rg -n 'using SocketServer|ConfigSocketServer' src/net/in/stream/legacy/SocketServer.h
rg -n 'listen\(|Super::listen' src/net/in/stream/SocketServer.h
rg -n 'listen\(|startFlow|make_shared' src/core/socket/stream/SocketServer.h
```

| Question | Expected source record |
| --- | --- |
| Which installed component does the application request and link? | `net-in-stream-legacy` and `snodec::net-in-stream-legacy` in EchoPair's CMake file |
| Which installed package was actually chosen? | The test's observed `snodec_DIR`, matching the enclosing build |
| Where are the family and connection variant selected? | Public legacy IPv4 alias, then the IPv4 stream wrapper |
| Where is an activation flow started? | Generic stream server's `listen(...)` and controller `startFlow(...)` path |
| Which file constructs protocol behavior? | Companion `EchoSocketContext.h` declaration and `EchoSocketContext.cpp` factory implementation |
| Which file reflects input? | Companion `EchoSocketContext.cpp`, `onReceivedFromPeer()` |

The source trace explains ownership and selection. The runtime exchange observes
one installed consumer's behavior; it does not by itself establish flow lifetime,
TLS authentication, or that every installed component works. The source checkout
and selected installation must correspond before attributing observed behavior to
the implementation being read.

## 4. Lab (O2, O3)

```sh
cmake --build ../build/labs --target appendix-a-lab
ctest --test-dir ../build/labs -R '^exercise-appendix-a-carrier-extension$' --output-on-failure -V
```

This reuses the existing carrier experiment in `../ch12/CMakeLists.txt` and the
independent peer driver in `../ch10/protocol.py`. CMake applies the worked edits to
the canonical line-server entry point in the build directory:

| Selection | IPv4 consumer | Unix-domain extension |
| --- | --- | --- |
| Header | `net/in/stream/legacy/SocketServer.h` | `net/un/stream/legacy/SocketServer.h` |
| Alias namespace | `net::in::stream::legacy` | `net::un::stream::legacy` |
| Default listen argument | Port 8090 | A Unix socket pathname |
| Exported component | `snodec::net-in-stream-legacy` | `snodec::net-un-stream-legacy` |

Inspect the generated `unix-main.cpp` under `../build/labs/companion/exercises/ch12/`.
Both targets compile the same `LineCommandServerContext.cpp` and include the same
factory; there is no copied parser or new framework layer. The canonical entry
point is a CMake reconfiguration dependency. The runtime fixture overrides the
endpoint with a private loopback port or temporary pathname.

Expect `READY`, then the same reconstructed `PONG`, `OK`, unknown-command error
and final `PONG` under every two-piece split and a coalesced send. Empty/CRLF
inputs are included; a lone `PI` must remain quiet until completed. `QUIT` closes
the peer. The driver compares the reply sequences across carriers and checks
server-owned Unix-path removal after shutdown. Expect two framing PASS lines and
one transfer/checkpoint PASS line. Application writes do not control kernel read
callback boundaries.

This is a bounded application-consumer extension using installed public
components, not a new framework implementation. It preserves the protocol while
changing endpoint selection. It does not establish Unix access policy or network
authentication; those deployment obligations still differ.

## 5. Design (O1, O3)

Add an explicitly named producer sample field to the domain value; keep the
model's local acceptance sequence separately owned. Update CSV parsing and JSON
encoding/decoding with a specified missing-field and compatibility policy. Preserve
validation before acceptance, sequence assignment by the model and observer
subscription lifetime. Decide whether producer identity must accompany the sample
number: two producers may legitimately use the same number.

Test conflicting producer numbers against one monotonic gateway sequence,
malformed records without state changes, both representations, HTTP status and
SSE observations. MQTT needs independent topic/payload observations if its wire
contract changes. A reconnect snapshot is not a durable history, and a process
restart still resets the in-memory acceptance sequence unless persistence is
separately designed.

Adding only another carrier can preserve the value, acceptance, codec and observer
contracts. Change the public carrier/header/component and endpoint setup, then
repeat the same framing observations. Factory construction passes the same model
reference into private contexts. Keeping either extension application-local avoids
teaching a generic transport about one product's measurement schema.
