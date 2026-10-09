# Chapter 12 — solutions and discussion

## 1. Review (O1)

Change the public server header, namespace in the server alias, default listen
argument, and linked CMake component. Keep the line context implementation/header
and its factory unchanged. The callback names `LineProtocolServer::SocketAddress`,
so selecting the alias also selects its address type. Runtime CLI values choose
the actual loopback endpoint or private path without entering the parser.

The lab's CMake file applies those exact carrier substitutions to the canonical
entry point in the build directory. Its dependency on the original `main.cpp`
triggers reconfiguration after changes. It compiles the original context source
and includes the original factory, maintaining one protocol implementation.

## 2. Review (O3)

Unix peer credentials describe local process identity under the platform's query.
An IP address is not a replacement user identity. Choose network authentication,
trust and authorization explicitly before exposing the same command parser over
IP. TLS authentication also needs certificate/name policy and an authorization
rule; encryption alone does not grant permission for every command. If protocol
meaning or conversation changes, distinct contexts may be clearer than carrier
conditionals in one class.

## 3. Lab (O1, O2): Part IV checkpoint

Use [the common configuration](../README.md), then:

```sh
cmake --build build/labs --target ch12-lab
ctest --test-dir build/labs -R '^exercise-ch12-part-checkpoint$' --output-on-failure -V
```

The canonical IPv4 server and generated Unix entry point use the same context and
factory sources. The bounded fixture runs the framing sequence at every two-piece
split and as one write on each carrier. It verifies `READY`, reconstructed `PONG`,
`OK` and unknown-command replies, empty/CRLF behavior, no premature response to
`PI` during a quiet interval, and closure after `QUIT`. Finally it compares the
recorded reply lists between carriers. Expect two framing PASS lines and one
Part IV checkpoint PASS. The Unix service path must be gone after shutdown, before
the fixture removes its private directory.

Application write boundaries are varied; kernel callback segmentation is not
controlled or certified. This checkpoint establishes a transferable line-framing
conversation. A measurement record still needs CSV parsing, validation and the
shared model's acceptance in the later extension. It does not certify Bluetooth,
TLS authentication, or deployment access policy. The lab needs only installed IPv4
and Unix legacy stream components and Python 3; no broker, database or radio.

## 4. Lab (O2, O3)

```sh
ctest --test-dir build/labs -R '^exercise-ch12-endpoint-failure$' --output-on-failure -V
```

Start the Unix listener in a private directory and establish a valid peer. A second
client uses a nonexistent pathname there and must fail with `FileNotFoundError`
before any protocol greeting. The valid peer then sends `BOGUS`, receives
`ERR unknown command`, and can still send `PING` and receive `PONG`. Expect one
PASS distinguishing endpoint failure from command rejection. Server-owned cleanup
is checked after bounded shutdown. Do not "repair" this failed endpoint by changing
the parser or weakening path permissions.

## 5. Design (O1, O3)

Keep framing, record validation and the shared model interface explicit. The local
helper and network input may share a parser if their message meanings agree, while
outer configuration chooses path versus host/port and legacy versus TLS components.
Factories supply stable limits, roles and required services; each connection still
gets its own unfinished record.

Choose local path ownership/permissions and any credential policy independently
from network certificate/name verification and authorization. Inactivity, command
deadlines and slow-peer policy may need different deployment values without changing
framing. If the authenticated conversation differs, use separate contexts around a
shared parser rather than hiding trust transitions in carrier-dependent branches.
The model remains the single owner of accepted state across both inputs.
