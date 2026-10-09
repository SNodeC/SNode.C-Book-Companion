# SSE-Server

Compact server-side Server-Sent Events example used by Chapter 19.

It exposes `/events`, rejects requests that do not accept `text/event-stream`,
sends the event-stream response header, and then writes event records as response
fragments. The `/simulate` route publishes a new measurement so connected SSE
clients receive another event.

Build with an installed SNode.C package:

```bash
cmake -S . -B build -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec
cmake --build build --target sse-server
```

Install/deploy this example into the configured install prefix:

```bash
cmake --build build --target deploy-sse-server
```

Use `-DCMAKE_INSTALL_PREFIX=/path/to/prefix` at configure time to choose the
deployment prefix.

The simulation endpoint uses `POST /simulate`. The teaching SSE route accepts the
explicit `Accept: text/event-stream` value (case-insensitively), rather than general
media-range negotiation. The HTTP context's disconnect callback removes the corresponding subscription,
even when no further measurement is published. The publisher/model outlives the
event loop, and listener changes happen on that loop's thread.
