# Chapter 4 — solutions and discussion

## 1. Review (O1)

The local endpoint handle configures the instance and registers activation. Shared
endpoint state and runtime callbacks retain what active work needs after a local
wrapper leaves scope. An explicit listen operation has its own flow; an accepted
connection is a separate peer relationship and can survive termination of that
listener. Its current context belongs to that connection, not to the local
variable or the listening operation's stack frame. Retaining a flow handle permits
control of that operation; dropping it is not cancellation.

This does not keep an arbitrary reference capture alive. If a factory passes an
application model to each context, the application must retain that model through
the last use. The independent-peer lab below tests peer isolation, not cancellation
of the listening flow; those are different observations.

## 2. Review (O2)

The listen-result message describes the flow's activation outcome using the named
instance `echoserver`. The transport record describes connection 1; attachment and
payload records describe its context. The local handle and the factory do not
have their own construction messages in this excerpt. A name alone does not count
connections or prove that a local wrapper remains in scope. The full observed log
is in the pass evidence `P3-echo-observation.log`; the manuscript shows its bodies.

## 3. Lab (O3)

Use the common configuration in [the exercise guide](../README.md), then:

```sh
cmake --build build/labs --target ch04-lab
ctest --test-dir build/labs -R '^exercise-ch04-model-instances$' --output-on-failure -V
```

This reuses `companion/exercises/ch32/model-instances.cpp` as a focused early
experiment; no later chapter is a prerequisite. It compiles the canonical
`companion/examples/MiniGateway/MeasurementModel.cpp` and uses the public
`accept(...)` and `current()` interface. Two references representing input paths
share one model. Their accepted sequences must be 1 and 2, and `current()` must
report 2. Two separate model objects instead each assign 1 to their first input.
Expect one PASS line comparing shared and separate ownership.

A minimal mental walkthrough is enough before opening the source: constructing
a model creates its own current measurement; `accept` replaces an input sequence
with the next locally accepted sequence. References do not create another model.
The exercise checks object ownership, not network delivery, persistence, or
interprocess order. A model constructed for each context would partition accepted
state by peer, even though every context used the same class definition.

## 4. Lab (O1)

```sh
ctest --test-dir build/labs -R '^exercise-ch04-independent-peers$' --output-on-failure -V
```

The existing bounded peer script is reused with the canonical EchoPair server.
One connection sends ten bytes, `other` followed by NUL followed by `peer`, while
another peer remains idle. The active connection must receive the same bytes.
After the idle peer closes, the first sends `still here` and must receive that
unchanged. Expect one PASS line covering both exchanges. The harness uses a fresh
loopback port and stops the server after the observations.

The result distinguishes per-connection behavior from the endpoint that accepted
both peers. It does not stop the listening flow or destroy the application model,
so neither of those operations is established by this run. It also does not say
that stream reads preserve the boundaries of the peer's writes.




## 5. Design (O1, O3)

Retain two flow handles only if the application needs independent activation
control. Both explicit connects use the instance's shared configuration. Each
resulting context keeps its own partial input; each flow keeps its activation and
recovery decisions; one separately retained model accepts parsed measurements
from both. Keep that model alive through its users and remove subscriptions before
captured state dies. No change of family, variant or protocol is needed to make
these lifetime distinctions. Stopping a listener and closing an accepted peer
remain separate operations.
