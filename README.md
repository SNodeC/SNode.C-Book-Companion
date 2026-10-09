# SNode.C Book Companion

Examples, exercises, solutions and edition verification for *Layered Network
Programming with SNode.C: Building Multi-Protocol Applications in Modern C++*
by Volker Christian.

This repository is published automatically from the private `SNodeC/SNode.C-Book`
repository, which is the sole source of truth. Do not edit this copy. Report
corrections through this repository's issue tracker; accepted fixes are made in
the book repository and published here after its GCC and Clang checks pass.
`publication.json` identifies the exact source commit and workflow run. The
manuscript, proposal, CV, internal reviews and private Git history are not included.

## Contents

- [Complete examples](companion/examples/README.md), including EchoPair,
  MiniGateway and MiniGateway Extended.
- [Exercises and solutions](companion/exercises/README.md) for all 32 chapters
  and Appendix A: review answers, lab commands, expected observations and design
  discussions.
- [Framework edition](source-baseline/SOURCE-VERSION.md), its content manifest
  and a checker usable without access to the book repository.
- CMake support for building the examples and running the 66 exercise tests.

## Setup

Use Linux, a C++20 compiler, CMake 3.20 or later, Python 3 and the installed
SNode.C 2.0.0 development components. The examples also need standalone Asio
headers. TLS labs use the OpenSSL command-line tool; equipped database labs
need MariaDB server/client tools. See the exercise guide for individual lab
requirements and optional hardware.

```sh
git clone https://github.com/SNodeC/SNode.C-Book-Companion.git
cd SNode.C-Book-Companion
export SNODEC_BOOK_SOURCE="$PWD"
git clone --branch Book-1.0 https://github.com/SNodeC/snode.c.git ../snodec-book-edition
python3 ci/source_reference.py --framework ../snodec-book-edition
```

Install the verified framework using its build instructions, or use the
[development packages](https://github.com/SNodeC/Packages). The installed package
and checked-out source must correspond to the edition being studied. MQTTSuite
source-reading exercises use `SNodeC/mqttsuite` at `Book-1.0`.

## Build and run the labs

Keep build files outside this checkout:

```sh
cmake -S . -B ../companion-build -DCMAKE_BUILD_TYPE=Debug
cmake --build ../companion-build --parallel 2
ctest --test-dir ../companion-build --output-on-failure
```

For a private framework installation, add
`-Dsnodec_DIR=/absolute/prefix/lib/cmake/snodec` to the configure command.
CMake supplies the selected package to the installed-consumer labs automatically.
Use `ctest --test-dir ../companion-build -LE equipped --output-on-failure` when
MariaDB tools are unavailable; this deliberately omits the equipped tests.

The programs are teaching examples, not hardened services. Start network labs on
loopback and read each example's prerequisites and limitations before wider use.
A successful build or local lab does not certify a production deployment.
