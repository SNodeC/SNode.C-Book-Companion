# Standalone Asio echo comparison

Chapter 1 compares this asynchronous TCP server with EchoPair. Install standalone
Asio headers (`libasio-dev` on Debian/Ubuntu), then build without SNode.C:

```sh
cmake -S companion/examples/Comparison-AsioEcho -B build/asio-echo
cmake --build build/asio-echo
./build/asio-echo/asio-echo 8081
```

The server binds loopback only. Stop with Ctrl-C. It reflects arbitrary bytes and
imposes no message framing. Each session owns its socket and buffer; handlers
retain the session until read/write completion. Reads resume only after the
entire output chunk has been written. EOF or I/O error releases the session when
the last handler returns. The server and signal registration outlive `run()`;
shutdown stops dispatch, then destruction releases remaining operations.

This is a teaching comparison, not a benchmark or a production service. It has
no TLS, idle timeout, reconnect policy, or admission limit. A slow peer occupies
one bounded session buffer and its socket. Chapter 1's paired lab sends identical
binary input to this server and EchoPair; see `companion/exercises/ch01/README.md`.

API reference: [Asio configuration and supported platforms](https://think-async.com/Asio/asio-1.30.2/doc/asio/using.html).
