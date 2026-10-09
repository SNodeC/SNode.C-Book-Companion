# HttpUpgrade-Client

Compact client-side HTTP upgrade example used by Chapter 17.

The client prepares an HTTP request, names the requested upgrade protocol as
`websocket`, and installs the WebSocket client upgrade factory through the linked
registration path. It logs the local upgrade initiation result, the HTTP upgrade
response result, parse errors, and connection-status callbacks.

Build with an installed SNode.C package:

```bash
cmake -S . -B build -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec
cmake --build build --target http-upgrade-client
```

Install/deploy this example into the configured install prefix:

```bash
cmake --build build --target deploy-http-upgrade-client
```

Use `-DCMAKE_INSTALL_PREFIX=/path/to/prefix` at configure time to choose the
deployment prefix.

For a complete WebSocket echo check, deploy `WebSocket-Echo-ServerSubprotocol` and
`WebSocket-Echo-ClientSubprotocol`, start `HttpUpgrade-Server`, and then run this
client. The client subprotocol sends one message and closes after the echo arrives.
