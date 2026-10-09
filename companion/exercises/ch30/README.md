# Chapter 30 — solutions and discussion

## 1. Review (O1)

`MiniGatewayMqtt` decodes the incoming measurement using `MeasurementJsonCodec`,
then calls the shared `MeasurementModel::accept(...)`. The model overwrites the
incoming sequence with its next local value, stores the measurement, and notifies
subscribers. SSE writes that accepted state; the MQTT integration publishes it
through connected protocol objects. Neither output assigns a second sequence.
`main()` owns the model and keeps it alive while the roles run.

## 2. Review (O1)

Parsing is the admission step. Call the model only after the codec has supplied
a valid measurement; otherwise invalid input could consume a sequence or notify
observers. The codec translates representation and validates required finite
values. The shared model knows the order of all accepted inputs, so it alone
assigns the local sequence. HTTP, SSE, and MQTT use the same representation
without each acquiring its own acceptance policy.

## 3. Lab (O2)

After the common configuration in [the exercise guide](../README.md):

```sh
cmake --build build/labs --target ch30-lab
ctest --test-dir build/labs -R '^exercise-ch30$' --output-on-failure -V
```

The target builds the canonical MiniGateway. `solution.py` reserves a loopback
endpoint without listening and configures it as the MQTT remote, so no broker can
silently satisfy the experiment. HTTP uses a separate port. Expect `/health` to
answer, initial status sequence 0, two simulated measurements with sequences 1 and
2, and identical JSON on the POST response, `/status`, and each SSE event. The
solution restarts the process and expects sequence 0 again. One PASS line reports
these observations.

Working HTTP shows the web role is usable while MQTT cannot connect; it says
nothing about CONNACK, subscription acknowledgement, or broker delivery. The
existing model is in memory, so restart discards both current state and ordering.
No broker is required or exercised by this lab.

## 4. Lab (O1)

Use the same build target, then run:

```sh
ctest --test-dir build/labs -R '^exercise-ch30-validation$' --output-on-failure -V
```

`validation.cpp` compiles the canonical model and JSON codec directly, without
copying their implementation. It accepts one valid measurement carrying producer
sequence 900, then tries malformed JSON, an object missing required fields, and
an in-memory JSON object with infinite temperature. Infinity is not a legal JSON
wire value; constructing the object directly tests the codec's finite-value guard.
Each rejected input must leave serialized state and notification count unchanged.
The next valid input must receive local sequence 2 and produce notification 2.
Expect one PASS line. This isolates validation-before-acceptance; it does not run
an MQTT broker or verify MQTT error reporting.

## 5. Design (O3)

Durable acceptance order belongs with durable accepted state. Put the sequence
advance and state update in one persistence transaction before notifying outputs;
do not add independent HTTP and MQTT counters. Define recovery after a committed
state whose publication was interrupted, and decide whether consumers need
idempotency keys. The in-memory model alone cannot supply those guarantees.

Overlapping MQTT input/output topics need an application-level origin contract:
carry stable gateway identity plus an event identity and reject already-originated
input before it becomes a fresh acceptance. Decide the retention and restart
behavior of deduplication state. Alternatively keep the disjoint topic policy and
reject overlapping configuration. Do not enable the example's private protocol-bit
option as if it were a standard MQTT 5 No Local subscription setting. These are
design discussions; neither persistence nor origin filtering is implemented by
the supplied lab.
