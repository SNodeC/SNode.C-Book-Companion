# Chapter 18 — solutions and discussion

## 1. Review (O1)

`WebApp` supplies the root router. `WebAppT<ServerT>` combines it with a concrete
HTTP server handle and named configuration instance. Construction registers that
configuration; listening activates a flow. Later, HTTP request readiness creates
a controller for one dispatch through the longer-lived route tree. The controller
carries request/response facades and continuation state. It is not another event
loop, and a request's dispatch lifetime is not the application's lifetime.

## 2. Review (O2, O3)

Returning from a middleware callback does not call its continuation. `next()`
advances the dispatcher chain; it is not a thread handoff. Sending a completed
response deliberately answers this request. Unconditional continuation after that
can make a later handler compete to answer the same request. Choose who responds,
and inspect both response data and handler visits when diagnosing the choice.

## 3. Lab (O1, O2)

Use [the common lab configuration](../README.md), then:

```sh
cmake --build build/labs --target ch18-lab
ctest --test-dir build/labs -R '^exercise-ch18-order$' --output-on-failure -V
```

`dispatch.cpp` implements the small route tree described in the chapter. App
middleware records `APP`, router middleware records `ROUTER`, and `/api/status`
records `HANDLER`. Its response header `X-Trace` and body must both contain
`app-before,router-before,handler`. A following `/outside` request returns 404;
only app middleware runs for that path. The Python solution verifies the response,
order trace and exact visit counts across both requests.

This fixture deliberately uses synchronous callbacks and sequential requests.
Its short shared trace is an observation aid for this experiment, not a proposed
request-state design for asynchronous handlers. No framework-source build or
module deployment is needed. It reuses the installed router and parser directly.

## 4. Lab (O2)

```sh
ctest --test-dir build/labs -R '^exercise-ch18-stop$' --output-on-failure -V
```

The `/blocked` middleware returns 403, sets `X-Trace: app-before,stop`, and sends
`middleware stopped request` without calling `next()`. A later handler would emit
`UNEXPECTED-HANDLER`; it must never run. The solution checks the response and
absence of all handler markers. This is an application response from admitted
HTTP input, not parser rejection. Try the optional scratch-copy continuation
experiment in the chapter without modifying the public solution's assertions.

## 5. Design (O1, O3)

Place shared authentication before protected handlers, then parse JSON where a
route actually needs it. Mount related sensor paths beneath one router; choose
strict/case routing and parent-parameter merging deliberately. An unauthenticated
request should have one response owner and should not continue into a protected
handler after rejection. Virtual-host dispatch and static content may need their
own policy rather than inheriting unrelated API decisions.

Bound malformed and oversized wire input in HTTP parser policy before middleware
runs. Middleware can validate JSON or permissions after admission, but cannot
retroactively bound memory already consumed. Keep long-lived subscriber lifetime,
slow-observer handling and accepted application state under explicit owners.
A flat handler remains reasonable for a small independent endpoint; mount routers
when shared policy or path context warrants the additional dispatch structure.
