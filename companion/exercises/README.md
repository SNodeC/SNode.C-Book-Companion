# Public exercises and solutions

These are the public solutions for Parts I–XI and Appendix A. Each chapter has two
review answers, two observable labs, and a design discussion. Try the exercise before
reading its solution. `O1`–`O3` refer to the objectives printed at the chapter opening;
each exercise and solution identifies its objective explicitly.

Use the installed SNode.C environment prepared in Chapter 2. Add standalone Asio
headers (`libasio-dev` on Debian/Ubuntu) for the Chapter 1 comparison. Most labs need no external service, radio hardware or framework source build; Part IX adds an equipped local database fixture as described below. The Bluetooth selector lab needs installed Bluetooth components and development support; its optional physical RFCOMM extension is an equipped lab. IPv6 loopback must be available for the IP-family comparison.

From the companion repository root (or the author’s book checkout):

```sh
cmake -S . -B ../build/labs \
  -DSNODEC_BOOK_BUILD_PDFS=OFF \
  -DSNODEC_BOOK_BUILD_COMPANION_EXAMPLES=ON \
  -DCMAKE_PREFIX_PATH="$HOME/.local/snodec"
cmake --build ../build/labs --parallel 2
ctest --test-dir ../build/labs --output-on-failure
```

Each chapter README gives a focused build target and test command. Chapters 1, 19 and 30 labs build the canonical companion programs, then use Python's standard
library to make observations at their public socket/HTTP interfaces. The environment labs build EchoPair as an independent installed-package consumer
and diagnose an intentionally missing component in a temporary copy. Chapter 3
adds a client with a changed greeting while inheriting the existing reflection
behavior, then checks independent measurement peers for the Part I checkpoint. Chapter 30 also isolates JSON validation before acceptance; Chapter 32 compiles
the canonical `MeasurementModel.cpp` into two ownership experiments. There is only one implementation of each reused algorithm.

The architecture labs reuse the existing measurement-model experiments and EchoPair
peer harness; the runtime lab separately checks deferred callbacks through the installed
public API. The Part II checkpoint needs no transport or external service.

Part III compiles thin family drivers around the same EchoPair context and factory,
checks IP and Unix identities/cleanup, and constructs Bluetooth service selectors
without opening a radio socket.

Part IV reuses the canonical line protocol to compare framing, fresh parser state,
construction refusal and IPv4/Unix transfer through bounded independent peers.

Part V reuses EchoPair and SemanticLogging for isolated configuration inspection,
scoped errors and a reproducible runtime/logging checkpoint.

Part VI adds the OpenSSL command-line tool, installed TLS components and Python's
standard-library TLS support. Temporary certificates exercise trust and expected
identity; EchoPair supplies secure echo and controlled retry/reconnect observations.
The fixtures generate and remove their own private keys and need no external CA.

Part VII shares one synchronous route fixture for HTTP admission and Express
continuation. The existing SSE observer labs feed the checkpoint. WebSocket labs
build linked-factory variants from canonical entry points and subprotocol sources;
no module installation or external web service is required for those labs.

Part VIII builds a disposable local broker fixture from installed `mqtt-server`
support and reuses the canonical MQTT client role. Its equipped broker labs need
that server component; a packet-peer lab and gateway outage lab offer observations
without starting a broker. MQTT-over-WebSocket labs use the installed adapter with
a controlled peer. No external broker package, account or service is required.

Part IX equipped labs need MariaDB server and client tools (`mariadb-server` and
`mariadb-client` on Debian/Ubuntu). They initialize a private temporary database,
disable networking and use a private Unix socket as the current ordinary user.
No existing database or credentials are used. Missing tools fail explicitly. The
HTTP composition and gateway restart observations remain local alternatives; they
do not establish database durability. Use `-LE equipped` for a local-only subset.

Part X reuses the external EchoPair build and missing-component experiment, then
installs a fresh Release consumer into a temporary prefix. Runtime checks clear
loader overrides and use the installation's library paths. They observe process
restart, invalid-configuration recovery, endpoint refusal and a bounded echo
measurement. They do not install a service unit or deploy to an OpenWrt device.

Part XI reuses MiniGateway and MiniGateway Extended. Independent peers check CSV
framing, validation, mixed HTTP/Unix acceptance and live SSE observations with
MQTT unavailable. The final checkpoint reruns these observations alongside the
existing JSON/model experiments. Its manual broker extension requires a separate
subscriber observation and is not part of the local CTests.

Appendix A reuses the external-consumer and line-protocol carrier experiments.
Its public source-reading record connects installed component selection to flow
creation, factory construction and protocol behavior; the extension keeps one
parser while changing IPv4 to a Unix-domain carrier.

The lab peers bind loopback and choose unused ports. Each process gets temporary
configuration, is stopped on success or failure, and has a bounded test duration.
CMake passes its selected `snodec_DIR` to the external-consumer labs and supplies
the imported library directory for installed-consumer runtime paths. No separate
`SNODEC_PREFIX` environment setting is required. A failed lab prints process
output, and CTest retains the test transcript in `../build/labs/Testing/Temporary/`.
These checks require permission to open local sockets.
