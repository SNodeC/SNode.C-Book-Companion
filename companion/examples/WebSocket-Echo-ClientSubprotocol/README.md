# WebSocket-Echo-ClientSubprotocol

Compact WebSocket client subprotocol module used by Chapter 20.

The shared library exports `echoClientSubProtocolFactory()`. With the output name
used in `CMakeLists.txt`, the built module follows the dynamic subprotocol naming
contract:

```text
libsnodec-websocket-echo-client.so.<SOVERSION>
```


Build with an installed SNode.C package:

```bash
cmake -S . -B build -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec
cmake --build build --target websocket-echo-client-subprotocol
```

Install/deploy this example into the configured install prefix:

```bash
cmake --build build --target deploy-websocket-echo-client-subprotocol
```

Use `-DCMAKE_INSTALL_PREFIX=/path/to/prefix` at configure time to choose the
deployment prefix. The module is installed below
`lib/snode.c/web/http/upgrade/websocket`, where the WebSocket client selector
looks for dynamically loadable subprotocol modules.


For a complete runtime check, deploy this module together with
`WebSocket-Echo-ServerSubprotocol`, start `HttpUpgrade-Server`, and then run
`HttpUpgrade-Client`.
