# Chapter 22 — solutions and discussion

## 1. Review (O1)

Message-data callbacks append bytes to `data`. At message end the adapter appends
that collection to `buffer`, adds to `size`, clears `data` and schedules the receive
event. `recv` copies at most the requested count, advances `cursor` and reduces
`size`. The event invokes MQTT receive processing and reschedules while unread
bytes remain; when exhausted it clears the buffer and resets the cursor. Callback
segmentation must not change packet meaning. WebSocket message boundaries are not
MQTT packet boundaries, and parsing remains the MQTT object's responsibility.

## 2. Review (O1, O3)

The HTTP upgrade selector resolves `websocket`; the WebSocket selector resolves
`mqtt`; that factory creates an adapter and the application's MQTT role. Linking
an adapter component supplies its code, but does not register an application-specific
factory automatically. The concrete HTTP carrier, upgrade entry point and matching
role registration must all exist. The generic adapter is shared by server/client
aliases; MQTT sees the stable `MqttContext` surface behind either role.

## 3. Lab (O1, O2)

Use [the common lab configuration](../README.md), then:

```sh
cmake --build build/labs --target ch22-lab
ctest --test-dir build/labs -R '^exercise-ch22-binary$' --output-on-failure -V
```

CMake derives an entry point from canonical `HttpUpgrade-Client`: request `mqtt`
and retain an explicit linked MQTT factory. `factory.cpp` attaches the unchanged
`SensorClient` to the installed `mqtt-client-websocket` adapter. It supplies no new
MQTT parser or WebSocket adapter. The context owns the protocol role for this
connection; session files are confined to a temporary working directory.

The bounded Python peer verifies the requested name, returns HTTP 101 with the
matching accept key and selected `mqtt`, then decodes the client's masked binary
CONNECT. It sends CONNACK split into a binary start frame and a continuation frame.
Expect the role's command SUBSCRIBE and telemetry PUBLISH. Return SUBACK, then a
binary command: the canonical client must log that exact command.

This tests framing-to-MQTT receive scheduling through the installed adapter. The
peer is deliberately a controlled protocol fixture, not a broker: successful
subscription/publication exchanges here are not independent subscriber delivery.
The local broker lab supplies that separate observation. TLS, all segmentation
patterns, malformed-packet cases, overload and reconnect are not exercised here.

## 4. Lab (O2, O3)

```sh
ctest --test-dir build/labs -R '^exercise-ch22-text$' --output-on-failure -V
```

Repeat the successful HTTP upgrade and binary CONNECT observation, but send the
same CONNACK bytes in a text message. Expect `Wrong Opcode: 1 (TEXT)` and close code
1002. The peer returns the close frame to complete closing. MQTT packet bytes do
not make the wrong WebSocket message type valid. The test checks the requested
error closure; it does not infer every later parser action from that one result.

## 5. Design (O3)

First separate lower connection/TLS readiness, HTTP 101 and selected subprotocol
from MQTT acceptance. Inspect message type and frame validation, then buffer
arrival, message end, scheduled receive and packet parsing. Finally examine the
broker's MQTT acceptance policy and response. Record each observed milestone,
rather than attributing a missing CONNACK to a generic connection failure.

Keep keep-alive, WebSocket control/close and lower timeouts distinct. Test a valid
binary packet before malformed input, and compare packet bytes across callback
segmentation. A protocol-level failure should not prompt changes to unrelated
routing or a second parser in the application.
