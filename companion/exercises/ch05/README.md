# Chapter 5 — solutions and discussion

## 1. Review (O1)

Read `net::rc::stream::tls::SocketServer<MyFactory>` as a Bluetooth RFCOMM stream
server with TLS connection handling and a factory creating per-peer contexts.
Its public header is `<net/rc/stream/tls/SocketServer.h>` and its corresponding
component is `net-rc-stream-tls`. Availability depends on the enabled framework
components and build dependencies. The type name does not supply Bluetooth
hardware, permissions, pairing, a selected channel, certificates, or trust policy.
It also does not specify the application protocol implemented by the factory's
contexts. Selecting this type alone does not demonstrate a radio or TLS exchange.

## 2. Review (O1, O2)

For IPv4→Unix, select `net::un::stream::legacy::SocketServer<MyFactory>`,
`<net/un/stream/legacy/SocketServer.h>` and `net-un-stream-legacy`; the stream
context and echo behavior remain. For legacy→TLS over IPv4, select the matching
`net::in::stream::tls` type, `<net/in/stream/tls/SocketServer.h>` and
`net-in-stream-tls`; configure certificate/trust policy separately. For echo→line,
change the context and its factory/header while retaining the selected lower
server header and component. Record parsing changes; byte transport need not.

## 3. Lab (O2, O3)

Use [the common configuration](../README.md), then:

```sh
cmake --build build/labs --target ch05-lab
ctest --test-dir build/labs -R '^exercise-ch05-layer-families$' --output-on-failure -V
```

The canonical `../ch07/family-server.cpp` is compiled twice with different family
and header definitions. Both use the canonical EchoPair context. The unchanged
driver sends the same binary measurement bytes and verifies exact replies for
IPv4 and Unix only. For this chapter, identify the type/header/component choices
and unchanged protocol behavior. The driver's additional endpoint and cleanup
assertions protect its fixture; interpreting family-specific addresses is deferred
to the address chapter. No Bluetooth equipment or IPv6 interpretation is needed.

## 4. Lab (O1, O3)

```sh
ctest --test-dir build/labs -R '^exercise-ch05-layer-component$' --output-on-failure -V
```

The unchanged component mode of `../ch02/solution.py` makes a temporary consumer
request `net-in-stream-missing`, observes configuration failure, restores
`net-in-stream-legacy`, then builds and observes exact reflected bytes. The missing
selection represents the composed IPv4 legacy stream layer. A failed component
request precedes any runtime endpoint; it is not an echo-parser failure. This
question checks the layer selection rather than repeating environment setup.

## 5. Design (O2)

Use IPv4 and Unix public server types and matching `net-in-stream-legacy` and
`net-un-stream-legacy` components. Keep the chosen stream form and connection
variant explicit. Both factories may supply the same measurement context and
model dependency if the protocol contract is unchanged. Addressing and admission
still require family-appropriate configuration. The runtime chapter's design
owns per-peer buffers and model lifetime; this design identifies the changed
composition and the behavior it does not need to duplicate.
