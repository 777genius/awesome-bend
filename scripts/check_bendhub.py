#!/usr/bin/env python3
"""Verify the published BendHub references in README without executing packages."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from functools import cache
from http.client import HTTPException
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import HTTPRedirectHandler, Request, build_opener

HUB = "https://hub.bend-lang.com"
HASH = re.compile(r"0x[0-9a-f]{32}\Z")
VERSION = r"(?:0|[1-9][0-9]*)(?:\.(?:0|[1-9][0-9]*)){3}"
NAMED_PACKAGE = re.compile(r"[a-z][a-z0-9-]{0,63}@" + VERSION + r"\Z")
PATH_PART = re.compile(r"[A-Za-z0-9_.-]+\Z")
IMPORT_PATH = re.compile(r"(?:[A-Za-z_][A-Za-z0-9_-]*/)*[A-Za-z_][A-Za-z0-9_-]*\.bend\Z")
FILE_HASH = re.compile(r"[0-9a-f]{64}\Z")
PLACEHOLDERS = {"name@version/file.bend", "0x…/file.bend"}
MAX_BYTES = 4 * 1024 * 1024


class CheckError(Exception):
    """A reference could not be verified."""


@dataclass(frozen=True)
class Reference:
    target: str
    line: int
    package: str
    path: str


@dataclass(frozen=True)
class Failure:
    line: int
    message: str


def safe_path(path: str) -> bool:
    return bool(path) and all(
        part not in {".", ".."} and PATH_PART.fullmatch(part)
        for part in path.split("/")
    )


def parse_references(text: str) -> tuple[list[Reference], list[Failure], int]:
    references, failures = [], []
    placeholders = 0
    for number, line in enumerate(text.splitlines(), 1):
        # Extract first, then validate: a misspelled version must not disappear.
        snippets = [span.strip() for span in re.findall(r"`+([^`\r\n]*)`+", line)
                    if re.match(r"import\b", span.strip())]
        if re.match(r"^\s*import(?:\s|$)", line):
            snippets.append(line.strip())
        for snippet in snippets:
            match = re.fullmatch(r"import\s+(\S+)(?:\s+as\s+[A-Za-z_][A-Za-z0-9_]*)?", snippet)
            if match is None:
                failures.append(Failure(number, f"Invalid BendHub import: {snippet!r}"))
                continue
            target = match.group(1)
            if target in PLACEHOLDERS:
                placeholders += 1
                continue
            package, separator, path = target.partition("/")
            if (
                not separator
                or not (HASH.fullmatch(package) or NAMED_PACKAGE.fullmatch(package))
                or not IMPORT_PATH.fullmatch(path)
            ):
                failures.append(Failure(number, f"Invalid BendHub reference: {target!r}"))
                continue
            references.append(Reference(target, number, package, path))
    if not references and not failures:
        failures.append(Failure(1, "No concrete BendHub imports found in README."))
    return references, failures, placeholders


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # README and registry data must never redirect CI to another service.
        return None


class HubClient:
    def __init__(self, opener=None, sleep=time.sleep):
        self.opener = opener if opener is not None else build_opener(NoRedirect())
        self.sleep = sleep

    @cache
    def fetch(self, relative_path: str) -> bytes:
        url = f"{HUB}/{quote(relative_path, safe='/@.-')}"
        request = Request(url, headers={"User-Agent": "awesome-bend-hub-check/1.0"})
        for attempt in range(3):
            try:
                with self.opener.open(request, timeout=10) as response:
                    data = response.read(MAX_BYTES + 1)
                if len(data) > MAX_BYTES:
                    raise CheckError(f"Response exceeds {MAX_BYTES} bytes: {url}")
                return data
            except HTTPError as error:
                retryable = error.code in {404, 408, 425, 429} or 500 <= error.code < 600
                detail = f"HTTP {error.code}"
                retry_after = error.headers.get("Retry-After", "") if error.headers else ""
                error.close()
            except (URLError, OSError, HTTPException) as error:
                retryable = True
                detail = str(error)
                retry_after = ""
            if not retryable or attempt == 2:
                raise CheckError(f"Could not verify {url}: {detail} (after {attempt + 1} attempt(s))")
            delay = min(int(retry_after), 10) if retry_after.isdigit() else attempt + 1
            self.sleep(delay)
        raise AssertionError("unreachable")


def read_manifest(package_hash: str, data: bytes) -> dict[str, str]:
    # Bend hashes the original bytes, including the final newline, to identify a package.
    if hashlib.sha256(data).hexdigest()[:32] != package_hash[2:]:
        raise CheckError(f"Manifest checksum does not match package {package_hash}")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise CheckError("Manifest is not valid UTF-8") from error
    files = {}
    for line in text.splitlines():
        digest, separator, path = line.partition(" ")
        if not separator or not FILE_HASH.fullmatch(digest) or not safe_path(path):
            raise CheckError(f"Malformed manifest record: {line!r}")
        if path in files:
            raise CheckError(f"Duplicate manifest path: {path}")
        files[path] = digest
    return files


def check_package(references: list[Reference], fetch) -> list[Failure]:
    package = references[0].package
    try:
        if HASH.fullmatch(package):
            package_hash = package
        else:
            try:
                package_hash = fetch(f"name/{package}").decode("ascii").strip()
            except UnicodeDecodeError as error:
                raise CheckError(f"Invalid hash returned for {package}") from error
            if not HASH.fullmatch(package_hash):
                raise CheckError(f"Invalid hash returned for {package}: {package_hash!r}")
        manifest = read_manifest(package_hash, fetch(f"{package_hash}/manifest"))
    except CheckError as error:
        return [Failure(ref.line, f"{ref.target}: {error}") for ref in references]

    failures = []
    paths: dict[str, list[Reference]] = {}
    for ref in references:
        paths.setdefault(ref.path, []).append(ref)
    for path, refs in paths.items():
        try:
            if path not in manifest:
                raise CheckError(f"File is absent from the published manifest: {path}")
            data = fetch(f"{package_hash}/{path}")
            if hashlib.sha256(data).hexdigest() != manifest[path]:
                raise CheckError(f"File checksum does not match its manifest: {path}")
        except CheckError as error:
            failures.extend(Failure(ref.line, f"{ref.target}: {error}") for ref in refs)
    return failures


def escape_annotation(text: str, *, property: bool = False) -> str:
    text = text.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
    return text.replace(",", "%2C").replace(":", "%3A") if property else text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("readme", nargs="?", type=Path, default=Path("README.md"))
    args = parser.parse_args()
    try:
        references, failures, placeholders = parse_references(args.readme.read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as error:
        print(f"Cannot read {args.readme}: {error}", file=sys.stderr)
        return 1

    packages: dict[str, list[Reference]] = {}
    for ref in references:
        packages.setdefault(ref.package, []).append(ref)
    client = HubClient()
    print(f"Checking {len(references)} imports across {len(packages)} packages; "
          f"{placeholders} generic examples excluded.", flush=True)
    with ThreadPoolExecutor(max_workers=4) as executor:
        for result in executor.map(lambda group: check_package(group, client.fetch), packages.values()):
            failures.extend(result)
    for failure in sorted(failures, key=lambda item: item.line):
        print(f"::error file={escape_annotation(str(args.readme), property=True)},"
              f"line={failure.line}::{escape_annotation(failure.message)}")
    if failures:
        print(f"BendHub verification failed: {len(failures)} reference error(s).")
        return 1
    print(f"Verified all {len(references)} references: package, manifest, file, and SHA-256.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
