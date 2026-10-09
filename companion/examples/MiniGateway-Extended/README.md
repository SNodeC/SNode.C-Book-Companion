# MiniGateway-Extended

Extended guided-project application used by Chapter 31.

MiniGateway Extended keeps the web and MQTT roles from MiniGateway and adds a
Unix-domain socket measurement input role. The shared `MeasurementModel` remains
the application state boundary, so the new network role can be added without
rewriting the existing protocol roles.

Build with an installed SNode.C package:

```bash
cmake -S . -B build -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec
cmake --build build --target minigateway-extended
```

Install/deploy this example into the configured install prefix:

```bash
cmake --build build --target deploy-minigateway-extended
```

Use `-DCMAKE_INSTALL_PREFIX=/path/to/prefix` at configure time to choose the
deployment prefix.

Running the example requires an MQTT broker and the Unix-domain socket input path
configured in the source tree. Chapter 31 shows the additional socket-based smoke
check for the extended variant.

The simulation endpoint uses `POST /simulate`. The teaching SSE route accepts the
explicit `Accept: text/event-stream` value (case-insensitively), rather than general
media-range negotiation. The HTTP context's disconnect callback removes the corresponding subscription,
even when no further measurement is published. The publisher/model outlives the
event loop, and listener changes happen on that loop's thread.
The HTTP role is named `web`; use `web local --host 127.0.0.1 --port 8081` to
override its endpoint. MQTT uses protocol level 4 without the private loop-prevention
extension. Keep input and output topics distinct.
