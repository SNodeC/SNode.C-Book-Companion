# Chapter 23 — solutions and discussion

## 1. Review (O1, O3)

A boundary role names a system conversation: device exchange, integration,
observation, local control or administration. A configured SNode.C instance supplies
concrete runtime configuration for a communication role. The design labels do not
force one class or one process each. Closely related roles can share one event loop
and model; a blocking callback or process failure then affects them together.
Separate processes allow independent permissions and restart, but add serialization,
identity, ordering and unavailable-peer decisions.

## 2. Review (O1, O2)

One model accepts the measurement. MQTT and SSE project it for different consumers;
neither becomes a competing owner of accepted state. HTTP success, an SSE sequence,
storage completion and broker/subscriber acknowledgement describe different facts.
If acceptance promises only memory state, storage failure can be reported alongside
that accepted fact. If it promises durability, acceptance cannot be reported before
the storage boundary completes. Merely adding a database protocol changes neither
contract automatically.

## 3. Lab (O1, O2)

Use [the common lab configuration](../README.md), then:

```sh
cmake --build build/labs --target ch23-lab
ctest --test-dir build/labs -R '^exercise-ch23-unavailable-output$' --output-on-failure -V
```

This reuses the public MiniGateway outage solution. A reserved, non-listening local
port refuses MQTT while HTTP remains reachable. Two POSTs must produce sequences
1 and 2, with matching JSON in the response, `/status` and SSE stream. On process
restart, sequence returns to zero. No broker is needed for this observation.
The result is accepted in-memory state and live observation, not MQTT delivery or
durability. The lab does not change the gateway or implement another state model.

## 4. Lab (O1, O2, O3): Part VIII checkpoint

**Equipped broker checkpoint using the disposable local fixture.** The preceding
lab remains its no-broker alternative observation. Build with installed MQTT server
support, then:

```sh
ctest --test-dir build/labs -R '^exercise-ch23-part-checkpoint$' --output-on-failure -V
```

First the unchanged MQTT client role exchanges through the local broker with an
independent subscriber. Require CONNACK, granted SUBACK, exact received telemetry
and the return command, in that order of observations. The fixture then stops the
broker and runs the separate gateway outage observation above. It does not claim
that the gateway was connected to that earlier broker or that a live disconnect
was tested. Compare evidence across the two experiments:

| Boundary | Owner | Evidence | What remains unproved |
| --- | --- | --- | --- |
| native carrier | stream connection/context | accepted local peer and received CONNECT | MQTT session acceptance |
| session | MQTT role and broker | successful CONNACK | granted subscription or delivery |
| subscription | broker/session | SUBACK granting QoS 0 | application processing of future publications |
| telemetry delivery | broker plus independent subscriber | exact topic and `23.5` payload | persistence or QoS 1/2 recovery |
| command delivery | canonical MQTT client role | command topic/payload in callback log | actuator completion |
| gateway acceptance | MeasurementModel | POST and `/status` agree on sequence/value | persistence or MQTT delivery |
| observation | HTTP/SSE adapter | event matches accepted measurement | durable history or replay |
| unavailable output | gateway MQTT role | refused endpoint while web observations pass | recovery/replay after reconnection |

Use this map as the expected discussion answer; add actual ports and observed
payloads from your run. The private port/session environment prevents overlap
between fixtures. All processes and sockets have time bounds and cleanup.

## 5. Design (O3)

A field adapter may use Bluetooth or a custom stream while same-host control uses
Unix sockets. MQTT can carry brokered telemetry; HTTP can manage the service; SSE
can observe accepted state without making observation a control channel. Use a
WebSocket path when bidirectional interaction or access constraints justify it.

Separate an adapter process when permissions, blocking hardware access or restart
policy warrant it. Define message identity and ordering at the new boundary.
Configure and diagnose each role independently: a reconnecting broker client need
not make a healthy local administration surface report failure. Conversely, a
broken administration bind should fail visibly. During storage failure, report
memory acceptance only if that is the contract; never label it durable success.
Use distinct MQTT input/output topics or an explicit origin rule to avoid feedback.
