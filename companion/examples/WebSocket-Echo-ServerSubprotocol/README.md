# WebSocket-Echo-ServerSubprotocol

Compact WebSocket server subprotocol module used by Chapter 20.

The shared library exports `echoServerSubProtocolFactory()`. With the output name
and SOVERSION used in `CMakeLists.txt`, the deployed module follows the dynamic
server-subprotocol naming contract used by SNode.C:

```text
libsnodec-websocket-echo-server.so.<SOVERSION>
```

Build with an installed SNode.C package:

```bash
cmake -S . -B build -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec
cmake --build build --target websocket-echo-server-subprotocol
```

Install/deploy this example into the configured install prefix:

```bash
cmake --build build --target deploy-websocket-echo-server-subprotocol
```

Use `-DCMAKE_INSTALL_PREFIX=/path/to/prefix` at configure time to choose the
deployment prefix. The module is installed below
`lib/snode.c/web/http/upgrade/websocket`, where the WebSocket server selector
looks for dynamically loadable subprotocol modules.

For a complete runtime check, deploy this module together with
`WebSocket-Echo-ClientSubprotocol`, start `HttpUpgrade-Server`, and then run
`HttpUpgrade-Client`.

The server preserves text/binary message type and the exact payload bytes, including
embedded zero bytes. It collects one complete message before replying; configure a
finite receiver message limit for untrusted peers. The supplied teaching client
sends `hello` as text. Independent peers can check binary, empty and fragmented
messages without changing the server.
