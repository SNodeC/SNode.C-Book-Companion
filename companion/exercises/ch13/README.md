# Chapter 13 — solutions and discussion

## 1. Review (O1)

An accepted peer's address is an observation on that connection, not an option
for choosing the listener's peer. The listener binds its `local` endpoint.
For the schematic name `echo`, the corresponding views are
`echoServer.getConfig()->Local::setPort(8080)`, `echoserver echo local --port=8080`,
and `echo.local.port = 8080`. The complete EchoPair uses the instance name
`echoserver`, so its actual key is `echoserver.local.port`.
A client separately exposes `remote`; writing that key into a server's file
cannot create a client role.

## 2. Review (O2)

`true` establishes successful parsing and final validation. It does not restart a
listener, reconnect peers, change a captured connection policy, or replace frozen
bootstrap logging/daemonization. Reconfiguration must be deliberately called from
the event-loop thread while running; a file edit alone does nothing. Original CLI
values still override the file. `false` can mean the lifecycle forbids the call or
that parsing/validation failed; changed values are not guaranteed to roll back.
Plan how old activity ends and future activation consumes the new values. If an
atomic deployment transition is required, validate replacement configuration and
consider a controlled restart.

## 3. Lab (O1, O2)

Use [the common build configuration](../README.md), then:

```sh
cmake --build build/labs --target ch13-lab
ctest --test-dir build/labs -R '^exercise-ch13-precedence$' --output-on-failure -V
```

The solution `configuration.py` runs the canonical `echoserver` in a temporary
configuration home. It writes a file containing port 18091, then inspects source
only, source plus file, and source plus file plus CLI port 18092. It distinguishes
commented defaults from active assignments. Expect `[8080, 18091, 18092]`, status 2
for each display action, and an unchanged file. No listener starts during these
inspection actions. The source default is the actual canonical listen argument;
no replacement program or duplicate configuration parser is introduced.

To repeat manually, use the three `--show-config` commands in the chapter with
your built binary and a private file. Do not treat display status 2 as a bind
failure or assume a one-run override writes the file. The fixture's inspection
parser reads this one observed port key; it is not a general metadata consumer.

## 4. Lab (O1, O2)

```sh
ctest --test-dir build/labs -R '^exercise-ch13-discovery$' --output-on-failure -V
```

Follow `--help`, `echoserver --help`, and `echoserver local --help` on the actual
binary. The fixture checks that they reveal the instance, local section, and
`--port` respectively. Port 70000 must yield a validation error naming `--port`
and the supported range ending at 65535, with no listening record. The error does
not itself print the entire instance/section path: the invocation and local help
identify that scope. This is invalid-value rejection before activation, not a
claim about missing-value wording or a live failed bind.

## 5. Design (O2, O3)

Construct two named endpoints such as `primary-uplink` and `backup-uplink` so each
owns independent remote configuration. Two activation handles from one endpoint
still share that endpoint's settings. Give the administrative listener a stable
name and disable it in deployments that do not use it. Disabling at activation is
different from closing established peers or terminating existing flows later.

Choose which deployment changes can wait for future activations. For changes that
must replace running listeners, stop/release the relevant activity explicitly and
handle failure before advertising success. Retain old configuration and event
history for diagnosis; a failed reparse is not atomic rollback. A validated restart
may be simpler than promising seamless replacement. Renaming an instance also
requires updating files, commands and operational procedures that address it.
