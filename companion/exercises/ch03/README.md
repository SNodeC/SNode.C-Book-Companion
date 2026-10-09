# Chapter 3 — solutions and discussion

## 1. Review (O1)

The named server handle supplies endpoint configuration and registers a listener.
An accepted connection asks the factory for a context. The factory allocates the
application context and hands it to the framework-managed connection lifecycle;
application code must not delete it. Each context holds one peer's behavior. The
handle is therefore neither the peer connection nor the echo protocol object.

## 2. Review (O1)

The client initiates the conversation in `onConnected()`. A newly connected
server waits for input. After that initial send, the same `onReceivedFromPeer()`
reflects bytes on both sides. If neither side initiated, both could wait forever;
if both initiated, two streams of reflected data would begin. Endpoint direction
and the decision to initiate a protocol exchange are related but distinct choices.

## 3. Lab (O2)

After the common configuration in [the exercise guide](../README.md):

```sh
cmake --build build/labs --target ch03-lab
ctest --test-dir build/labs -R '^exercise-ch03$' --output-on-failure -V
```

For a manual run, use two terminals:

```sh
./build/labs/companion/examples/EchoPair/echoserver --log-level=5
./build/labs/companion/exercises/ch03/greeting-client --log-level=5
```

Stop both with Ctrl-C. The echo traffic now contains `Learning by echo`. The
solution subclasses the printed context and overrides only `onConnected()`; its
factory creates that context. The inherited receive callback still reflects bytes.
This leaves the canonical printed EchoPair sources intact. In a private playground
copy, changing the original greeting directly is equivalent for this experiment.

The automated solution first observes the changed greeting at the actual server,
then runs the client against a controlled peer. That peer checks the exact greeting
and sends a 5,000-byte binary reply, which must return unchanged. Expect three PASS
lines. This separates the initiation callback from reflection and avoids relying
only on fast, repetitive ping-pong logs.

### Part I checkpoint: measurement transport

The same Lab 3 command also opens two bounded peers to EchoPair. The first sends
`sensor-a,21.5` and `sensor-a,not-a-number`, each followed by a newline; the second
sends `sensor-b,18.0`. Each receives exactly its own bytes. After closing the
second peer, the first sends again and must still receive identical bytes. The
checkpoint PASS line names both independence and reflection of the invalid value.

These observations establish a byte-transport baseline for MiniGateway. The echo
context neither parses a numeric measurement nor accepts domain state: even the
invalid value returns unchanged. Later milestones will add framing, validation,
and one shared accepted model. No acceptance sequence or stored measurement is
created here. Explain that limit before treating the transport run as a gateway.

## 4. Lab (O3)

Use the same build target, then run:

```sh
ctest --test-dir build/labs -R '^exercise-ch03-occupied-port$' --output-on-failure -V
```

`occupied-port.py` first establishes a connection to EchoPair. It starts another
copy with the same address and port and expects `Address already in use` in that
process's endpoint diagnostic. The established connection must still reflect
`original owner` unchanged. Expect one PASS line covering both observations.
For manual repetition, run the two server commands in separate terminals on the
same port. The failure occurs before a second server can create a peer context;
changing greeting or reflection code cannot repair that listener conflict.

## 5. Design (O3)

If no connection is established, inspect the connect/listen state and the selected
address and port first. The greeting callback cannot run before the context is
attached to a ready connection. Confirm that the expected process owns the port;
a second process failing to bind is an endpoint setup problem.

If a connection works but echoed bytes change, inspect the receive count and the
buffer length passed to `sendToPeer(...)`. Treat embedded NUL as data; a C-string
operation may truncate it. If the greeting alone is wrong, inspect the client
`onConnected()` instead. These are different observations with different owners.
