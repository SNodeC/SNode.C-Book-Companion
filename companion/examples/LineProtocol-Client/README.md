# LineProtocol-Client

This compact example is the runnable client counterpart to the line-command
`SocketContext` introduced in Chapter 10.

It connects to `localhost:8090` using the legacy IPv4 stream stack:

```text
net::in::stream::legacy::SocketClient<LineCommandClientContextFactory>
```

After the server sends `READY`, the client sends this short command sequence:

```text
PING
STATUS
UNKNOWN
QUIT
```

The expected response sequence before the final close is:

```text
READY
PONG
OK
ERR unknown command
```

Build with an installed SNode.C package:

```bash
cmake -S . -B build -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec
cmake --build build --target line-protocol-client
```

Install/deploy this example into the configured install prefix:

```bash
cmake --build build --target deploy-line-protocol-client
```

Use `-DCMAKE_INSTALL_PREFIX=/path/to/prefix` at configure time to choose the
deployment prefix.

Start `LineProtocol-Server` first, then run this client.
