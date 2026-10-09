# Example source trees

This directory contains complete source trees that accompany the manuscript.

## Edition and new teaching examples

Use the exact 2.0.0 source snapshot in [the edition record](https://github.com/SNodeC/SNode.C-Book-Companion/blob/main/EDITION.md).

`EchoPair` supplies the complete Chapter 3 files. `SemanticLogging` supplies the
complete Chapter 14 public-API example. The selected book smoke tests check both
with deterministic observations; inspect the specific CI run for actual results.

## Compact examples

The compact examples are standalone SNode.C consumer projects for the short code
fragments in the protocol and persistence chapters:

```text
companion/examples/HttpUpgrade-Server
companion/examples/HttpUpgrade-Client
companion/examples/SSE-Server
companion/examples/SSE-EventSource-Client
companion/examples/WebSocket-Echo-ServerSubprotocol
companion/examples/WebSocket-Echo-ClientSubprotocol
companion/examples/LineProtocol-Server
companion/examples/LineProtocol-Client
companion/examples/MQTT-ClientRole
companion/examples/MariaDB-Minimal
```

Each compact example has its own `CMakeLists.txt` and can be configured against
an installed SNode.C package:

```bash
cmake -S <example-dir> -B ../example-build \
    -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec
cmake --build ../example-build --target <example-target>
```

The `companion/examples/` directory also contains an aggregate `CMakeLists.txt` that
configures, builds, and installs/deploys all examples together. The public companion is published after the book CI passes its compiler and
runtime checks. Build and test the examples in your own environment as well:

```bash
cmake -S companion/examples -B ../examples-build \
    -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec \
    -DCMAKE_INSTALL_PREFIX=/path/to/deploy-prefix
cmake --build ../examples-build --target all-examples
cmake --build ../examples-build --target deploy-examples
```

The WebSocket echo example is split across the HTTP-upgrade server/client and the
matching server/client subprotocol modules. Deploy both subprotocol modules before
running `HttpUpgrade-Server` and `HttpUpgrade-Client` as a complete echo check.

The line-protocol examples are the complete runnable server/client version of
the Chapter 10 worked `SocketContext`. Start `line-protocol-server`, then run
`line-protocol-client`. The client waits for `READY`, sends `PING`, `STATUS`,
an intentionally unknown command, and then `QUIT`.

Some examples are intended to demonstrate compilation and framework integration
rather than standalone runtime behavior. For example, `MQTT-ClientRole` builds the
MQTT role as a library because the concrete lower connection is intentionally
outside that compact example.

## Guided project examples

The final project chapters use two larger source trees:

```text
companion/examples/MiniGateway
companion/examples/MiniGateway-Extended
```

These are the source-of-truth examples for Chapters 30 and 31. They are included
in the aggregate build as `minigateway` and `minigateway-extended`; their
individual deployment targets are `deploy-minigateway` and
`deploy-minigateway-extended`.
