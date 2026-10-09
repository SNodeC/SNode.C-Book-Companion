# Chapter 1 — solutions and discussion

## 1. Review (O1)

An input callback knows its own protocol, not the order of all accepted inputs.
Independent counters can collide or disagree. Both callbacks should parse a value
and pass it to one shared model; that model assigns the acceptance sequence.
Protocol framing belongs to the input, while ordering shared state belongs to the
application. This distinction remains useful even when all callbacks run on one
thread: the conflict is competing policy, not merely simultaneous execution.

## 2. Review (O2)

Asio's write operation still refers to the session's byte array until completion.
Starting another read into that array early could overwrite bytes being sent.
The completion handler holds a shared session owner, keeping both socket and
buffer alive. EchoPair's `sendToPeer(...)` copies into framework-managed output;
its stack buffer can disappear when the callback returns. Neither implementation
requires one read to correspond to one sender write.

## 3. Lab (O2)

After Chapter 2 and the common configuration in [the exercise guide](../README.md):

```sh
cmake --build build/labs --target ch01-lab
ctest --test-dir build/labs -R '^exercise-ch01$' --output-on-failure -V
```

`ch01-lab` builds EchoPair's `echoserver` and standalone `asio-echo`. Read the two
implementations using the side-by-side table in Chapter 1. `solution.py` starts
each on a different loopback port and sends the same 20,480-byte payload, including
NUL and non-ASCII bytes. The payload exceeds both 4,096-byte receive buffers. It
checks a short first exchange, then the remaining bytes, and opens another session
after EOF. Expect two PASS lines reporting exact equality and a working later
connection. Any mismatch, early EOF, timeout, or failed shutdown fails the lab.

The received byte stream is the contract. TCP may split or combine writes into
reads; the peer accumulates bytes until the expected length is reached. Equal
bytes do not establish application message boundaries or relative performance.
The test deliberately has no throughput claim. Read completion starts an Asio
write; write completion permits buffer reuse. EchoPair instead submits bytes to
the framework's output queue.

## 4. Lab (O2)

After Chapter 2, use the same build target and run just this second lab:

```sh
ctest --test-dir build/labs -R '^exercise-ch01-independent-peers$' --output-on-failure -V
```

`independent-peers.py` keeps two connections open to each compiled server. One
sends nothing while the other sends `other\x00peer`; that active connection then
sends `still here` after the idle peer closes. Expect unchanged bytes for both
exchanges and one PASS line per server. A blocking wait on the idle peer would
time out the active exchange. Independent session state allows one connection
to end without ending the listener or the other connection. This checks progress
and byte equality, not a throughput or resource-exhaustion claim.

## 5. Design (O3)

For the Linux gateway, SNode.C is a reasonable choice when shared HTTP/MQTT roles,
configuration, and diagnostics justify learning its layered model. Keep callbacks
short because the process has one event loop; plan a process boundary for work that
requires an independent loop. Its small ecosystem also means budgeting source
reading and integration work.

For a native Windows utility, choose Asio from these two candidates: its documented
platform coverage includes Windows, whereas the SNode.C setup taught here targets
Linux. A short TCP-only program may also benefit from Asio's narrower dependency.
Neither result follows from counting lines, and different deployment requirements
can change the gateway decision. No market-share estimate is needed for either
argument.
