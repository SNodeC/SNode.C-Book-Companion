# SemanticLogging

Complete logging-only Chapter 14 example. It uses `<Log.h>` and the public
`snode::log::configure(Settings)` startup path, without starting SNode.C's runtime.

```sh
cmake -S . -B build -DCMAKE_PREFIX_PATH=/path/to/snodec-prefix
cmake --build build --parallel 8
./build/semantic-logging
```

It emits JSON records with application/component/instance identity, a named event,
a component-level debug override, and a deliberately constructed typed error.
The error is a presentation demonstration, not an observed failed system call.
