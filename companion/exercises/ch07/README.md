# Chapter 7 — solutions and discussion

## 1. Review (O1)

For a local IPv4 bind, `0.0.0.0` permits all local IPv4 interfaces and port zero
asks the operating system for a port. A remote client still needs a reachable
address and the actual chosen port. Loopback narrows exposure to this host.
An empty Unix path is not a request to listen on every pathname; choose a concrete
rendezvous name and its owning directory. A Bluetooth selector of zero is initial
configuration, not evidence that the desired service exists. Select the matching
family and service and supply the peer's device identity. The Bluetooth address
lab also distinguishes an empty configured device string from an explicit wildcard.

## 2. Review (O3)

`Unsupported` supplies no successful credential observation. Do not interpret the
remaining fields as a verified user or group. A reachable socket path establishes
reachability, not permission to perform every application operation. Choose a
policy: refuse operations requiring credentials, or use another explicitly defined
authentication mechanism. A successful credential query would still need a rule
mapping the observed identity to the requested operation. Directory permissions
and application authorization answer different questions.

## 3. Lab (O1, O2)

Use [the common configuration](../README.md), then:

```sh
cmake --build build/labs --target ch07-lab
ctest --test-dir build/labs -R '^exercise-ch07-ip-families$' --output-on-failure -V
```

The three thin `family-server.cpp` targets choose a public family header/type and
component at compilation. They link the existing `echosocketcontext` library;
there is no second echo protocol or measurement parser. `families.py` binds only
loopback and uses the common process harness with isolated configuration and a
bounded lifetime. It sends `900,23.5`, `2,24.0`, and invalid binary input as one byte
sequence and requires the exact bytes back. Neither input sequence becomes an
accepted model sequence.

Expect one PASS for IPv4 and one for IPv6, with producer and service identities.
The producer's local endpoint must agree with the server's remote observation;
the service endpoint must agree with the server's local observation. A rendered host may be `localhost`; the fixture resolves it within the selected
family and compares the resulting host/port with the socket observation. The producer
has an automatically chosen local port. Each server uses the separate loopback
endpoint supplied to its configuration. The socket family is explicit at both
ends: this experiment does not establish IPv4-mapped or dual-stack behavior.

IPv6 loopback must be enabled on the lab host. An unavailable family fails this
exercise rather than silently substituting IPv4. The script chooses an unused
port before starting the server; an intervening external bind can still produce
an endpoint conflict, which is reported as a failure. Rerun after resolving that
conflict. No DNS service, broker, or radio is needed.

## 4. Lab (O3)

```sh
ctest --test-dir build/labs -R '^exercise-ch07-unix-path$' --output-on-failure -V
```

The same driver/context and peer script use a private temporary directory. The
service binds `service.sock`; the Python producer explicitly binds `producer.sock`.
Expect matching local/remote identities in opposite directions and an exact
measurement-byte reply. After the producer closes, it removes its own bind path.
After graceful server shutdown, its service path must be absent. The sentinel
`keep.txt` must still contain `unrelated file` before the temporary directory is
removed by the fixture. Expect one Unix PASS line.

Those checks distinguish endpoint cleanup from fixture cleanup: the directory
manager is not allowed to hide a surviving server-owned path. This run does not
exercise permission denial, stale paths, abstract addresses, or the credential
query. Those remain separate behaviors; do not infer an authorization policy from
successful byte transport.

## 5. Design (O1, O2, O3)

A pathname socket fits a deliberately local helper with a controlled runtime
directory and explicit access/cleanup ownership. Give both processes access to the
same namespace and use a credential or protocol policy appropriate to the commands.
Loopback IP may fit existing network tools and a later move to another host; make
the future routing, authentication, encryption, and exposure policy explicit.
Moving from loopback to a network interface is a deployment change even if the
context code stays identical.

For either choice, separate the producer's own endpoint from the service it seeks,
record actual identities after connection, and keep framing and measurement
validation in the protocol layer. Byte reflection establishes the carrier;
application acceptance still belongs to the shared model developed earlier.
