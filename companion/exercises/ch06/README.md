# Chapter 6 — solutions and discussion

## 1. Review (O1)

`RUNNING` describes the runtime's lifecycle phase. `SUCCESS` is a result returned
for an iteration; by itself it does not establish that a callback executed. In the
public stepping path described in the text, initialized state does not provide
the same dispatch contract as `start()`. Observe a callback effect or a byte
exchange to establish progress, and keep that evidence separate from return status.
The deferred-work lab checks both running state and its trace.

## 2. Review (O2)

The receive callback occupies the same event-loop thread that advances other
readers, queued writes, deferred activation, timers, timeout checks, and cleanup.
A sleep delays its return. A timer can become due during that interval, but its
callback cannot preempt the sleeping callback. Schedule the retry and return, or
use a deliberately supported asynchronous/process boundary for blocking work.
A worker holding a shared pointer gains lifetime, not permission to call loop-owned
connection or controller methods concurrently.

## 3. Lab (O1, O2)

After the common configuration in [the exercise guide](../README.md):

```sh
cmake --build build/labs --target ch06-lab
ctest --test-dir build/labs -R '^exercise-ch06-deferred-work$' --output-on-failure -V
```

`deferred-work.cpp` uses the installed public `SNodeC` and `EventReceiver` APIs.
It queues a callback and first requires an empty trace. The callback checks
`RUNNING`, marks itself active, appends 1, queues a child, appends 2, and clears
its active flag before returning. The child records whether the first callback
has returned, appends 3, and requests shutdown. After `start()` returns, the
program requires trace 1,2,3 and the recorded non-overlap condition.

Expect one PASS line naming the empty initial trace, running dispatch, and order.
CTest supplies an isolated configuration directory and a ten-second outer timeout.
The explicit result checks remain active in release builds. The local captured
state outlives `start()` and shutdown. This verifies deferred execution at the
public callback interface; it specifies neither a maximum scheduling latency nor
fairness under load. It also does not claim that two `span()` calls on one already
published receiver represent two independent callbacks.

## 4. Lab (O3): Part II checkpoint

```sh
ctest --test-dir build/labs -R '^exercise-ch06-model-checkpoint$' --output-on-failure -V
```

The target reuses `companion/exercises/ch32/model-ownership.cpp` and compiles the
canonical MiniGateway `MeasurementModel.cpp`; the later chapter is not required
to understand this experiment. The model offers four operations used here:

| Operation | What the experiment observes |
| --- | --- |
| `subscribe(callback)` | Retain a token for one observer; its callback records accepted sequences. |
| `accept(measurement)` | Replace the producer-supplied sequence with the next local one, store the value, notify listeners synchronously, and return it. |
| `unsubscribe(token)` | Remove that subscription between acceptance calls. |
| `current()` | Return the model's latest accepted state. |

Create two observers, then accept inputs carrying sequences 900 and 2. Both
observers see 1,2. Remove the first subscription before accepting input carrying
sequence 1. The second observer now sees 1,2,3; the first remains at 1,2. The
returned third measurement and current state must both have sequence 3. Remove
the second subscription before the captured vectors leave scope. Expect one PASS
line naming those input, accepted, and observer sequences.

This is a model and lifetime experiment, not an event-loop scheduling test. In a
gateway, short protocol callbacks will parse and validate input, then call this
same shared owner on the event-loop thread. The lab uses well-formed model inputs;
`accept` is not a substitute for protocol parsing or validation. Unsubscription
here happens between calls, not while a listener list is being traversed. Do not
infer that arbitrary listener removal or recursive acceptance during notification
is supported. No transport teardown, persistent storage, or cross-process sequence
is established by this run.

## 5. Design (O1, O2, O3)

Keep acceptance and its local ordering in the gateway model. An observer may hand
an already accepted value to a bounded queue or separate persistence process;
it must not block until a database write completes. Define whether overflow
rejects, drops, or delays further input and expose that outcome. Persistence
completion records durability of a specific accepted value, not a replacement
acceptance sequence.

A separate process can own the blocking database client and report completion over
a protocol consumed by the loop. A worker-thread alternative needs a documented,
supported handoff back to the loop; a pointer alone is insufficient, and this
experiment does not supply a general cross-thread dispatcher. Retain completion
state until its callback finishes or cancellation is acknowledged. During shutdown,
stop new handoffs, bound draining or abandonment, remove subscriptions before
captured observers die, and distinguish accepted data from durably stored data.
