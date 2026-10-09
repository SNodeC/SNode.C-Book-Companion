# Chapter 25 — solutions and discussion

## 1. Review (O1)

In-tree targets use local names; installed consumers resolve exported `snodec::`
targets and installed public headers. Source includes identify directly named C++
abstractions. The link line selects components such as the protocol/application
layer and concrete stream implementation. Their targets propagate the deeper dependency graph.
Copying every internal dependency into an application's link list makes the
application responsible for implementation details it does not own.

## 2. Review (O2)

In `src/apps/main.cpp`, locate the Express WebApp and its registered routes before
following HTTP readiness into dispatch. The shown teaching shape uses an anonymous
instance; do not invent a name from the executable name. Its build selects
`http-server-express` and `net-in-stream-legacy`. Predict a completed response
from a selected route, then verify that route in the actual entry point rather
than treating every illustrative path as an inventory of the source.

## 3. Lab (O1)

Use [the common configuration](../README.md), then inspect the public route fixture
at `../ch18/CMakeLists.txt` and `../ch18/dispatch.cpp`. Its single imported Express
stream component supplies the public protocol and concrete stream implementation; initialization,
middleware/routes, listener activation and runtime start form its composition root.
Find the handlers that append `app-before`, `router-before` and `handler`.

```sh
cmake --build build/labs --target ch25-lab
ctest --test-dir build/labs -R '^exercise-ch25-composition$' --output-on-failure -V
```

This reuses the earlier public HTTP framing observer unchanged. A request missing
its final blank line produces neither a response nor an application marker during
200 ms. Completing it produces HTTP 200 and the expected handler order. Relate the
observation to the build/entry-point trace: the application registers behavior,
while the installed parser admits the completed request. This is a local reading
and execution exercise; it does not execute every program in `src/apps`.




## 4. Lab (O1, O3)

```sh
ctest --test-dir build/labs -R '^exercise-ch25-consumer-trace$' --output-on-failure -V
```

Read EchoPair's executable target, `echoserver.cpp`, context library and public
component link before running the unchanged consumer mode of `../ch02/solution.py`.
Expect installed-package selection, a successful build and an exact
`environment-ready` echo reply. Attribute initialization/activation to `main()`,
byte reflection to the context, and lower dependencies to the imported component.
The new observation is that the assembled application realizes its predicted
contract; checking an installation alone would not establish the reply.

## 5. Design (O2, O3)

Read target and feature guards, then composition root, linked components and
public headers, entry-point activation, protocol callback and test. Before editing,
observe the intended endpoint's activation, the selected handler's execution and
the external result. Record captured dependencies and their lifetimes. A successful
build is a prerequisite, not one of those three runtime observations.
