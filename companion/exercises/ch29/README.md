# Chapter 29 — solutions and discussion

## 1. Review (O1)

A wrong address string belongs at the address-value boundary. Fragmented HTTP input
needs parser pending/accept/reject checks plus a real exchange where relevant.
An unexpectedly retained context needs the ownership transition and a bounded
lifetime observation. A missing installed module needs a genuine installed-path
negotiation, not another source include path. Register the smallest reproduction
that would have failed before the repair, then check the composed public behavior.

## 2. Review (O1, O3)

An ASan loader error means instrumentation did not start correctly; it is not a
protocol result. A skipped socket test did not execute its intended exchange.
A passing timing run checks the declared payload exchanges and reports that
client's workload timing. It supplies neither production capacity nor protocol
certification, crash recovery or target-deployment evidence. Record environment,
selection, counts and limits rather than collapsing these outcomes into “green”.

## 3. Lab (O1, O2)

Use [the common configuration](../README.md) with the C++ build tools available
during CTest. The tests inherit the enclosing build’s selected package.

```sh
cmake --build ../build/labs --target ch29-lab
ctest --test-dir ../build/labs -R '^exercise-ch29-diagnosis$' --output-on-failure -V
```

The driver first reuses the missing-component experiment from `../ch02/solution.py`:
configuration fails before an application exists, then restoration builds and runs.
Next `../ch28/installed.py` independently builds and installs the canonical consumer.
The correct configured endpoint echoes. A separate local socket reserves a port
without listening; connection to that wrong endpoint must be refused. This avoids
accidentally contacting an unrelated service. The installed application's build
and correct exchange remain successful. Record the two failures at their different
boundaries; changing CMake cannot repair a peer's wrong address.

## 4. Lab (O1, O2, O3): Part X checkpoint

```sh
ctest --test-dir ../build/labs -R '^exercise-ch29-checkpoint$' --output-on-failure -V
```

The checkpoint repeats component diagnosis, a fresh external Release build,
private installation, exact echo and wrong-endpoint refusal. It then runs
`roundtrip.py`, the chapter's complete Python listing, with only the fixed endpoint
substituted by the fixture's private port. Source alignment checks the public file
against the printed listing. There is one calculation of the sample count,
median and nearest-rank p95. The driver checks output shape and correctness, with
no machine-specific speed threshold.

Expect twenty warm-up exchanges followed by `samples=200 bytes=256 connections=1`,
a positive median and a p95 at least as large. Every reply must match all 256 bytes;
short reads are accumulated and timeouts fail the experiment. The process runs
without loader overrides; the server logs at Info in JSON to a temporary file.
The CMake transcript records the compiler and selected installation, and the
measurement records the platform, build type, endpoint, logging and warm-up count.

For comparison across runs, also record the CPU, selected multiplexer, operating
conditions and source contents as the chapter requests. Preserve the output sink,
binary and workload while changing one chosen condition. A single result from
this local checkpoint is a diagnostic observation, not a performance baseline.
The 190th sorted sample gives the small-sample p95; the reciprocal of a round-trip
time is not server capacity. Connection establishment, TLS, concurrency, slow peers,
proxy behavior and persistent state remain outside this measurement.

You can run the unchanged listing manually against the chapter's installed server
at `127.0.0.1:18093`. The public driver avoids that fixed port for automated labs.

## 5. Design (O1, O3)

Define what remains observable when one subscriber stops reading: accepted state,
other subscribers' progress, bounded queued bytes and the declared slow-peer
policy. Use a controlled slow peer and an independent healthy observer. State the
message size/rate, connection count, duration, logging and platform before measuring.
Track complete delivered records, latency distribution, queue/memory growth and
recovery after removing pressure. Bound the test and clean up every peer.

A regression asserts the public invariant and failure policy; a benchmark measures
a declared workload. Do not merely sleep and assume a callback happened. Profile
an observed regression to locate cost. Add installed-module, service-user, TLS,
proxy or OpenWrt checks only for deployments that introduce those boundaries, and
report absent equipment as untested. The loopback echo checkpoint cannot establish
those production properties.
