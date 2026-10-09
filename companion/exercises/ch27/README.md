# Chapter 27 — solutions and discussion

## 1. Review (O1)

A header exposes a C++ abstraction. A supported component request tells the
installed package which public selection to load. An exported target may also be
loaded as a dependency without being a supported request name. The logging example
requests `core` and links the loaded `snodec::logger`; it does not invent a `logger`
request. Header presence alone cannot validate a component name or its export.

## 2. Review (O1, O3)

PUBLIC requirements serve the target and consumers; PRIVATE requirements serve
the target; INTERFACE requirements serve consumers. A static library has no final
executable link of its own, so a private implementation dependency can still be
needed when the consumer links. Keep compile usage requirements distinct from
that final-link responsibility. Declare a dependency at the component that needs
it instead of making every application repeat the transitive graph.

## 3. Lab (O1, O2)

Use [the common configuration](../README.md); CTest inherits the selected
framework package. CMake and a C++ compiler must remain available during CTest:
this exercise performs a fresh external build.

```sh
cmake --build ../build/labs --target ch27-lab
ctest --test-dir ../build/labs -R '^exercise-ch27-consumer$' --output-on-failure -V
```

This deliberately repeats the environment lab while reading the consumer's
component ownership. It reuses `../ch02/solution.py` without another implementation.
Inspect `../../examples/EchoPair/CMakeLists.txt` and the selected installation's
`INTERFACE_LINK_LIBRARIES` entries. The public request is `net-in-stream-legacy`;
the shared echo context carries it to both executables. Follow the installed
network and stream dependencies without copying them into the consumer.

Expect `snodec_DIR` to match the enclosing build’s selected package exactly, a successful independent
build, then exact reflection of `environment-ready`. The observer accumulates the
whole response. That establishes a selected installed consumer, not every component
combination or a packaged service.

## 4. Lab (O2, O3)

```sh
ctest --test-dir ../build/labs -R '^exercise-ch27-component$' --output-on-failure -V
```

The reused lab copies EchoPair into a temporary directory and changes its component
to `net-in-stream-missing`. Configuration must fail naming that component before
an executable exists. The lab restores the canonical CMake text, configures and
builds it, then repeats the successful exchange. The installed framework and
original companion sources are unchanged. The error belongs to package discovery,
not the socket endpoint or the protocol.

## 5. Design (O1, O3)

A TLS IPv4 web administrator can name `<express/tls/in/WebApp.h>` and select the
concrete `http-server-express-tls-in` component. That component owns Express/HTTP
and the TLS carrier; the application should not reproduce their lower graph. A
source that directly names a MariaDB client adds its public header and `db-mariadb`
selection when that feature is enabled. An absent database dependency must be an
explicit build/configuration decision, not a mysterious runtime feature loss.

Place implementation-only dependencies privately and propagate usage requirements
needed by public headers. Record compiled defaults separately from instance options
and policy already captured by running flows. Rebuild ABI-dependent applications
and protocol modules together against the selected installation. Check both package
configuration and an installed consumer; neither a header inventory nor an in-tree
build establishes the whole contract.
