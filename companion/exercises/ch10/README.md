# Chapter 10 — solutions and discussion

## 1. Review (O1)

The two bytes have moved from the connection into the context's receive buffer.
The returned count accounts for that consumption, although the newline needed to
complete `PING` has not arrived. A completed-command counter is a separate protocol
observation. Queuing a reply would still not establish peer receipt or application
processing. Context attachment and detachment define the parser's lifetime; they
need not coincide with the entire connection lifetime during a context switch.

## 2. Review (O3)

An inactivity timeout may keep being refreshed without a command ever completing.
A command deadline needs a policy tied to protocol progress. Queue admission failure
requires an explicit choice: defer within a bounded application policy, reject the
operation, or close according to protocol semantics. Do not announce success for
bytes that were not admitted or defeat the limit with an unbounded shadow queue.
Shared connection machinery still owns transport buffering and descriptor lifetime.

## 3. Lab (O1, O2)

Use [the common configuration](../README.md), then:

```sh
cmake --build build/labs --target ch10-lab
ctest --test-dir build/labs -R '^exercise-ch10-framing$' --output-on-failure -V
```

The fixture runs the unchanged `LineProtocol-Server` on loopback with a temporary
configuration and bounded process lifetime. On fresh connections it sends
`PING\nSTATUS\nBOGUS\n\nPING\r\n` at every possible two-piece split, including one
coalesced send. Every case must yield exactly `PONG\nOK\nERR unknown command\nPONG\n`,
then close after `QUIT`. A separate case sends only `PI`, checks a bounded quiet
interval, and then supplies `NG\nSTATUS\n`; expect `PONG\nOK\n`. The PASS line reports
the number of tested segmentations and the command/closure observations.

Writes do not force receive-callback boundaries. The cases vary application writes
and compare visible results; they do not claim to exercise every possible network
schedule. The quiet interval catches an early response in this run, while the code
review explains the delimiter invariant. The empty line produces no response;
CRLF removes the trailing carriage return before command dispatch. The example
models command framing, not MiniGateway CSV validation or accepted state.

## 4. Lab (O2)

```sh
ctest --test-dir build/labs -R '^exercise-ch10-limits$' --output-on-failure -V
```

Expect unknown-command replies for 4096 `x` bytes plus newline, and for 4095 `x`
bytes plus CRLF. Both connections must still answer a later `PING`. For an overlong
case, send 4096 non-delimiter bytes, observe a quiet interval, then send the 4097th
byte either alone or with a newline. The runnable server queues `ERR line too long`
and immediately closes before interpreting that command. Immediate closure need
not flush queued output: require closure, allowing only a prefix of that diagnostic
(including no bytes), never an unknown-command response. The abridged printed
context closes without that diagnostic; both preserve the same admission boundary.

The limit counts bytes preceding newline, including an optional carriage return.
Checking only the unfinished suffix would wrongly admit an overlong complete line;
checking the delimiter position protects both forms. Expect a PASS naming the
4096/4097 boundary. These tests cover framing length, not output-queue saturation
or a deadline policy; those remain separate observations.

## 5. Design (O1, O3)

The context owns its unfinished record, parser phase and completed-command count.
It can copy an immutable parsing limit at construction. One application model owns
accepted measurements, reached through an explicit dependency supplied by the
factory. A completed line still requires parsing and validation before acceptance;
producer sequence numbers do not become the accepted model's sequence owner.

Define a command deadline separately from inactivity and a bounded response to
output admission failure. Connection queues remain in the framework. Teardown
releases parser state and any subscriptions before captured application state dies.
A model reference is valid only while the application-owned model outlives every
context and observer using it. The lab intentionally stops before implementing
this later measurement adapter.
