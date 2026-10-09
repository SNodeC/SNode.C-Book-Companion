# Chapter 32 — solutions and discussion

## 1. Review (O1)

An SSE event ID describes an already accepted measurement; letting it assign order
would make one observer authoritative over other outputs. A producer's number
orders that producer's samples, not all gateway inputs. Keep a distinct
`sensorSampleNumber` together with sensor identity if provenance matters. The model
then assigns its own acceptance sequence after parsing, preserving both facts
without making them compete. In the supplied model that sequence is process-local.

## 2. Review (O3)

Two flow handles can represent independent attempts and cancellation under one
endpoint policy. Use separate endpoint roles when destinations, credentials,
configuration identity, or operational ownership differ. Counting connections
alone does not settle this choice: ask which settings and lifetime decisions
must be independently owned.

## 3. Lab (O2)

After the common configuration in [the exercise guide](../README.md):

```sh
cmake --build build/labs --target ch32-lab
ctest --test-dir build/labs -R '^exercise-ch32$' --output-on-failure -V
```

`model-ownership.cpp` compiles and uses the same `MeasurementModel.cpp` printed in
Chapter 30. It creates two observers, accepts input with sequences 900 and 2,
removes the first observer, then accepts input with sequence 1. Expect model order
1, 2, 3; the detached observer sees only 1, 2, and the remaining observer sees all
three. The returned and current measurement must both have sequence 3. Explicit
checks remain active even in a release build. The experiment removes the second
subscription before the captured vectors leave scope.

This isolates acceptance and observer ownership from transport. It does not test
HTTP teardown or persistence; those are different boundaries.

## 4. Lab (O1, O2)

Use the same build target, then run:

```sh
ctest --test-dir build/labs -R '^exercise-ch32-model-instances$' --output-on-failure -V
```

`model-instances.cpp` compiles the canonical model. Two references representing
input paths share one model and receive sequences 1 and 2. Two separate model
instances each receive sequence 1. Expect one PASS line describing both results.
Sharing a class definition does not share its state: the owner must be the same
instance if acceptance order is to be common. The lab has no transport dependency
and makes no claim about interprocess ordering or persistence.

**Part XI checkpoint.** Build the shared targets and run the integrated set:

```sh
cmake --build build/labs --target part-xi-checkpoint
ctest --test-dir build/labs -R '^exercise-ch(28|29|30)($|-)' --output-on-failure -V
```

The six tests reuse the public MiniGateway, extended-input, JSON-validation and
model experiments. No extra application or checkpoint implementation is needed.
The [extended-input solution](../ch31/README.md) specifies the observations:
HTTP and Unix input share one acceptance order while MQTT is unavailable;
malformed CSV changes neither state nor that order; an observer can disconnect
while the other continues; reconnect gives the current state, not missed-event
replay; restart resets the in-memory sequence. Contrast these observations with
the independent model instances tested above. Record the expected and observed
results, then use the decision tables for the following design problem. Actual
MQTT delivery remains a separate equipped subscriber observation described in the
extended-input solution.

## 5. Design (O3)

Use a separate collector process for privileged device access and independent
restarts. Leave HTTP/MQTT and the shared model in the unprivileged gateway. A
Unix-domain endpoint is a plausible local contract: select a filesystem path,
restrict ownership/permissions, and define bounded newline-delimited records or
length-prefixed frames. Validate the record before calling the model.

Specify what happens if either process restarts: reconnect with bounded retry,
choose whether the collector buffers or drops samples, bound any buffer, and carry
producer identity/sample identity if replay needs deduplication. A disconnected
collector should produce an observable degraded input state, not reset other
roles. Collector diagnostics own device errors; gateway diagnostics own validation
and acceptance; the service manager owns restart policy. The additional process
costs deployment and recovery work, but here the privilege and restart requirements
justify it. If those requirements disappear, keeping one process may be simpler.
