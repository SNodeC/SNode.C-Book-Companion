# Chapter 21 — solutions and discussion

## 1. Review (O1)

The lower stream context handles connection activity. `MqttContext` bridges its
receive/send/end/close operations to the protocol object. Fixed-header processing
selects a packet deserializer; the completed packet is delivered to the server or
client role. Sessions, packet identifiers, acknowledgements and keep-alive belong
to MQTT. The carrier does not become the owner of broker or session state merely
because it receives the bytes. That state can outlive a connection.

## 2. Review (O1, O3)

CONNECT asks to establish a session; successful CONNACK reports acceptance. A
SUBACK with a granted result answers a subscription request. An independent
subscriber's received topic and payload show delivery to that peer. None of these
alone demonstrates a downstream application's durable processing. This role sends
QoS 0 telemetry, so it gets no publication acknowledgement. Its command subscription
and telemetry publication use different topic paths, and it sends both requests
from CONNACK handling without waiting for SUBACK first.

## 3. Lab (O1, O2)

Use [the common lab configuration](../README.md), then:

```sh
cmake --build build/labs --target ch21-lab
ctest --test-dir build/labs -R '^exercise-ch21-wire$' --output-on-failure -V
```

`client.cpp` supplies only the native context/factory and launcher around the
unchanged `MQTT-ClientRole` library. Its context owns the canonical `SensorClient`;
the installed MQTT implementation owns parsing and session behavior.

The independent packet peer sees standard MQTT CONNECT with clean session,
60-second keep-alive and client ID `sensor-client-1`. Withhold CONNACK for 200 ms:
expect no subscription or publication during that bounded observation. Then send
successful CONNACK, observe the command subscription and the exact telemetry
publication, return SUBACK, and send a command. The client must log the command's
topic and payload. This is a controlled packet experiment, not a full broker test.
The quiet interval is not a universal timing guarantee.

## 4. Lab (O2, O3)

**Equipped broker lab, with a local disposable fixture.** This build needs installed
`mqtt-server` support in addition to the client and native stream components. It
needs no external broker service, credentials, radio, database or broker download.
The wire lab above supplies a local observation without starting the broker.

```sh
ctest --test-dir build/labs -R '^exercise-ch21-delivery$' --output-on-failure -V
```

`broker.cpp` is a launcher/factory around the installed server's broker, not another
broker implementation. It binds loopback on a selected free port with no persistent
session store. The independent subscriber connects and receives CONNACK, then a
SUBACK granting QoS 0, before the canonical client starts. It must receive exactly
`sensors/temperature/value` with payload `23.5`. A command published back through
the broker must reach the canonical role's `onPublish` callback.

The canonical source has fixed topic names and a fixed client ID. Isolation comes
from a fresh private broker and port per run, rather than rewriting that source to
claim a unique topic prefix. The temporary working directory contains its relative
session filename and is removed after shutdown. Peers and processes have bounded
waits; the fixture is stopped on success or failure. This verifies the installed
broker path, not third-party broker interoperability, persistence or QoS 1/2.

## 5. Design (O3)

Prefer a native service when both peers can use it directly. Add the WebSocket
carrier when the access path requires HTTP upgrade, while retaining MQTT semantics.
Account for upgrade/subprotocol deployment, framing and diagnostic cost.

Name separate evidence for carrier establishment, accepted session, granted
subscription, publication receipt and application processing. For absent QoS 0
subscribers, a successful send supplies no delivery proof; decide whether the
application needs retained state, replay, acknowledgements or idempotent commands.
Do not imply that the compact client's clean-session behavior supplies durable
recovery. Keep protocol keep-alive distinct from transport and reconnect timers.
