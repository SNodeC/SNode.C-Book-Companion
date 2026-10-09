# MiniGateway

Guided-project application used by Chapter 30.

This example composes one small SNode.C application from several roles:

- a shared `MeasurementModel` created in `main()`;
- an HTTP/SSE web role for observation and simulation;
- an MQTT client role for measurement input and output;
- socket-state reporting for visible runtime diagnostics.

Build with an installed SNode.C package:

```sh
cmake -S . -B build -DCMAKE_PREFIX_PATH="$HOME/.local/snodec"
cmake --build build --target minigateway
```

Install/deploy this example into the configured install prefix:

```sh
cmake --build build --target deploy-minigateway
```

Use `-DCMAKE_INSTALL_PREFIX=/path/to/prefix` at configure time to choose the
deployment prefix.

Exercising MQTT input and output requires a broker reachable through the configured
client settings. The HTTP and SSE checks can run while that broker is unavailable.
Chapter 30 distinguishes those local checks from the broker-dependent scenario.

The simulation endpoint uses `POST /simulate`. The teaching SSE route accepts the
explicit `Accept: text/event-stream` value (case-insensitively), rather than general
media-range negotiation. The HTTP context's disconnect callback removes the corresponding subscription,
even when no further measurement is published. The publisher/model outlives the
event loop, and listener changes happen on that loop's thread.
The HTTP role is named `web`; use `web local --host 127.0.0.1 --port 8081` to
override its endpoint. MQTT uses protocol level 4 without the private loop-prevention
extension. Keep input and output topics distinct.
