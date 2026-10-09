# Chapter 15 — solutions and discussion

## 1. Review (O1)

The wrapper's include, alias and linked component select TLS stream handling.
The registered instance, context factory and EchoPair byte-reflection context can
remain unchanged. The carrier still determines the endpoint and reachability;
TLS adds secure setup, trust/name policy, shutdown and diagnostics. A protocol
that interprets certificates or requires mutual authentication has additional
application policy, so unchanged context code is a conditional result.

## 2. Review (O2, O3)

A certificate can chain to a trusted authority yet name another service. Configure
trust and the expected name separately. SNI selects a server identity; sending it
does not itself require verification of that identity. In the early connection
callback, the SSL context is available but the per-connection SSL object is not.
Apply the expected-name policy before the handshake. Shared SSL-context policy
must suit all connections using it; endpoints with different identity policies
need appropriately separate configuration. Secure readiness follows successful
setup and verification. It still does not authorize an application operation.

## 3. Lab (O2, O3)

Use [the common build configuration](../README.md) with installed TLS components,
Python TLS support and the OpenSSL command-line tool, then:

```sh
cmake --build build/labs --target ch15-lab
ctest --test-dir build/labs -R '^exercise-ch15-trust-identity$' --output-on-failure -V
```

The solution compiles `tls-runtime.cpp` and runs `run-tls.py` through `tls.py`,
all in this companion directory; the verification policy has one implementation.
The fixture creates three temporary self-signed certificate identities, supplies
an explicit trust file and uses an independent Python TLS server. Expect:

| Peer certificate | Explicit trust | Expected name | Secure readiness |
| --- | --- | --- | --- |
| sensor.example | sensor.example | sensor.example | yes |
| wrong.example | wrong.example | sensor.example | no |
| sensor.example | unrelated.example | sensor.example | no |

Each case reports `early_ssl_null=1`; readiness is 1 only in the first case. The
second case isolates a wrong expected name despite trust, while the third isolates
missing trust despite a matching name. These are local identity observations, not
a production certificate provisioning or authorization procedure. Keys and isolated
configuration are removed with the temporary directory. The test has a 60-second
outer limit and bounded subprocess/socket waits.

## 4. Lab (O1, O3)

```sh
ctest --test-dir build/labs -R '^exercise-ch15-secure-echo$' --output-on-failure -V
```

CMake derives `tls-main.cpp` from canonical EchoPair by changing only the server
include and namespace from legacy to TLS. It links the unchanged EchoPair context
and the TLS component. Inspect that generated file under the chapter's build
directory to compare the wrapper selection; there is no second echo algorithm.

The public Python solution creates a temporary `sensor.example` certificate and
key, supplies them through the server's TLS configuration and trusts that
certificate in an independent client. Expect the payload `part-vi\x00secure-echo\xff`
to return byte for byte. The client's `unwrap()` must complete, observing the
reciprocal TLS close-notify rather than treating TCP EOF as a clean TLS shutdown.
This observes one cooperative shutdown; it does not exercise a stalled peer,
forced termination or every concurrent shutdown path. Temporary keys stay local.

## 5. Design (O1, O2, O3)

With service TLS, give the service certificate/key ownership and an explicit
expected-peer policy where it acts as a client. With proxy termination, decide
whether the proxy-to-service hop is trusted or separately secured, and how any
forwarded identity is authenticated. Never treat a user-supplied identity header as
a verified certificate identity. Include renewal, key access, handshake and shutdown
timeouts, and logs that distinguish the failed boundary without exposing secrets.

Both choices can be reasonable: service TLS keeps identity at the endpoint;
a proxy can centralize certificate operations but adds a trusted intermediary.
Map verified identity to application permissions separately. A Unix pathname's
access policy or Bluetooth pairing can restrict reachability without replacing
these identity and authorization decisions.
