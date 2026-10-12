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
    edition = root / "production/edition.env"
    if not edition.is_file():
        edition = root / "edition.env"
    for line in edition.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            key, separator, value = line.partition("=")
            if not separator or not re.fullmatch(r"SNODEC_[A-Z_]+", key):
                raise ValueError(f"Invalid baseline assignment: {line!r}")
            values[key] = value
    return values


def verify_edition(root, framework=None, selected_ref=None):
    values = baseline(root)
    if selected_ref is not None:
        values["SNODEC_REF"] = selected_ref
    version = values.get("SNODEC_VERSION", "")
    errors = []
    if not re.fullmatch(r"Book-[0-9]+\.[0-9]+(?:\.[0-9]+)?", values.get("SNODEC_REF", "")):
        errors.append("Framework source must use a numeric Book edition tag")
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
    parser = argparse.ArgumentParser(description="Verify the framework edition without the manuscript.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--framework", type=pathlib.Path)
    mode.add_argument("--select-ref", help="Select a validated tag in this checkout only")
    args = parser.parse_args()
    try:
        root = pathlib.Path(__file__).resolve().parents[1]
        values, errors = verify_edition(root, args.framework, args.select_ref)
        if errors:
            raise ValueError("\n".join(errors))
        if args.select_ref is not None:
            edition = root / "production/edition.env"
            if not edition.is_file():
                edition = root / "edition.env"
            lines = edition.read_text().splitlines(keepends=True)
            matches = [i for i, line in enumerate(lines) if line.startswith("SNODEC_REF=")]
            if len(matches) != 1:
                raise ValueError("Exactly one SNODEC_REF assignment is required")
            lines[matches[0]] = "SNODEC_REF=" + values["SNODEC_REF"] + "\n"
            edition.write_text("".join(lines))
        action = "selected" if args.select_ref is not None else "verified"
        print("Framework edition " + action + ": SNode.C " + values["SNODEC_VERSION"] + ", " + values["SNODEC_REF"])
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print("Framework edition check failed: " + str(error), file=sys.stderr)
        raise SystemExit(1)
