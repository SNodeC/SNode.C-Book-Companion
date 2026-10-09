# SSE-EventSource-Client

Compact EventSource client example used by Chapter 19.

It connects to `/events`, registers open/message/custom-event/error callbacks,
and then enters the SNode.C runtime.

Build with an installed SNode.C package:

```bash
cmake -S . -B build -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec
cmake --build build --target sse-eventsource-client
```

Install/deploy this example into the configured install prefix:

```bash
cmake --build build --target deploy-sse-eventsource-client
```

Use `-DCMAKE_INSTALL_PREFIX=/path/to/prefix` at configure time to choose the
deployment prefix.
