#!/usr/bin/env python3
"""Verify the edition tag and declared project version."""
import argparse
import pathlib
import sys
import re
import subprocess


def checkout_tag(framework, tag):
    return subprocess.check_output(
        ['git', '-C', str(framework), 'describe', '--tags', '--exact-match', '--match', tag, 'HEAD'],
        stderr=subprocess.PIPE, text=True).strip()


def baseline(root) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in (root / "source-baseline/book-source-baseline.env").read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            key, separator, value = line.partition("=")
            if not separator or not re.fullmatch(r"SNODEC_[A-Z_]+", key):
                raise ValueError(f"Invalid baseline assignment: {line!r}")
            values[key] = value
    return values


def verify_edition(root, framework=None):
    values = baseline(root)
    version = values.get("SNODEC_VERSION", "")
    errors = []
    if values.get("SNODEC_REF") != "Book-1.0":
        errors.append("Framework source must use the Book-1.0 edition tag")
    if version != "2.0.0":
        errors.append("This migration's declared project version must be 2.0.0")
    if framework:
        checkout_tag(framework, values["SNODEC_REF"])
        cmake = (framework / "CMakeLists.txt").read_text()
        if ((framework / "VERSION").read_text().strip() != version
                or not re.search(r"\bVERSION\s+\$\{RELEASE_VERSION\}", cmake)
                or not re.search(r"include\(cmake/Version\.cmake\)", cmake)) :
            errors.append("Framework CMake project version differs from the declared version")
    return values, errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify the Book-1.0 framework edition without the manuscript.")
    parser.add_argument("--framework", type=pathlib.Path, required=True)
    args = parser.parse_args()
    try:
        values, errors = verify_edition(pathlib.Path(__file__).resolve().parents[1], args.framework)
        if errors:
            raise ValueError("\n".join(errors))
        print("Framework edition verified: SNode.C " + values["SNODEC_VERSION"] + ", " + values["SNODEC_REF"])
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print("Framework edition check failed: " + str(error), file=sys.stderr)
        raise SystemExit(1)
