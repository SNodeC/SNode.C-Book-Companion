# MariaDB-Minimal

Compact MariaDB client example used by Chapter 24.

The example is intended to compile as a SNode.C consumer application. Running it
requires a reachable MariaDB server and a schema such as the one shown in the
chapter. It logs connection state, affected-row counts, selected rows, and SQL
errors.

Build with an installed SNode.C package:

```bash
cmake -S . -B build -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec
cmake --build build --target mariadb-minimal
```

Install/deploy this example into the configured install prefix:

```bash
cmake --build build --target deploy-mariadb-minimal
```

Use `-DCMAKE_INSTALL_PREFIX=/path/to/prefix` at configure time to choose the
deployment prefix.
