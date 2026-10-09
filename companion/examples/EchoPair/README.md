# EchoPair

Complete Chapter 3 teaching example for the pinned SNode.C 2.0.0 source snapshot.
Unlike the framework's separate `examples/echo`, this version keeps the direct
host/port setup printed in the chapter. Both are installed consumers.

```sh
cmake -S . -B build -DCMAKE_PREFIX_PATH=/path/to/snodec-prefix
cmake --build build --parallel 8
./build/echoserver --log-level=5
./build/echoclient --log-level=5
```

The pair reflects bytes repeatedly. Stop both processes after observing it.
The book CI separately checks each executable with a controlled Python socket
peer; it does not interpret arbitrary TCP chunk boundaries as message boundaries.
