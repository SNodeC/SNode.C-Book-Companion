# Chapter 14 — solutions and discussion

## 1. Review (O1)

An accepted application record belongs to application origin and the context (or
other protocol owner) boundary. A transport attachment belongs to framework origin
and the connection boundary. Both can carry the actual instance and connection
identifier; a context need not have a separate server/client role field. Do not
invent an identifier before a peer exists. A logger owns its identity strings,
but deriving identity from a live connection does not extend that connection's
ownership. HTTP context replacement can keep the connection identifier while
changing the protocol responsibility.

## 2. Review (O2, O3)

The component's `Debug` threshold applies unless a matching instance override is
more specific. These are ordered choices, not successive minimum filters.
Disabling trace skips logger formatting, but C++ still evaluates call arguments.
Guard expensive diagnostic-only work with `enabled(...)`; keep required state
transitions outside that guard. Neither disabled logging nor semantic fields
redact an emitted application message. Decide which content is safe separately.

## 3. Lab (O1, O2)

Use [the common build configuration](../README.md), then:

```sh
cmake --build build/labs --target ch14-lab
ctest --test-dir build/labs -R '^exercise-ch14-records$' --output-on-failure -V
```

The public `records.py` solution runs the canonical `semantic-logging` executable.
Expect four JSON records with levels info, info, debug and warn. Each has application
origin/boundary, component `gateway.measurements` and instance `measurement-input`.
The debug record survives the global Info threshold because of the component
override. The second record's event is `measurement.accepted`; the fourth carries
an explicit error and states that no file operation occurred. No connection or role
identity appears. Timestamps are intentionally not compared.

This program demonstrates the standalone `configure(Settings)` path, not a running
service's bootstrap or runtime reconfiguration. The same public observation is
reused by the teaching smoke check so there is one authority for this contract.

## 4. Lab (O1, O2, O3): Part V checkpoint

```sh
ctest --test-dir build/labs -R '^exercise-ch14-part-checkpoint$' --output-on-failure -V
```

The shared configuration fixture repeats the source/file/CLI experiment, with a
fresh unused loopback port as the CLI winner. It checks local help and rejection
of 70000 before starting a listener. The private file remains at 18091.

It then starts EchoPair twice on the selected loopback endpoint. Both runs exchange
`part-v-checkpoint` unchanged. Global `--log-level=2 --log-format=json` suppresses
normal records. Adding `--log-component-level=echo=info` and
`--log-instance-level=echoserver=debug` exposes the application listening record
with that port and an application-origin context debug record with actual instance
and connection identity. The fixture checks those semantic facts and prints the
observed records. It does not require incidental ordering, timestamps or a fixed
connection identifier. The application `echo` logger has no instance field, which
is why its component override and the context's instance override are both used.

The invalid-value diagnostic names `--port`; help and the command's `echoserver local`
path locate its owning scope. An actual echo response establishes that the selected
endpoint ran. Suppressed records alone would not establish inactivity. The fixtures
use isolated configuration, bounded processes and loopback; no broker, database,
TLS fixture or hardware is needed. This checkpoint verifies startup selection and
logging attribution, not runtime reparse, reload rollback or live listener replacement.
Carry this discipline into the named MiniGateway inputs and uplinks later.

## 5. Design (O3)

Record `publish.submitted` only after local admission, with a message that says it
was queued. Record failure at the attempt or connection boundary that observed it,
using an actual connection identifier only when available. Delivery needs its own
protocol-level acknowledgment or application receipt; do not infer it from a send
queue or transport connection. A retry can retain the instance name while changing
the peer episode. HTTP upgrades similarly change context without requiring a new
transport identity.

Use component, instance, message size, correlation identifier and failure reason
where safe. Avoid credentials and unnecessary payload content. Capture a supplied
error immediately and preserve its category; protocol rejection need not have a
system error. Keep a short history and the effective endpoint/retry/log policy
rather than enabling an unbounded confidential dump. Logging must not change the
protocol's acceptance or retry decisions.
