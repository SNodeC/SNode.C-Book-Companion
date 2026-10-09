# Chapter 31 — solutions and discussion

## 1. Review (O1)

`main()` constructs one `MeasurementModel` before constructing the roles. The
Unix server receives it through `std::ref`; its factory stores a reference and
passes that reference to each newly allocated context. No measurement state is
copied by this route. Two connections share acceptance order but have separate
`receiveBuffer` strings: fragments from different producers must never form one
record. The model outlives the roles' event-loop use. The factory constructs;
the context frames and validates; the model accepts and notifies subscribers.
The web and MQTT roles need no knowledge of this new input path.

## 2. Review (O2)

A stream preserves bytes, not sender write boundaries. A record has at most 4096
bytes before its newline, including a trailing carriage return if supplied.
Receiving 4097 bytes must close the connection whether the sender writes once or
several times. Dropping an overlong prefix and parsing its suffix as a new
measurement would turn invalid input into an acceptance whose result depends on
buffering. The context retains incomplete data, checks the delimiter position,
and closes an overlong incomplete record too. A separate, fresh connection can
submit a valid record afterward; it receives the next model-assigned sequence.

## 3. Lab (O2)

After configuring the installed SNode.C environment in
[the exercise guide](../README.md), run:

```sh
cmake --build build/labs --target ch31-lab
ctest --test-dir build/labs -R '^exercise-ch31-framing$' --output-on-failure -V
```

This builds the canonical `minigateway-extended`; `gateway.py` supplies independent
Unix and HTTP peers. It selects private endpoints, reserves an unavailable MQTT
port, isolates configuration and closes the process and socket path on exit.
It adds no application implementation or alternative parser.

Expected observations, in order:

| Input | Accepted sequence / outcome |
| --- | --- |
| Whole CSV record carrying sequence 9000 | Local sequence 1, with the three supplied numeric values |
| The same CSV split across two writes | Identical values, local sequence 2 |
| Malformed number, non-finite number, missing field, invalid sequence suffix, extra field; then a valid record on the same stream | Only the final valid record is accepted, at sequence 3 |
| Valid values padded to 4096 bytes before newline, including CR | Accepted once, sequence 4 |
| Overlong record with a valid-looking suffix, sent together or across writes | Connection closes; status remains exactly at sequence 4 |
| Valid record on a fresh connection | Sequence 5 |

The valid record after malformed inputs is a parsing barrier on the same ordered
stream: its observed sequence establishes that the preceding malformed records
were not accepted. Two Python writes do not guarantee two OS receive callbacks;
the checks assert the record contract independently of that scheduling. They are
bounded examples of framing and validation, not exhaustive parser fuzzing.

## 4. Lab (O1, O2)

```sh
ctest --test-dir build/labs -R '^exercise-ch31-mixed$' --output-on-failure -V
```

Run with MQTT deliberately unavailable. Two independent SSE observers and HTTP
status see the same accepted values: an HTTP simulation gives sequence 1 and a
Unix record carrying 9000 gives sequence 2. Disconnect the first observer. Send
malformed CSV followed by valid CSV on one Unix stream: the surviving observer
gets the valid record at sequence 3. Reconnect with `Last-Event-ID: 1`: expect the
current snapshot 3, not replay of 2. Simulating again yields 4 at both active
observers and in status. Restarting the process resets sequence to zero.

The observer context managers close the actual HTTP connections. Continued public
observations test the remaining live path; the model-ownership experiment in
[the architectural solutions](../ch32/README.md) separately checks unsubscribe
semantics. A snapshot on reconnect is not durable history. None of these local
observations establishes MQTT delivery or persistence.

**Equipped MQTT extension.** With a reachable test broker and the gateway's
`mqtt-uplink` directed to it, open an independent subscriber before injecting:

```sh
mosquitto_sub -t minigateway/measurement/output
```

Inject a valid CSV line through the configured Unix socket. Compare the subscriber's
JSON values and sequence with `/status` and the SSE event. Supply sequence 9000
again and verify the published value uses the gateway's next local sequence.
Keep input and output topics disjoint. This manual extension needs broker and
client tools plus confirmed session/subscription readiness; it is separate from
the two mandatory local labs and is not executed by their CTests. A connected
socket or successful local acceptance alone supplies no subscriber-delivery
observation. Use the unavailable-MQTT lab above as the local alternative.

## 5. Design (O3)

Different privileges and independent restart requirements justify a separate
collector process. Give the gateway ownership of the Unix socket path; restrict
its parent directory and socket permissions to the intended collector identity.
Define bounded newline-delimited records, validation rules and whether the
collector expects an acknowledgement. The current input protocol supplies none:
if acceptance evidence is required, add an explicit reply contract rather than
interpreting a successful write as acceptance.

Let the collector own device errors and bounded reconnect/buffering policy; let
the gateway own record validation and acceptance order. On replay, a separately
named device sample identity and deduplication policy may be needed. The gateway
model remains in memory and does not become durable merely because the collector
is separate. If both responsibilities instead share privileges, lifetime and
restart policy, another in-process role avoids an unnecessary recovery protocol.
