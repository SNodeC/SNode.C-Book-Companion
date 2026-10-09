# LineProtocol-Server

This compact example is the runnable server counterpart to the line-command
`SocketContext` introduced in Chapter 10.

It listens on IPv4 TCP port `8090` using the legacy stream stack:

```text
net::in::stream::legacy::SocketServer<LineCommandServerContextFactory>
```

For each connection, the server sends a greeting line:

```text
READY
```

It then accepts the following line commands:

```text
PING    -> PONG
STATUS  -> OK
QUIT    -> close the connection
other   -> ERR unknown command
```

Build with an installed SNode.C package:

```bash
cmake -S . -B build -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec
cmake --build build --target line-protocol-server
```

Install/deploy this example into the configured install prefix:

```bash
cmake --build build --target deploy-line-protocol-server
```

Use `-DCMAKE_INSTALL_PREFIX=/path/to/prefix` at configure time to choose the
deployment prefix.

Run the server before starting `LineProtocol-Client`.
