#!/usr/bin/env python3
"""Report newer BendHub versions without installing or executing packages."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from check_bendhub import (
    HASH, HUB, VERSION, CheckError, Failure, HubClient, Reference,
    escape_annotation, parse_references, read_manifest,
)

RELEASE_ROOT = "https://github.com/bendlang/bend/releases/tag/"
RELEASE_VERSION = r"(?:0|[1-9][0-9]*)(?:\.(?:0|[1-9][0-9]*)){2}"
RELEASE_POINTER = re.compile(
    r"Latest stable release: \[Bend (" + RELEASE_VERSION + r")\]\("
    + re.escape(RELEASE_ROOT) + r"(v" + RELEASE_VERSION + r")\)"
)


@dataclass(frozen=True)
class Update:
    line: int
    name: str
    current: str
    latest: str
    url: str
    detail: str


def version_tuple(value: str) -> tuple[int, ...]:
    if not isinstance(value, str) or not re.fullmatch(VERSION, value):
        raise CheckError("Expected a canonical four-component Hub version")
    try:
        return tuple(int(part) for part in value.split("."))
    except ValueError as error:
        raise CheckError("Hub version components are too large") from error


def load_json(data: bytes) -> dict:
    try:
        value = json.loads(data)
    except (ValueError, UnicodeError, RecursionError) as error:
        raise CheckError("Invalid JSON metadata") from error
    if not isinstance(value, dict):
        raise CheckError("Expected a metadata object")
    return value


def check_name(refs: list[Reference], fetch) -> tuple[list[Update], list[Failure]]:
    name = refs[0].package.split("@", 1)[0]
    try:
        metadata = load_json(fetch(f"name/{name}"))
        latest = metadata.get("latest")
        if metadata.get("name") != name or not isinstance(latest, dict):
            raise CheckError("Missing latest publication or mismatched Hub name")
        version = latest.get("version")
        newest = version_tuple(version)
        package_hash = latest.get("hash")
        if not isinstance(package_hash, str) or not HASH.fullmatch(package_hash):
            raise CheckError("Invalid latest package hash")
        older = []
        for ref in refs:
            current = version_tuple(ref.package.split("@", 1)[1])
            if current > newest:
                raise CheckError(f"README version is ahead of Hub latest {version}; metadata is inconsistent")
            if current < newest:
                older.append(ref)
        # Most runs need metadata only. Inspect one manifest per newer package.
        manifest = read_manifest(package_hash, fetch(f"{package_hash}/manifest")) if older else {}
    except CheckError as error:
        return [], [Failure(ref.line, f"{name}: {error}") for ref in refs]

    updates = []
    for ref in older:
        detail = (f"{ref.path} is present; review compatibility before updating"
                  if ref.path in manifest else
                  f"{ref.path} is absent; find the new entrypoint before updating")
        updates.append(Update(ref.line, name, ref.package.split("@", 1)[1],
                              version, f"{HUB}/n/{name}", detail))
    return updates, []


def parse_release_pointer(text: str) -> tuple[int, str]:
    candidates = [(number, line) for number, line in enumerate(text.splitlines(), 1)
                  if "Latest stable release:" in line]
    if len(candidates) != 1:
        raise CheckError("Expected exactly one 'Latest stable release' link in README")
    number, line = candidates[0]
    matches = list(RELEASE_POINTER.finditer(line))
    if len(matches) != 1 or line.count("Latest stable release:") != 1:
        raise CheckError("Malformed 'Latest stable release' link in README")
    display, tag = matches[0].groups()
    if tag != f"v{display}":
        raise CheckError("Latest stable release label disagrees with its linked tag")
    return number, tag


def check_release(pointer: tuple[int, str], data: bytes) -> list[Update]:
    release = load_json(data)
    tag = release.get("tag_name")
    if (release.get("draft") is not False or release.get("prerelease") is not False
            or not isinstance(tag, str) or not re.fullmatch("v" + RELEASE_VERSION, tag)):
        raise CheckError("Expected an official, non-draft, non-prerelease Bend release")
    line, current = pointer
    # GitHub's designated latest release need not be the numerically largest tag.
    if tag == current:
        return []
    return [Update(line, "Bend stable release", current, tag, RELEASE_ROOT + tag,
                   "Official latest release differs; review the top-level release link")]


def cell(value: str) -> str:
    """Render untrusted errors as text, not Markdown links or table structure."""
    return html.escape(value).translate(str.maketrans({
        "\n": " ", "\r": " ", "|": "&#124;", "`": "&#96;", "[": "&#91;",
        "]": "&#93;", "*": "&#42;", "_": "&#95;", "\\": "&#92;",
    }))


def report(refs: list[Reference], package_count: int, checked: int, release_status: str,
           updates: list[Update], failures: list[Failure]) -> str:
    named_count = sum(not HASH.fullmatch(ref.package) for ref in refs)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = ["# Version freshness", "",
             f"**Audit {'incomplete' if failures else 'complete'}.** {stamp}", "",
             f"- Named imports: {named_count}; package names checked: {checked}/{package_count}.",
             f"- Hash-only imports excluded from version ordering: {len(refs) - named_count}.",
             f"- Official Bend release pointer: {release_status}.", "",
             "This report finds review candidates, not compatible upgrades. Hash-only imports, "
             "renamed packages, source-release prose, and project compiler pins need manual review. "
             "No packages are installed or executed, and README's Last checked date is unchanged.", "",
             "## Updates to review", ""]
    if updates:
        lines.extend(["| README line | Package | Documented | Published latest | Review |",
                      "| --- | --- | --- | --- | --- |"])
        for item in sorted(updates, key=lambda item: (item.line, item.name)):
            lines.append(f"| {item.line} | {cell(item.name)} | {cell(item.current)} | "
                         f"[{cell(item.latest)}]({item.url}) | {cell(item.detail)} |")
    else:
        lines.append("No update candidates found in the successfully checked metadata."
                     if failures else "No update candidates found within the checked scope.")
    if failures:
        lines.extend(["", "## Audit errors", "", "Missing evidence is not an up-to-date result.", "",
                      "| README line | Error |", "| --- | --- |"])
        for failure in sorted(failures, key=lambda item: item.line):
            lines.append(f"| {failure.line} | {cell(failure.message)} |")
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("readme", nargs="?", type=Path, default=Path("README.md"))
    parser.add_argument("--bend-release", type=Path,
                        help="JSON from GitHub's bendlang/bend releases/latest endpoint")
    args = parser.parse_args(argv)
    refs, failures, updates = [], [], []
    groups: dict[str, list[Reference]] = {}
    checked = 0
    release_status = "not checked (pass --bend-release to include it)"
    text = None
    try:
        text = args.readme.read_text(encoding="utf-8")
        refs, failures, _ = parse_references(text)
    except (OSError, UnicodeError) as error:
        failures.append(Failure(1, str(error)))

    if args.bend_release:
        release_status = "incomplete"
        pointer = None
        if text is not None:
            try:
                pointer = parse_release_pointer(text)
                updates.extend(check_release(pointer, args.bend_release.read_bytes()))
                release_status = "checked against the official latest release"
            except (OSError, CheckError) as error:
                failures.append(Failure(pointer[0] if pointer else 1, f"Bend release: {error}"))

    for ref in refs:
        if not HASH.fullmatch(ref.package):
            groups.setdefault(ref.package.split("@", 1)[0], []).append(ref)
    client = HubClient()
    with ThreadPoolExecutor(max_workers=4) as executor:
        for candidates, errors in executor.map(lambda group: check_name(group, client.fetch), groups.values()):
            updates.extend(candidates)
            failures.extend(errors)
            checked += not errors

    filename = escape_annotation(str(args.readme), property=True)
    for item in updates:
        message = f"{item.name}: {item.current} -> {item.latest}. {item.detail}"
        print(f"::notice file={filename},line={item.line}::{escape_annotation(message)}")
    for failure in failures:
        print(f"::error file={filename},line={failure.line}::{escape_annotation(failure.message)}")
    summary = report(refs, len(groups), checked, release_status, updates, failures)
    print(summary)
    if path := os.environ.get("GITHUB_STEP_SUMMARY"):
        try:
            with Path(path).open("a", encoding="utf-8") as output:
                output.write(summary)
        except OSError as error:
            print(f"Cannot write job summary: {error}", file=sys.stderr)
            return 1
    return int(bool(failures))


if __name__ == "__main__":
    sys.exit(main())
