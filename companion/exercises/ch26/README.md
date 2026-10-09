# Chapter 26 — solutions and discussion

## 1. Review (O1, O2)

MQTTBroker owns brokerage and related administration/observation boundaries.
MQTTIntegrator subscribes, applies mapping semantics and republishes. MQTTBridge
owns broker connections, selected traffic movement and loop policy. MQTTStore
owns raw-envelope and optional typed-projection storage. A tool can host several
configured instances; a system role need not be a socket instance.

Separate executables allow independent restart, but require agreed topic/payload
contracts and recovery rules. Specify which state survives, who owns it and how a
replacement obtains it. MQTTStore submits raw and projection writes separately;
projection is not gated by the raw insert's success callback. Observe each result
and each independent row. A successful subscription or broker delivery establishes
neither raw storage nor projection, and one insert's error need not imply the
other failed. Do not label the pair an atomic transaction without that contract.

## 2. Review (O3)

The publisher submits; its broker accepts the MQTT relationship and distributes
matching publications. A source subscriber proves local delivery. MQTTBridge
selects and forwards to a destination broker; a subscriber there proves that
outcome. MQTTStore receives and submits raw/projection writes; each write's result
and an independent database query prove storage separately. No earlier observer
can certify a later participant's work solely from its own success.

## 3. Lab (O1, O2): Part IX checkpoint

**Equipped database checkpoint.** Use the private MariaDB setup in
`../ch24/README.md`, then:

```sh
ctest --test-dir build/labs -R '^exercise-ch26-part-checkpoint$' --output-on-failure -V
```

First the canonical MariaDB client commits a measurement in the disposable schema,
then exits. An independent CLI and a restarted client read that row without a
second insert. The checkpoint then runs the existing MiniGateway outage/restart
observer: two accepted HTTP measurements agree with status and SSE despite refused
MQTT, but the restarted gateway begins at sequence zero. These are separate
experiments, not a database-enabled gateway or an executed MQTTStore deployment.

Apply the difference to the chapter's publication trace:

| Outcome | Required observation | What it does not establish |
| --- | --- | --- |
| broker delivery | independent subscriber's topic/payload | storage or actuator completion |
| bridge forwarding | selected destination subscriber receives the intended topic/payload | transformation or durable storage |
| mapping | selected input and expected transformed output | bridge topology or database commit |
| raw storage | successful raw insert and independent envelope query | successful typed projection |
| typed projection | its own successful insert and independent typed-row query | atomicity with the raw insert |
| client restart | the committed measurement can be read afterward | database crash recovery or every durability configuration |
| gateway acceptance | HTTP/status/SSE share one sequence/value | persistence or MQTT delivery |
| gateway restart | sequence returns to zero | loss of a separately committed database row |

The raw/projection entries are the expected architectural discussion, not claims
that this checkpoint ran MQTTStore. Trace its two call sites and callbacks in the
suite before designing a deployment test. Preserve the original payload alongside
chosen projections when that is the declared storage contract.

The no-database alternative is `exercise-ch23-unavailable-output`, which verifies
only the in-memory half. It does not replace the equipped checkpoint. The suite's
unique-topic, ten-publication exercise additionally needs configured brokers and
MQTTStore; it is not silently inferred from these component observations.

## 4. Lab (O2, O3)

```sh
cmake --build build/labs --target ch26-lab
ctest --test-dir build/labs -R '^exercise-ch26-publication-trace$' --output-on-failure -V
```

The unchanged delivery mode of `../ch21/mqtt.py` launches the canonical local
broker and client fixtures. It needs loopback access, not an external broker,
database or device. Expect a granted subscription, exact telemetry at the
independent subscriber and an incoming command at the client. Attribute those
outcomes to broker subscription/distribution, publisher submission and subscriber
handling. This system-reading question differs from locating packet callbacks:
name the participant responsible for each fact and what remains unobserved.
It does not run MQTTBridge, MQTTStore or a multi-broker deployment.

## 5. Design (O1, O2, O3)

Keep broker delivery, integration transformation, bridge forwarding and storage as
separate responsibilities. Name each process, topic contract, endpoint, state owner
and operator observation. When a destination fails, decide whether other roles
continue and whether messages are boundedly buffered, dropped or retried. Reconnect
does not decide replay correctness. Use origin policy or distinct input/output
paths to prevent loops; the private MQTT CONNECT option is not a universal broker
interoperability mechanism.

For storage, decide whether raw and projected rows must be atomic. If they must,
a separate queue of inserts is insufficient; define transaction ownership and
failure recovery before promising that outcome. If independent outcomes are allowed,
report each honestly. A health handler running establishes local progress, not
readiness of every downstream service. Account for independent upgrades and old/new
payload compatibility when splitting processes.


