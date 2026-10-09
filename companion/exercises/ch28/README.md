# Chapter 28 — solutions and discussion

## 1. Review (O1, O3)

Startup shows that the immediate executable dependencies were found. A later
WebSocket upgrade can still fail because a selected module is absent, its directory
is wrong, its dependent libraries cannot be loaded, or permissions prevent access.
Record the intended module name, installed file, loader search configuration and
runtime diagnostic, then exercise HTTP negotiation and the selected subprotocol.
Installing an unrelated library or adding an in-tree path hides the package defect.

## 2. Review (O2, O3)

A foreground-process supervisor observes the process it starts. Self-daemonization
can separate that process from the worker the supervisor is meant to manage.
Restart policy, identity and logging therefore belong to an explicit service model.
Active status establishes process state; an exact echo establishes the listener's
behavior. MiniGateway's liveness response shows a working HTTP handler, while
readiness depends on whatever broker, persistence or freshness promises the
application declares. A restart needs a new process and a repeated exchange.

## 3. Lab (O1, O2)

Use [the common configuration](../README.md) with CMake and a C++ compiler.
CTest inherits the selected package and its imported library directory. No service-manager session or root access is required.

```sh
cmake --build ../build/labs --target ch28-lab
ctest --test-dir ../build/labs -R '^exercise-ch28-lifecycle$' --output-on-failure -V
```

`installed.py` builds the unchanged EchoPair source as a fresh Release consumer,
checks `snodec_DIR`, and installs the two applications into a temporary prefix.
It disables CMake package-registry shortcuts. The application's install RPATH lists
the actual selected framework library directories. On Linux, the lab selects
`DT_RPATH` with `--disable-new-dtags` so this private search policy also reaches
transitive dependencies such as the event-loop library; `DT_RUNPATH` on the
executable alone would apply only to its direct dependencies. The framework itself
stays in its existing prefix. This is a local installed-layout test, not a relocatable
framework package or a cross-compilation test.

The runtime observer clears `LD_LIBRARY_PATH` and `LD_PRELOAD`, then writes a
private foreground configuration using a selected loopback port. Expect exact
binary echo, normal shutdown and connection refusal afterward. A second process
must have a different identity and repeat the exchange at the same configured
endpoint. Temporary configuration, logs, build and installation are removed after
the processes stop. No host service unit is installed or changed.

To extend this to supervision, perform the chapter's systemd user-unit rehearsal
only in a session with that manager available. Observe start, new process identity
after restart, exact exchange, shutdown and inactive status. These are additional
service observations; the portable process lab does not claim to have run systemd.

## 4. Lab (O2, O3)

```sh
ctest --test-dir ../build/labs -R '^exercise-ch28-configuration$' --output-on-failure -V
```

The same private installed consumer first receives `not-a-port` in its configuration.
Expect configuration status 2, a port diagnostic and no listening message. Restore
a numeric loopback port and require the exact echo and shutdown refusal. The
application binary is unchanged: this isolates configuration recovery from build
or protocol repair. It does not exercise a supervisor's restart throttling.

Service-account permissions, log rotation, protected certificates and database
resources need their own deployment checks. The chapter's OpenWrt path is an
**advanced lab** requiring a matching SDK, a recipe modelled on the published
recipes in [the OpenWrt recipe repository](https://github.com/SNodeC/OpenWRT/tree/main/net),
and a disposable target. The book examples and labs are not prepared for
cross-compilation; writing the echo-consumer recipe is part of this advanced lab. The local installation/recovery lab is an alternative observation, not
evidence that the target package or `procd` service works.

## 5. Design / advanced lab (O1, O3)

Record release, target CPU/C library/ABI, SDK and prepared source, then review the
recipe's component dependencies and consumer toolchain. Inspect package contents,
shared-library names and target architecture before installation. Distinguish
read-only binaries/modules/assets from configuration and writable state; define
the management group and service identity, protecting private keys separately.

Let `procd` own the foreground process and bounded restart policy. Test loopback
through the chapter's controlled peer or SSH tunnel: exact exchange after start
and restart, refusal after stop, visible invalid-configuration failure and recovery.
Enable boot startup only after those checks, then verify a reboot. Keep package
repository signing and update trust with the deployment plan. Desktop success,
configuration preview and a process-status line cannot substitute for these
observations. No SDK build or target deployment is claimed by the public local labs.
