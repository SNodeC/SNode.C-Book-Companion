# Chapter 19 — solutions and discussion

## 1. Review (O1)

The publisher stores a listener whose shared response pointer keeps the facade
alive. The HTTP context's disconnect callback captures the publisher and one list
iterator, then removes that listener. Removing it releases the response reference.
The callback does not capture another owning response pointer. The publisher
outlives the event loop, and list insertion/removal does not invalidate other
subscription iterators. Publication does not mutate that list.

Cleanup must follow disconnect, even if the source is quiet; waiting for the next
measurement would retain obsolete responses indefinitely. A silent network failure
still needs detection by the transport or timeout policy. An SSE blank line ends a
record, and EventSource dispatches its parsed fields as a typed `MessageEvent`.

## 2. Review (O1)

A blank line terminates an SSE record. The parser accumulates fields before
emitting a `MessageEvent`: `event` selects its type, `id` supplies its event ID,
and `data` supplies the payload. An ID can be remembered for reconnect, but it
neither acknowledges delivery nor makes the server retain history. The example
uses `measurement` events whose JSON sequence matches the event ID.

## 3. Lab (O2)

After the common configuration in [the exercise guide](../README.md):

```sh
cmake --build build/labs --target ch19-lab
ctest --test-dir build/labs -R '^exercise-ch19$' --output-on-failure -V
```

The target builds both SSE programs. `solution.py` uses a controlled HTTP peer so
it can compare exact JSON and event IDs. It rejects the parameterized Accept value
with 406, reads the initial measurement, and checks two POST results against the
next events. It disconnects and opens a new stream with the older `Last-Event-ID`.
The first event is the current measurement, not the intervening history. Expect
one PASS line describing all three checks.

For manual observation, run the server and the curl commands printed in the
chapter. The initial server sequence is 1; the two simulations produce 2 and 3.
These observations check response behavior and reconnect output. They do not
measure retained allocations or establish acknowledgement of earlier events.
The explicit disconnect-to-unsubscribe path explains idle cleanup.

## 4. Lab (O2)

Use the same build target, then run:

```sh
ctest --test-dir build/labs -R '^exercise-ch19-observers$' --output-on-failure -V
```

`observers.py` opens two streams and consumes each initial snapshot. One simulation
must produce identical JSON and IDs for both. It closes one stream, simulates
again, and requires the remaining stream to receive the next accepted sequence.
Expect one PASS line. For a manual run, use two `curl -N` observers and stop one
with Ctrl-C before the second POST. Closing an observation path does not own the
other observer's lifetime or the shared measurement. The wire observations do
not measure memory reclamation; the disconnect-to-unsubscribe code explains that
separate ownership fact.

## 5. Design (O3)

One bounded policy is to retain at most 600 accepted events for at most ten minutes,
whichever limit is reached first. Apply a finite per-observer output queue and
disconnect a peer that cannot keep up; do not block the model's acceptance path.
On reconnect, replay only if the supplied ID is still in that bounded history.
Otherwise signal a gap and provide a current snapshot so the dashboard can restart
its view. Define that gap contract before implementing it.

Show stream state and the time/ID of the last accepted update separately. A healthy
but quiet stream should not look like a known disconnection; an old displayed
measurement should remain visibly old. Event IDs identify continuity positions,
not proof that the user saw every update. Other bounds can be valid if justified
by source rate, memory budget, and the cost of losing intermediate samples.
