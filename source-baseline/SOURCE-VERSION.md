# Target SNode.C Source Version

This edition describes SNode.C project version **2.0.0**. Use `SNodeC/snode.c`
tag `Book-1.0` as the sole edition source reference. The version 2.0.0 is the
CMake project version; `Book-1.0` identifies the edition source.

## Reader checkout

Set `SNODEC_BOOK_SOURCE` to the absolute directory containing the companion source
package. Clone the edition tag:

```sh
git clone --branch Book-1.0 https://github.com/SNodeC/snode.c.git
cd snode.c
git describe --tags --exact-match --match Book-1.0 HEAD
python3 "$SNODEC_BOOK_SOURCE/ci/source_reference.py" --framework "$PWD"
```

The printed tag must be `Book-1.0`. The checker verifies the selected tag and
project version. It does not compare file contents with a separately recorded
snapshot. If verification fails, check the selected tag or use a fresh clone.

Follow Chapter 2 for build requirements. Keep source, build and install locations
separate; rebuild applications and dynamically loaded extensions against the
selected public headers and libraries.

## One checkout authority

`book-source-baseline.env` declares the repository, edition tag and project
version. The companion workflow checks out that tag and verifies the tag and
version before building. The reader checker works without manuscript access.
The private book CI additionally checks complete printed listings against the
companion sources. Compilation and runtime tests are separate.

Historical review records retain their original observations; a later tag update
does not renew earlier test results. MQTTSuite uses `SNodeC/mqttsuite` tag
`Book-1.0` as a separate source-reading reference; the external anchor checker
verifies its tag, named paths and symbols.

The [published repository](https://github.com/SNodeC/Packages/blob/main/README.md)
contains signed packages and documentation. OpenWrt recipes are maintained separately,
under [net/snode.c/Makefile](https://github.com/SNodeC/OpenWRT/blob/main/net/snode.c/Makefile)
and [net/mqttsuite/Makefile](https://github.com/SNodeC/OpenWRT/blob/main/net/mqttsuite/Makefile).
The package repository’s main branch is recreated on every publication. Use these
URLs for that published surface; the framework edition tag does not identify
package publications.
