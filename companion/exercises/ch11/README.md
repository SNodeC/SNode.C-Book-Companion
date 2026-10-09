# Chapter 11 — solutions and discussion

## 1. Review (O1)

The factory returns a newly created endpoint for the supplied connection. The
connection attaches and manages it; the factory does not retain a second owner or
manually delete it later. A replacement context is another fresh endpoint, not a
singleton shared by multiple peers. Detachment ends that context's responsibility,
possibly while the underlying connection continues with a different protocol.

Returning `nullptr` gives the connection no protocol endpoint and closes that
connection. There is no ready-context callback to run for a nonexistent context.
An established socket alone therefore does not guarantee protocol readiness.

## 2. Review (O3)

A copied immutable parser limit isolates each context from later changes to the
original setting. A reference to one application model avoids duplicate accepted
state, but the model must outlive all users, including callbacks and observers.
Shared ownership can permit independent retention of a service; avoid cycles and
release subscriptions before their captured state expires. Reference counting does
not make concurrent mutation safe. Construction chooses these relationships; the
factory should not become an unrestricted route to unrelated application services.

## 3. Lab (O2)

Use [the common configuration](../README.md):

```sh
cmake --build build/labs --target ch11-lab
ctest --test-dir build/labs -R '^exercise-ch11-isolation$' --output-on-failure -V
```

This runs the canonical line server and factory. Two peers first receive `READY`.
One sends `PI` without a delimiter, while the other sends `STATUS` and receives
`OK`. Close the partial peer and open a replacement through the same listener.
Its `NG` must produce `ERR unknown command`, not complete the old peer's `PING`.
Then both the replacement and surviving peer answer `PING` normally. Expect a PASS
for independent pending buffers, fresh replacement state and surviving progress.

This observes context-local parsing through peer behavior. It does not count
allocations or inspect object addresses. It also does not demonstrate persistence
of a shared model: this line protocol has no such model. The earlier model checkpoint
supplies the separate accepted-state observation.

## 4. Lab (O1)

```sh
ctest --test-dir build/labs -R '^exercise-ch11-refusal$' --output-on-failure -V
```

`refusal.cpp` is a test-only construction policy: refuse the first creation by
returning `nullptr`, then delegate to the unchanged canonical factory. It neither
parses bytes nor deletes the supplied connection. The first peer must see closure
without `READY`; the second must see `READY` and a `PONG` reply. Expect the PASS
line distinguishing refusal from later successful creation. A parser rejection
would require a created, attached context to interpret input; this failure precedes
that stage. The procedure uses the common bounded process/configuration harness.

## 5. Design (O1, O3)

Give each role a factory configured with its own immutable parser limit and an
explicit reference to the same application-owned measurement model. Each context
gets a fresh parser/buffer and a copied limit; all valid inputs reach the one model.
Place the model in a scope enclosing runtime execution and shut down contexts and
subscriptions before destroying it. Shared service ownership is an alternative only
if independent retention is needed, with cycles and thread access addressed.

A factory can select a role or context type from stable configuration. Authentication
messages and their state transitions belong in the context, using a deliberately
supplied authentication service if needed. Retry/reconnect policy remains with the
role/flow machinery. None of these responsibilities requires a factory to become
a protocol endpoint or global service locator.
