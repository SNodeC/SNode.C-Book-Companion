# Chapter 8 — solutions and discussion

## 1. Review (O1)

Each explicit connect returns its own controller, but both flows use the endpoint's
shared configuration. `terminateFlow()` ends the selected operation's pending
attempts/recovery. Dropping a shared handle releases one reference; it is not a
termination request. An established connection has a separate close operation.
Destruction/unregistration of the shared endpoint configuration is another event.
Use separately configured endpoints for independent destinations, rather than
assuming address-taking overloads create immutable per-flow configuration.

`setOnFlowTerminated` reports termination, while `setOnFlowCompleted` follows final
controller release. Retaining a controller can delay completion. Capture stable
identifiers by value rather than creating a callback/owner reference cycle.

## 2. Review (O2)

A failed bind belongs to activation status and may produce no connection. A TLS
handshake failure requires transport/handshake observations; `onConnect` and
`onConnected` do not denote the same readiness stage. At final disconnect, copy
addresses, counters, duration, or identifiers while the borrowed connection pointer
is valid. Do not retain it for later reporting, and do not call the former context:
its detachment/destruction can precede the outer disconnect callback. Application
protocol responses belong in the context rather than in these diagnostic hooks.

## 3. Lab (O3)

After [the common configuration](../README.md):

```sh
cmake --build build/labs --target ch08-lab
ctest --test-dir build/labs -R '^exercise-ch08-independent-peers$' --output-on-failure -V
```

This deliberately reuses the existing independent-peer fixture and canonical
EchoPair. The active peer sends `other`, a NUL byte, and `peer`, then receives all
ten bytes unchanged while a second peer is idle. After that idle peer closes, the
first peer sends and receives `still here`. Expect a PASS covering both exchanges.

The observations support independent progress and closure of these two peer
relationships. They do not exercise stopping the listener, partial-record parsing,
reconnection, or shared model ordering. A future parser needs separate receive
buffers even though every context uses the same factory; only accepted application
state should be deliberately shared.

## 4. Lab (O2)

```sh
ctest --test-dir build/labs -R '^exercise-ch08-occupied-endpoint$' --output-on-failure -V
```

The existing occupied-port fixture starts the canonical server and establishes a
peer. A second server then attempts the same endpoint. Expect an `Address already
in use` diagnostic, followed by unchanged `original owner` bytes from the first
server. The test keeps the first listener alive while observing the second failure;
it does not mistake a failed activation for a broken echo protocol.

Both processes use isolated configuration and bounded shutdown through the common
harness. The local diagnostic is part of this Linux fixture. No claim is made about
successful automatic recovery after the original owner later exits.

## 5. Design (O1, O2, O3)

Give the two destinations separate named endpoint configurations and retain the
flow handles needed to control their recovery independently. The role/flow machinery
owns retry and reconnect policy. Each peer episode owns its connection counters
and context; each context owns its unfinished measurement record. A new episode
must not inherit an unrelated peer's half-read record.

Pass one application model through the factories, with a lifetime that covers all
contexts and observers that use it. Parsing and validation precede acceptance;
reconnection does not create another global sequence owner. Copy diagnostics at
disconnect into independently owned values and release subscriptions before their
captured state dies. A protocol upgrade may replace a context without replacing
the connection, so count attempts, connections, and contexts separately.
