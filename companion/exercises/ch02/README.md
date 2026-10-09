# Chapter 2 — solutions and discussion

## 1. Review (O1)

Inspect the edited source and the build directory first. Then check where
`cmake --install` placed the rebuilt framework. Finally inspect the consumer's
`CMakeCache.txt`: `snodec_DIR` identifies the installed package selected during
configuration. A successful framework build does not refresh the installation,
and moving a checkout does not change a cached package selection. Reinstall into
the intended prefix and rebuild the consumer. Use a fresh consumer build directory
when switching installations so old cache entries cannot silently win.

## 2. Review (O3)

The client development headers and libraries satisfy compilation and linking.
A persistence experiment also needs a running MariaDB server, a test database,
and suitable credentials. Updating the in-memory model checks acceptance and
observation within one process. It cannot demonstrate durable storage, database
permissions, or recovery after a database outage. This is why the persistence
experiment is an equipped lab even if the server runs on your own machine.

## 3. Lab (O2)

After configuring the book's labs as described in [the exercise guide](../README.md):

```sh
cmake --build ../build/labs --target ch02-lab
ctest --test-dir ../build/labs -R '^exercise-ch02-consumer$' --output-on-failure -V
```

CTest passes the package selected by the enclosing CMake build. The solution
configures `companion/examples/EchoPair` directly in a fresh temporary build tree,
checks that `snodec_DIR` matches that selection exactly, and builds both canonical programs.
It runs the server against a bounded loopback peer, which sends
`environment-ready` followed by a newline and requires identical returned bytes.
Expect two PASS lines: the selected package location, then the build and byte
exchange. This exercises an external consumer independently of the book's enclosing
build. The next programming chapter explains the context behind that reflection.

To inspect a persistent consumer build manually from the repository root:

```sh
cmake -S companion/examples/EchoPair -B ../build/environment-consumer \
  -DCMAKE_PREFIX_PATH="$HOME/.local/snodec"
cmake --build ../build/environment-consumer --parallel 2
cmake -LA -N ../build/environment-consumer | grep '^snodec_DIR:'
../build/environment-consumer/echoserver --log-level=5
```

In a second terminal, run `../build/environment-consumer/echoclient --log-level=5`
and observe the repeated greeting; stop both with Ctrl-C. The automated solution
uses a finite peer instead of that repeating pair.

The automated solution uses the shared lab harness to locate libraries under the
selected prefix and isolate user configuration. If a manual executable cannot
load a library, check the installation's runtime search path as well as its CMake
package location; configure-time discovery and runtime loading are separate steps.

## 4. Lab (O3)

```sh
ctest --test-dir ../build/labs -R '^exercise-ch02-component$' --output-on-failure -V
```

The solution copies the canonical EchoPair into a temporary directory and changes
`net-in-stream-legacy` to `net-in-stream-missing` in that copy's CMake file.
Configuration must fail with the missing name in its diagnostic, before a server
binary exists. It then restores the original CMake file, configures again, checks
the prefix, builds both programs, and runs the same bounded byte exchange. Expect three PASS
lines: the intentional failure, the selected package, and the repaired build/exchange.
All temporary files are removed; the companion sources remain unchanged.

The failure belongs to component discovery. No listener or client connection has
been created, so a port change cannot affect it. Repair the component name and
its matching imported target together. Merely suppressing a required-package
error would leave the target without the public framework surface it needs.

## 5. Design (O1, O2, O3)

Keep each framework source/build pair separate, install each into an explicit
prefix, and give each consumer configuration its own build directory. Record the
selected `snodec_DIR` alongside the run command. Rebuild and reinstall before
rebuilding a consumer when the framework changes.

Begin with the local echo labs. Later, inspect MQTT packet construction using a
controlled peer and Bluetooth address selection without claiming broker delivery
or radio exchange. Schedule those equipped labs only when their services or
hardware are available. A second framework installation does not supply missing
runtime equipment; these are independent choices in the environment.
