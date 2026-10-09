#!/usr/bin/env python3
"""Select the edition source; paired overrides are a maintainer re-baseline hook."""
import argparse
import hashlib
import json
import pathlib
import sys
import os
import re
import subprocess


def verification_target(project, reader_ref):
    ref = os.environ.get(project + '_VERIFY_REF')
    sha = os.environ.get(project + '_VERIFY_SHA')
    if bool(ref) != bool(sha) or (sha and not re.fullmatch(r'[0-9a-f]{40}', sha)):
        raise ValueError(project + ': verification override requires both a ref and a full commit')
    return sha or reader_ref


def checkout_tag(framework, tag):
    return subprocess.check_output(
        ['git', '-C', str(framework), 'describe', '--tags', '--exact-match', '--match', tag, 'HEAD'],
        stderr=subprocess.PIPE, text=True).strip()


def verify_checkout(framework, project, reader_ref):
    target = verification_target(project, reader_ref)
    if target != reader_ref:
        head = subprocess.check_output(['git', '-C', str(framework), 'rev-parse', 'HEAD'], text=True).strip()
        if head != target:
            raise ValueError(project + ': checkout differs from the frozen verification target')
    else:
        checkout_tag(framework, reader_ref)


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


def content_drift(framework, manifest):
    names = subprocess.check_output(
        ["git", "-C", str(framework), "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        text=True).split("\0")
    actual = {name: hashlib.sha256((framework / name).read_bytes()).hexdigest()
              for name in sorted(set(filter(None, names))) if (framework / name).is_file()}
    return [name for name in sorted(set(actual) | set(manifest["files"]))
            if actual.get(name) != manifest["files"].get(name)]


def verify_edition(root, framework=None):
    values = baseline(root)
    version = values.get("SNODEC_VERSION", "")
    errors = []
    manifest = json.loads((root / values["SNODEC_WORKTREE_MANIFEST"]).read_text())
    patch = root / values["SNODEC_WORKTREE_PATCH"]
    if manifest["project_version"] != version:
        errors.append("Working-tree manifest differs from the baseline declaration")
    if hashlib.sha256(patch.read_bytes()).hexdigest() != manifest["patch_sha256"]:
        errors.append("Captured framework patch differs from its recorded digest")
    recorded_tree = "".join(f"{digest}  {name}\n" for name, digest in sorted(manifest["files"].items()))
    if hashlib.sha256(recorded_tree.encode()).hexdigest() != manifest["tree_sha256"]:
        errors.append("Framework file manifest differs from its recorded tree digest")
    if values.get("SNODEC_REF") != "Book-1.0" or "SNODEC_COMMIT" in values:
        errors.append("Framework source must use the Book-1.0 edition tag")
    if version != "2.0.0":
        errors.append("This migration's declared project version must be 2.0.0")
    if framework:
        verify_checkout(framework, "SNODEC", values["SNODEC_REF"])
        cmake = (framework / "CMakeLists.txt").read_text()
        if ((framework / "VERSION").read_text().strip() != version
                or not re.search(r"\bVERSION\s+\$\{RELEASE_VERSION\}", cmake)
                or not re.search(r"include\(cmake/Version\.cmake\)", cmake)) :
            errors.append("Framework CMake project version differs from the declared version")
        for name in content_drift(framework, manifest):
            errors.append(f"Book-1.0 checkout differs from the edition manifest: {name}")
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
