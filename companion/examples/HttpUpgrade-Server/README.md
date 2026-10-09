# HttpUpgrade-Server

Compact server-side HTTP upgrade example used by Chapter 17.

It shows the HTTP/Express boundary only: a route receives an HTTP request and calls
`res->upgrade(...)`. The example links the WebSocket server upgrade factory at
compile/link time so the upgrade selector can resolve the name `websocket`
without relying on a later dynamic module lookup.

Build with an installed SNode.C package:

```bash
cmake -S . -B build -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec
cmake --build build --target http-upgrade-server
```

Install/deploy this example into the configured install prefix:

```bash
cmake --build build --target deploy-http-upgrade-server
```

Use `-DCMAKE_INSTALL_PREFIX=/path/to/prefix` at configure time to choose the
deployment prefix.

For a complete WebSocket echo check, deploy `WebSocket-Echo-ServerSubprotocol` and
`WebSocket-Echo-ClientSubprotocol`, then run this server and `HttpUpgrade-Client`.
