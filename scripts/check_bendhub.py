#!/usr/bin/env python3
"""Verify the published BendHub references in README without executing packages."""

from __future__ import annotations

import argparse
import hashlib
import html
import os
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
IMPORT_FILE = r"(?:[A-Za-z_][A-Za-z0-9_-]*/)*[A-Za-z_][A-Za-z0-9_-]*\.bend"
IMPORT_PATH = re.compile(IMPORT_FILE + r"\Z")
RELATIVE_PATH = re.compile(r"(?:\./(?:\.\./)*|(?:\.\./)+)" + IMPORT_FILE + r"\Z")
FILE_HASH = re.compile(r"[0-9a-f]{64}\Z")
PLACEHOLDERS = {"name@version/file.bend", "0x…/file.bend"}
MAX_BYTES = 4 * 1024 * 1024


class CheckError(Exception):
    """A reference could not be verified."""


class UnavailableError(CheckError):
    """Temporary service or transport failure; the reference is unverified."""


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
    transient: bool = False


def safe_path(path: str) -> bool:
    return bool(path) and all(
        part not in {".", ".."} and PATH_PART.fullmatch(part)
        for part in path.split("/")
    )


def parse_references(text: str, *, allow_empty: bool = False) -> tuple[list[Reference], list[Failure], int]:
    references, failures = [], []
    placeholders = 0
    for number, line in enumerate(text.splitlines(), 1):
        # Extract first, then validate: a misspelled version must not disappear.
        snippets = [span.strip() for span in re.findall(r"`+([^`\r\n]*)`+", line)
                    if re.match(r"import\b", span.strip())]
        if re.match(r"^\s*import(?:\s|$)", line):
            snippets.append(line.strip())
        for snippet in snippets:
            match = re.fullmatch(r"import\s+(\S+)(?:\s+as\s+([A-Za-z_][A-Za-z0-9_]*))?(?:\s+#.*)?", snippet)
            if match is None:
                failures.append(Failure(number, f"Invalid BendHub import: {snippet!r}"))
                continue
            target = match.group(1)
            # Bend's book_load accepts Base and explicit relative paths with an alias.
            # Exclude only these known local forms; malformed Hub references still fail.
            if (target == "Base" and match.group(2) is None
                    or RELATIVE_PATH.fullmatch(target) and match.group(2) is not None):
                continue
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
    if not references and not failures and not allow_empty:
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
                transient = error.code in {408, 425, 429} or 500 <= error.code < 600
                retryable = transient or error.code == 404
                detail = f"HTTP {error.code}"
                retry_after = error.headers.get("Retry-After", "") if error.headers else ""
                error.close()
            except (URLError, OSError, HTTPException) as error:
                retryable = True
                transient = True
                detail = str(error)
                retry_after = ""
            if not retryable or attempt == 2:
                error_type = UnavailableError if transient else CheckError
                raise error_type(f"Could not verify {url}: {detail} (after {attempt + 1} attempt(s))")
            delay = min(int(retry_after), 10) if retry_after.isascii() and retry_after.isdigit() else attempt + 1
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
        return [Failure(ref.line, f"{ref.target}: {error}", isinstance(error, UnavailableError))
                for ref in references]

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
            failures.extend(Failure(ref.line, f"{ref.target}: {error}", isinstance(error, UnavailableError))
                            for ref in refs)
    return failures


def escape_annotation(text: str, *, property: bool = False) -> str:
    text = text.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
    return text.replace(",", "%2C").replace(":", "%3A") if property else text


def print_failures(failures: list[Failure], readme: Path) -> int:
    """Keep unavailable evidence separate from reference errors, including in CI."""
    actions = os.environ.get("GITHUB_ACTIONS") == "true"
    hard = [failure for failure in failures if not failure.transient]
    temporary = [failure for failure in failures if failure.transient]
    filename = escape_annotation(str(readme), property=True)
    for failure in sorted(hard, key=lambda item: item.line):
        if actions:
            print(f"::error file={filename},line={failure.line}::{escape_annotation(failure.message)}")
        else:
            print(f"{readme}:{failure.line}: {failure.message}")
    if temporary:
        message = (f"BendHub is temporarily unavailable for {len(temporary)} reference(s). "
                   "These imports remain unverified; retry when the service is available.")
        print(f"::warning::{escape_annotation(message)}" if actions else message)
        for failure in sorted(temporary, key=lambda item: item.line):
            # One physical line prevents response text from creating Actions commands.
            detail = f"  {readme}:{failure.line}: {failure.message}".replace("\r", "\\r").replace("\n", "\\n")
            print(detail)
    if hard:
        print(f"BendHub verification failed: {len(hard)} reference error(s); "
              f"{len(temporary)} temporarily unverified.")
        return 1
    return 3 if temporary else 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("readme", nargs="?", type=Path, default=Path("README.md"))
    parser.add_argument("--offline", action="store_true", help="Check Hub reference syntax without any network requests")
    parser.add_argument("--base-readme", type=Path,
                        help="Verify only import targets absent from this base README")
    args = parser.parse_args(argv)
    references, selected = [], []
    mode = "Offline syntax" if args.offline else "New or changed imports" if args.base_readme else "Full catalog"
    comparison_note = ""

    def finish(failures: list[Failure], note: str, *, attempted: int = 0, source=None) -> int:
        source = args.readme if source is None else source
        code = print_failures(failures, source) if failures else 0
        if comparison_note:
            note = comparison_note + "\n\n" + note
        print(note)
        if destination := os.environ.get("GITHUB_STEP_SUMMARY"):
            state = "Failed" if code == 1 else "Incomplete" if code == 3 else "Complete"
            verified = max(0, attempted - len(failures))
            lines = ["# BendHub imports", "", f"**{state}.** Scope: {mode}.", "",
                     f"Concrete imports parsed: {len(references)}. Live checks attempted: {attempted}. "
                     f"Verified: {verified}.",
                     f"Reference errors: {sum(not item.transient for item in failures)}. "
                     f"Temporarily unverified: {sum(item.transient for item in failures)}.", "", note]
            if failures:
                details = "\n".join(f"{source}:{item.line}: {item.message}" for item in failures)
                lines.extend(["", "<details><summary>Reference details</summary>", "",
                              "<pre>" + html.escape(details) + "</pre>", "", "</details>"])
            try:
                with Path(destination).open("a", encoding="utf-8") as output:
                    output.write("\n".join(lines) + "\n")
            except OSError as error:
                print(f"Cannot write job summary: {error}", file=sys.stderr)
                return 1
        return code

    try:
        references, failures, placeholders = parse_references(args.readme.read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as error:
        return finish([Failure(1, f"Cannot read README: {error}")], "No network verification was performed.")
    if failures:
        return finish(failures, "Fix the import syntax before retrying; no network verification was performed.")

    selected = references
    if args.base_readme is not None:
        try:
            # A real, valid base can predate the catalog's first published import.
            previous, errors, _ = parse_references(args.base_readme.read_text(encoding="utf-8"), allow_empty=True)
        except UnicodeError:
            previous, errors = [], [Failure(1, "Base README is not valid UTF-8")]
        except OSError as error:
            return finish([Failure(1, f"Cannot read base README: {error}")],
                          "Cannot compare imports without the real base README; no network verification was performed.",
                          source=args.base_readme)
        if errors:
            # A broken base must not prevent a change that repairs it.
            if args.offline:
                comparison_note = ("The base README is invalid; "
                                   "the current README's full syntax was checked instead.")
            else:
                mode = "Full catalog (base README invalid)"
                comparison_note = ("The base README is invalid; "
                                   "every current import is selected for verification so this change can repair it.")
        else:
            old_targets = {reference.target for reference in previous}
            selected = [reference for reference in references if reference.target not in old_targets]
    if args.offline:
        return finish([], f"Hub reference syntax valid: {len(references)} BendHub references; "
                      f"{placeholders} generic examples excluded. "
                      "Publication and integrity were not checked (--offline).")
    if not selected:
        return finish([], "No new or changed BendHub imports; network verification skipped.")

    packages: dict[str, list[Reference]] = {}
    for ref in selected:
        packages.setdefault(ref.package, []).append(ref)
    client = HubClient()
    scope = "new or changed " if mode == "New or changed imports" else ""
    print(f"Checking {len(selected)} {scope}imports across {len(packages)} packages; "
          f"{placeholders} generic examples excluded.", flush=True)
    with ThreadPoolExecutor(max_workers=4) as executor:
        for result in executor.map(lambda group: check_package(group, client.fetch), packages.values()):
            failures.extend(result)
    if failures:
        return finish(failures, "Unavailable imports remain unverified; reference errors require a corrected import.",
                      attempted=len(selected))
    return finish([], f"Verified all {len(selected)} checked references: package, manifest, file, and SHA-256.",
                  attempted=len(selected))


if __name__ == "__main__":
    sys.exit(main())
