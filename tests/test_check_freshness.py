"""Offline contracts for advisory updates, incomplete audits, and report safety."""

import hashlib
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import check_freshness as checker


POINTER = ("Latest stable release: [Bend 2.0.39]"
           "(https://github.com/bendlang/bend/releases/tag/v2.0.39).")
RELEASE = {"tag_name": "v2.0.39", "draft": False, "prerelease": False}


def encode(value):
    return json.dumps(value).encode()


def reference(version="0.9.0.0", path="main.bend", line=3):
    package = f"example@{version}"
    return checker.Reference(f"{package}/{path}", line, package, path)


def publication(version="0.10.0.0"):
    manifest = f"{hashlib.sha256(b'code').hexdigest()} main.bend\n".encode()
    package_hash = "0x" + hashlib.sha256(manifest).hexdigest()[:32]
    metadata = {"name": "example", "latest": {"version": version, "hash": package_hash}}
    return metadata, {"name/example": encode(metadata), f"{package_hash}/manifest": manifest}


class PublicationTests(unittest.TestCase):
    def test_numeric_order_and_latest_field_instead_of_history_order(self):
        metadata, responses = publication()
        metadata["versions"] = [{"version": "0.9.0.0"}, {"version": "99.0.0.0"}]
        responses["name/example"] = encode(metadata)
        updates, errors = checker.check_name([reference()], responses.__getitem__)
        self.assertEqual(errors, [])
        self.assertEqual([(item.current, item.latest) for item in updates], [("0.9.0.0", "0.10.0.0")])

    def test_unchanged_version_does_not_download_a_manifest(self):
        _, responses = publication()
        fetch = Mock(side_effect=responses.__getitem__)
        self.assertEqual(checker.check_name([reference("0.10.0.0")], fetch), ([], []))
        fetch.assert_called_once_with("name/example")

    def test_grouped_versions_and_submodule_paths_use_one_manifest(self):
        metadata, responses = publication()
        metadata["latest"]["entry"] = "different.bend"
        responses["name/example"] = encode(metadata)
        refs = [reference(), reference("0.10.0.0", line=4),
                reference("0.8.0.0", "removed.bend", line=5)]
        fetch = Mock(side_effect=responses.__getitem__)
        updates, errors = checker.check_name(refs, fetch)
        self.assertEqual(errors, [])
        self.assertEqual([item.line for item in updates], [3, 5])
        self.assertIn("is present", updates[0].detail)
        self.assertIn("is absent", updates[1].detail)
        self.assertEqual(fetch.call_count, 2)

    def test_corrupt_newer_manifest_is_incomplete_not_a_verified_upgrade(self):
        metadata, responses = publication()
        responses[f"{metadata['latest']['hash']}/manifest"] = b"wrong bytes"
        updates, errors = checker.check_name([reference()], responses.__getitem__)
        self.assertEqual(updates, [])
        self.assertIn("checksum", errors[0].message)

    def test_bad_metadata_cannot_be_reported_as_current(self):
        metadata, _ = publication()
        latest = metadata["latest"]
        payloads = [b"not JSON", b"\xff", b"[]", b"null", b"42", b"{}",
                    b"[" * 2000 + b"0" + b"]" * 2000,
                    encode({"name": "wrong", "latest": latest}),
                    encode({"name": "example", "latest": None}),
                    encode({"name": "example", "latest": []})]
        for version in [None, 10, "0.10.0", "00.10.0.0", "0.10.0.0-beta"]:
            payloads.append(encode({"name": "example", "latest": {**latest, "version": version}}))
        for package_hash in [None, 42, "0x1234", "0x" + "A" * 32]:
            payloads.append(encode({"name": "example", "latest": {**latest, "hash": package_hash}}))
        for payload in payloads:
            with self.subTest(payload=payload):
                updates, errors = checker.check_name([reference()], Mock(return_value=payload))
                self.assertEqual(updates, [])
                self.assertEqual([error.line for error in errors], [3])

    def test_readme_ahead_of_registry_is_not_a_downgrade_candidate(self):
        _, responses = publication()
        updates, errors = checker.check_name([reference("1.0.0.0")], responses.__getitem__)
        self.assertEqual(updates, [])
        self.assertIn("inconsistent", errors[0].message)

    def test_network_failure_preserves_each_reference_location(self):
        fetch = Mock(side_effect=checker.CheckError("HTTP 404"))
        updates, errors = checker.check_name([reference(line=3), reference(line=10)], fetch)
        self.assertEqual(updates, [])
        self.assertEqual([error.line for error in errors], [3, 10])


class ReleaseTests(unittest.TestCase):
    def test_only_explicit_release_pointer_is_compared(self):
        text = "Requires exactly Bend 2.0.34.\nLast checked: today. " + POINTER
        pointer = checker.parse_release_pointer(text)
        self.assertEqual(pointer, (2, "v2.0.39"))
        self.assertEqual(checker.check_release(pointer, encode(RELEASE)), [])

    def test_missing_duplicate_or_mismatched_release_link_fails(self):
        invalid = ["No latest claim", POINTER + "\n" + POINTER, POINTER + " " + POINTER,
                   POINTER.replace("tag/v2.0.39", "tag/v2.0.38"),
                   POINTER.replace("github.com/bendlang", "example.com/bendlang")]
        for text in invalid:
            with self.subTest(text=text), self.assertRaises(checker.CheckError):
                checker.parse_release_pointer(text)

    def test_github_latest_designation_can_move_to_an_older_tag(self):
        updates = checker.check_release((9, "v2.0.39"), encode({**RELEASE, "tag_name": "v2.0.38"}))
        self.assertEqual([(item.line, item.latest) for item in updates], [(9, "v2.0.38")])
        self.assertEqual(updates[0].url, checker.RELEASE_ROOT + "v2.0.38")

    def test_nonstable_or_invalid_release_payload_fails(self):
        payloads = [{}, {**RELEASE, "draft": True}, {**RELEASE, "prerelease": True},
                    {**RELEASE, "draft": 0}, {**RELEASE, "tag_name": None},
                    {**RELEASE, "tag_name": "v2.0.40-rc1"}, {**RELEASE, "tag_name": "v2.0"}]
        for payload in payloads:
            with self.subTest(payload=payload), self.assertRaises(checker.CheckError):
                checker.check_release((1, "v2.0.39"), encode(payload))


class CommandTests(unittest.TestCase):
    def run_audit(self, readme, fetch, release=RELEASE):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, summary = root / "README.md", root / "summary.md"
            source.write_text(readme, encoding="utf-8")
            args = [str(source)]
            if release is not None:
                release_path = root / "release.json"
                release_path.write_bytes(encode(release))
                args.extend(["--bend-release", str(release_path)])
            stdout = io.StringIO()
            with patch.object(checker, "HubClient", return_value=Mock(fetch=fetch)), \
                    patch.dict(os.environ, {"GITHUB_STEP_SUMMARY": str(summary)}), redirect_stdout(stdout):
                code = checker.main(args)
            self.assertEqual(source.read_text(encoding="utf-8"), readme)
            return code, stdout.getvalue(), summary.read_text(encoding="utf-8")

    def test_updates_are_advisory_and_hash_only_coverage_is_explicit(self):
        _, responses = publication()
        refs = ["`import example@0.9.0.0/main.bend`", "`import example@0.8.0.0/main.bend`"]
        refs.extend(f"`import 0x{number:032x}/main.bend`" for number in range(12))
        fetch = Mock(side_effect=responses.__getitem__)
        code, stdout, summary = self.run_audit(POINTER + "\n" + "\n".join(refs), fetch)
        self.assertEqual(code, 0)
        self.assertIn("::notice file=", stdout)
        self.assertIn("**Audit complete.**", summary)
        self.assertIn("Named imports: 2; package names checked: 1/1", summary)
        self.assertIn("Hash-only imports excluded from version ordering: 12", summary)
        self.assertEqual(fetch.call_count, 2)

    def test_failed_network_is_incomplete_and_cannot_inject_annotations(self):
        problem = "bad%\r\n::warning::injected | [link](https://example.com) <img>"
        code, stdout, summary = self.run_audit(
            POINTER + "\n`import example@0.9.0.0/main.bend`",
            Mock(side_effect=checker.CheckError(problem)))
        self.assertEqual(code, 1)
        self.assertIn("**Audit incomplete.**", summary)
        self.assertIn("package names checked: 0/1", summary)
        self.assertIn("bad%25%0D%0A::warning::", stdout)
        for raw in ["\n::warning::", "[link]", "<img>"]:
            self.assertNotIn(raw, summary)
        self.assertIn("&#124;", summary)

    def test_release_failures_do_not_hide_successful_hub_coverage(self):
        _, responses = publication()
        code, _, summary = self.run_audit(POINTER + "\n`import example@0.10.0.0/main.bend`",
                                          Mock(side_effect=responses.__getitem__), release={})
        self.assertEqual(code, 1)
        self.assertIn("package names checked: 1/1", summary)
        self.assertIn("Official Bend release pointer: incomplete", summary)

    def test_hub_only_mode_explicitly_discloses_skipped_release_check(self):
        _, responses = publication()
        code, _, summary = self.run_audit(POINTER + "\n`import example@0.10.0.0/main.bend`",
                                          Mock(side_effect=responses.__getitem__), release=None)
        self.assertEqual(code, 0)
        self.assertIn("not checked (pass --bend-release", summary)

    def test_release_pointer_is_required_only_when_release_check_is_requested(self):
        _, responses = publication()
        for pointer in ["", "Latest stable release: a malformed link."]:
            for release, expected_code in [(None, 0), (RELEASE, 1)]:
                with self.subTest(pointer=pointer, release_requested=release is not None):
                    code, _, summary = self.run_audit(
                        pointer + "\n`import example@0.10.0.0/main.bend`",
                        Mock(side_effect=responses.__getitem__), release=release)
                    self.assertEqual(code, expected_code)
                    self.assertIn("package names checked: 1/1", summary)
                    self.assertIn("**Audit incomplete.**" if expected_code else "**Audit complete.**", summary)

    def test_malformed_imports_and_empty_inventory_fail(self):
        for extra in ["", "\n`import example@0.9/main.bend`"]:
            with self.subTest(extra=extra):
                fetch = Mock()
                code, _, summary = self.run_audit(POINTER + extra, fetch)
                self.assertEqual(code, 1)
                self.assertIn("**Audit incomplete.**", summary)
                fetch.assert_not_called()


if __name__ == "__main__":
    unittest.main()
