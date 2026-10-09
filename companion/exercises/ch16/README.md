# Chapter 16 — solutions and discussion

## 1. Review (O1, O2)

A refused initial connection is a failed activation; retry may schedule another
attempt within that activation flow. Loss after context attachment ends an
established peer episode; enabled client reconnect can initiate a new connection.
An activation status alone is insufficient evidence of protocol readiness, especially
with TLS. Observe context attachment and the conversation too. `DISABLED` records
intentional non-participation. `ERROR | NO_RETRY` still reports an error, with a
separate indication that this path will not retry. Terminating one activation's
recovery does not close an already established connection or stop sibling flows.

## 2. Review (O1, O3)

Inactivity measures absence of input; repeated partial commands are activity.
An absolute command deadline measures time to semantic completion and must not
restart merely because another fragment arrives. The line protocol's byte limit
bounds stored input but is not that deadline. Likewise, a successful queue admission
means local ownership of bytes, not remote execution. Backpressure, timeout,
transport failure and protocol rejection should remain distinguishable. A replay
after uncertain delivery can duplicate an operation even when the new stream works.

## 3. Lab (O1, O2)

Use [the common build configuration](../README.md), then:

```sh
cmake --build build/labs --target ch16-lab
ctest --test-dir build/labs -R '^exercise-ch16-bounded-retry$' --output-on-failure -V
```

The public `recovery.py` solution reserves a loopback endpoint by binding without
listening, then runs canonical EchoPair's client there. Retry is enabled with
`--retry-tries=1 --retry-timeout=.2 --retry-base=1 --retry-jitter=0`; reconnect is
disabled. Expect two application error records, no `Echo context attached` record,
and natural successful process exit after the recovery budget is exhausted. One
retry is additional to the initial attempt. A process exit code describes the
program's completion, not success of either connection attempt; the error records
supply those outcomes. The socket reservation prevents another listener from
silently turning this experiment into a success case.

## 4. Lab (O1, O2, O3): Part VI checkpoint

```sh
ctest --test-dir build/labs -R '^exercise-ch16-part-checkpoint$' --output-on-failure -V
```

First, the solution runs the same TLS trust/name fixture as the previous chapter:
trusted/matching succeeds, trusted/wrong-name fails, untrusted/matching fails.
Next, a controlled independent TCP peer tests recovery using unchanged EchoPair.
These are separate observations; the recovery half uses the legacy stream wrapper
and does not claim to repeat the complete TLS lifecycle during reconnect.

The peer initially reserves its port without listening. The client must report a
failed attempt before any context attachment. The peer then listens; the first
connection must deliver EchoPair's greeting. Closing that peer and listener causes
a subsequent failed activation. After the listener restarts, expect another greeting,
a second distinct connection identifier and a byte-for-byte `recovered` response.
The fixture prints the observed error, attachment and detachment records. Instance
identity persists; peer-episode identity changes. Bounded waits and a finite retry
budget prevent an unavailable peer from leaving an unbounded test.

Reconnect is enabled at a short delay; retry handles failed attempts while the
listener is unavailable. The experiment distinguishes these by whether an
established connection preceded the failure, not by guessing from elapsed time.
The restored echo shows the new stream works; it does not establish delivery of
any request sent on the old stream. No automatic application replay is implemented
or claimed. Carry the same distinction into MiniGateway's uplink diagnostics.

## 5. Design (O2, O3)

Choose a finite retry budget for a one-shot operation, or explain why an always-on
uplink should continue under a capped, jittered delay with observable failure.
Jitter reduces synchronized attempts; it does not change the error's meaning.
State whether fatal conditions are eligible and expose intentional disablement.
Bound local queues and define refusal behavior; accepted bytes still need whatever
acknowledgment the application requires. Use an absolute deadline for a complete
command if steady incomplete traffic must not keep it alive indefinitely.

For a state-changing command, choose no automatic replay after uncertain delivery,
or use a stable operation identifier with a receiver-side deduplication contract.
An idempotent operation can permit retry, but only if repeating it has the intended
semantics. Define the identifier's lifetime, acknowledgment and retention policy;
reconnect and a new context alone cannot supply them. Test the policy separately
from the local recovery experiment above.
