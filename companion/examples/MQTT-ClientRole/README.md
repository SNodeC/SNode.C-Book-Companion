# MQTT-ClientRole

Compact MQTT client role example used by Chapter 21.

This source tree intentionally builds a library, not a standalone executable. It
shows the MQTT protocol role that is later attached to a concrete lower
connection by application code. Incoming publishes are logged so the command
path is visible instead of being silently discarded.

Build with an installed SNode.C package:

```bash
cmake -S . -B build -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec
cmake --build build --target mqtt-client-role
```

Install/deploy this example into the configured install prefix:

```bash
cmake --build build --target deploy-mqtt-client-role
```

Use `-DCMAKE_INSTALL_PREFIX=/path/to/prefix` at configure time to choose the
deployment prefix.
