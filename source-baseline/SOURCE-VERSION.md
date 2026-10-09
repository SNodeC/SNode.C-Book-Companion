# Target SNode.C Source Version

This edition describes SNode.C project version **2.0.0**. Use `SNodeC/snode.c`
tag `Book-1.0`, then compare its content with the edition manifest. The version
2.0.0 is the CMake project version; `Book-1.0` identifies the edition source.

- Repository: `SNodeC/snode.c`, edition tag `Book-1.0`
- Edition content: `framework-working-tree.json` (1,405 files)
- Baseline recorded: `2026-10-06`
- `framework-working-tree.patch` is empty; its digest remains checked.

## Reader checkout

Set `SNODEC_BOOK_SOURCE` to the absolute directory containing the companion source
package. Clone the edition tag; no patch is needed.

```sh
git clone --branch Book-1.0 https://github.com/SNodeC/snode.c.git
cd snode.c
git describe --tags --exact-match --match Book-1.0 HEAD
python3 "$SNODEC_BOOK_SOURCE/ci/source_reference.py" --framework "$PWD"
```

The printed tag must be `Book-1.0`. The checker verifies the selected tag and
compares file contents with the edition manifest. If it reports
“Book-1.0 checkout differs from the edition manifest”, the named files have
changed, appeared or disappeared. Repeat the check against a fresh `Book-1.0`
clone. If the mismatch remains, report the named files to the book maintainers
and pause the affected examples until claims, manifest and tests have been
reviewed together. Do not bypass the check or move the edition tag.

Follow Chapter 2 for build requirements. Keep source, build and install locations
separate; rebuild applications and dynamically loaded extensions against the
verified public headers and libraries.

## One checkout authority

`book-source-baseline.env` declares the repository, edition tag and manifest.
The companion workflow checks out that tag, reports its name and verifies
contents before building. The reader checker verifies the supplied framework
clone without requiring manuscript access. The private book CI additionally
checks complete printed listings against the companion sources. Compilation
and runtime tests are separate.

The manifest covers the framework's tracked file contents, including public
headers, implementation, build files and tests; its digest identifies the reviewed
content. Historical review records retain their original observations. MQTTSuite
uses `SNodeC/mqttsuite` tag `Book-1.0` as a separate source-reading reference;
the external anchor checker verifies its named paths and symbols.

The [published repository](https://github.com/SNodeC/Packages/blob/main/README.md)
contains signed packages and documentation. OpenWrt recipes are maintained separately,
under [net/snode.c/Makefile](https://github.com/SNodeC/OpenWRT/blob/main/net/snode.c/Makefile)
and [net/mqttsuite/Makefile](https://github.com/SNodeC/OpenWRT/blob/main/net/mqttsuite/Makefile).
The package repository’s main branch is recreated on every publication. Use these URLs rather than
an edition tag or a content anchor for that published surface; the framework
manifest does not cover package publications.
