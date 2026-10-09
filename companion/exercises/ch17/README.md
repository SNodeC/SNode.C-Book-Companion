# Chapter 17 — solutions and discussion

## 1. Review (O1)

The lower connection owns stream activity; the HTTP context parses messages and
exposes complete request/response meaning. Its factory creates that protocol
endpoint. On the server, readiness invokes application handling with request and
response objects. On the client, `MasterRequest` coordinates sending concrete
requests and delivers responses or parse errors. Neither application path should
create a second HTTP framing parser. Connection/TLS establishment and HTTP
message completion remain different observations.

## 2. Review (O1, O3)

A connected peer can send malformed or over-limit HTTP and be rejected before
application dispatch. Parser limits belong before that dispatch; authorization
belongs to the application meaning of an admitted request. A valid request can
also receive an application rejection such as 403.

Successful descriptor adoption transfers ownership to the file source; the caller
must not close it afterward. Directory-relative opening supplies normal `openat`
lookup, not a confinement guarantee against symlinks, `..`, mounts or renames.
Check a null source after opening, and stop a valid source if pipe attachment is
rejected. Later EOF, read failure and backpressure follow the streaming lifecycle.

## 3. Lab (O1, O2)

Use [the common lab configuration](../README.md), then:

```sh
cmake --build build/labs --target ch17-lab
ctest --test-dir build/labs -R '^exercise-ch17-framing$' --output-on-failure -V
```

This target builds the public `../ch18/dispatch.cpp` route fixture. The shared
`dispatch.py` peer sends the start line and complete header lines for
`GET /api/status`, withholding only the final blank line. During a bounded
200-ms observation, expect no response and no `APP` marker. Sending the final
blank line must then produce 200 and `app-before,router-before,handler`.

This makes message completeness observable at both the wire and application
boundary. The finite quiet interval is a controlled observation, not a universal
timing guarantee. The fixture uses ordinary Express dispatch over the HTTP parser;
it does not implement parsing. Its request handlers are synchronous and the test
sends requests sequentially. All sockets and the process have finite timeouts.

## 4. Lab (O2, O3)

```sh
ctest --test-dir build/labs -R '^exercise-ch17-limits$' --output-on-failure -V
```

The same fixture starts with `lab http parser --maximum-header-line-bytes=40`.
One valid request must return 200. The bytes `not-http\r\n\r\n` and a request
with `X-Large: ` followed by fifty `x` bytes must each receive an HTTP client-error
response; the run prints the actual status. The observed statuses are 405 and 431.
The contract tested is rejection before application dispatch, not a claim that
all malformed requests share one status. Only the valid request may emit an
`APP /api/status` marker.

The experiment exercises this line limit, including its terminator, and malformed
request input. It does not certify every parser limit, trailer counting,
pipelining policy, client response policy or file-streaming ownership path. Their
separate definitions and qualifications remain in the chapter.

## 5. Design (O3)

For uploads, choose finite start-line/header/field and decoded-body limits based
on accepted resources. Bound pending requests and decide chunked-transfer and
pipelining policy. Count decoded entity bytes separately from wire chunk framing.
Limit output independently; a parser budget is not a write-queue budget.

For SSE, HTTP header limits still apply, but the raw event receiver takes over
after response validation: `maximum-body-bytes` is not a lifetime byte quota for
an open event stream. Bound individual events, subscriber count, replay history
and each observer's queued output where their owners can enforce those policies.
Keep authorization before opening the stream. No chosen resource limit grants a
caller permission to access an upload destination or subscribe to protected data.
