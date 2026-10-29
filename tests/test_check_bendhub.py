"""Offline regressions for catalog validation and the BendHub wire protocol."""

import hashlib
import io
from http.client import BadStatusLine, IncompleteRead
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock
from urllib.error import HTTPError, URLError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import check_bendhub as checker


def package_fixture(files):
    manifest = "".join(f"{hashlib.sha256(data).hexdigest()} {path}\n"
                       for path, data in files.items()).encode()
    package_hash = "0x" + hashlib.sha256(manifest).hexdigest()[:32]
    responses = {f"{package_hash}/manifest": manifest}
    responses.update({f"{package_hash}/{path}": data for path, data in files.items()})
    return package_hash, responses


class ReferenceTests(unittest.TestCase):
    def test_named_hash_nested_and_bare_references(self):
        text = "\n".join([
            "- Tensor `import bend-ml-tensor-array@0.1.18.0/main.bend`.",
            "- Hash `import 0x07516e23611e5287ce89bcff661be83f/BendSR.bend`.",
            "import cli@0.1.0.0/src/cli.bend as CLI",
        ])
        refs, errors, examples = checker.parse_references(text)
        self.assertEqual(errors, [])
        self.assertEqual(examples, 0)
        self.assertEqual([ref.line for ref in refs], [1, 2, 3])
        self.assertEqual(refs[1].package, "0x07516e23611e5287ce89bcff661be83f")
        self.assertEqual(refs[2].path, "src/cli.bend")

    def test_only_exact_documented_placeholders_are_excluded(self):
        refs, errors, examples = checker.parse_references(
            "`import name@version/file.bend` `import 0x…/file.bend` "
            "`import tensor@1.2.3.4/main.bend` `import tensor@version/main.bend`"
        )
        self.assertEqual((len(refs), len(errors), examples), (1, 1, 2))

    def test_padded_markdown_spans_do_not_hide_invalid_imports(self):
        refs, errors, _ = checker.parse_references(
            "` import tensor@1.2.3.4/main.bend ` and ` import tensor@1.2.3/main.bend `"
        )
        self.assertEqual((len(refs), len(errors)), (1, 1))

    def test_malformed_references_fail_instead_of_being_skipped(self):
        targets = [
            "tensor@1.2.3/main.bend", "tensor@1.2.3.4.5/main.bend",
            "tensor@01.2.3.4/main.bend", "Tensor@1.2.3.4/main.bend",
            "tensor@1.2.3.4/../main.bend", "tensor@1.2.3.4/src/./main.bend",
            "tensor@1.2.3.4//main.bend", "tensor@1.2.3.4/%2e%2e/main.bend",
            "tensor@1.2.3.4/main.bend?x=1", "tensor@1.2.3.4/main.bend#x",
            "tensor@1.2.3.4/maín.bend", "tensor@1.2.3.4/main.js",
            "tensor@1.2.3.4/1main.bend", "tensor@1.2.3.4/src.dir/main.bend",
            "tensor@1.2.3.4/main.part.bend", "tensor@1.2.3.4/main.bend as 1Alias",
            "tensor@1.2.3.4 /main.bend", "https://example.com/main.bend",
            "0x1234/main.bend", "tensor@1.2.3.4\\main.bend", "",
        ]
        for target in targets:
            with self.subTest(target=target):
                refs, errors, _ = checker.parse_references(f"`import {target}`")
                self.assertEqual(refs, [])
                self.assertEqual(len(errors), 1)

    def test_empty_inventory_is_not_a_success(self):
        self.assertEqual(len(checker.parse_references("No imports here.")[1]), 1)


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.package_hash, self.responses = package_fixture({"main.bend": b"value = 42\n"})
        self.responses["name/example@1.2.3.4"] = (self.package_hash + "\n").encode()
        self.ref = checker.Reference("example@1.2.3.4/main.bend", 7, "example@1.2.3.4", "main.bend")

    def test_named_reference_and_both_checksums(self):
        self.assertEqual(checker.check_package([self.ref], self.responses.__getitem__), [])

    def test_hash_reference_does_not_resolve_a_name(self):
        ref = checker.Reference(f"{self.package_hash}/main.bend", 3, self.package_hash, "main.bend")
        del self.responses["name/example@1.2.3.4"]
        self.assertEqual(checker.check_package([ref], self.responses.__getitem__), [])

    def test_invalid_alias_response(self):
        for response in [b"<html>not a hash</html>", b"0x1234", b"\xff"]:
            with self.subTest(response=response):
                self.responses["name/example@1.2.3.4"] = response
                errors = checker.check_package([self.ref], self.responses.__getitem__)
                self.assertIn("Invalid hash", errors[0].message)

    def test_original_manifest_bytes_matter(self):
        key = f"{self.package_hash}/manifest"
        self.responses[key] = self.responses[key].rstrip(b"\n")
        errors = checker.check_package([self.ref], self.responses.__getitem__)
        self.assertIn("Manifest checksum", errors[0].message)

    def test_file_must_be_in_a_valid_manifest(self):
        ref = checker.Reference("example@1.2.3.4/missing.bend", 8, self.ref.package, "missing.bend")
        errors = checker.check_package([ref], self.responses.__getitem__)
        self.assertIn("absent", errors[0].message)

    def test_http_200_with_wrong_file_bytes_fails(self):
        self.responses[f"{self.package_hash}/main.bend"] = b"<html>Unavailable</html>"
        errors = checker.check_package([self.ref], self.responses.__getitem__)
        self.assertIn("File checksum", errors[0].message)

    def test_duplicate_references_fetch_once_and_keep_each_line(self):
        duplicate = checker.Reference(self.ref.target, 18, self.ref.package, self.ref.path)
        self.responses[f"{self.package_hash}/main.bend"] = b"wrong"
        fetch = Mock(side_effect=self.responses.__getitem__)
        errors = checker.check_package([self.ref, duplicate], fetch)
        self.assertEqual([error.line for error in errors], [7, 18])
        self.assertEqual(fetch.call_count, 3)

    def test_one_missing_file_does_not_hide_other_files(self):
        missing = checker.Reference("example@1.2.3.4/absent.bend", 4, self.ref.package, "absent.bend")
        errors = checker.check_package([missing, self.ref], self.responses.__getitem__)
        self.assertEqual([error.line for error in errors], [4])

    def test_unavailable_package_preserves_reference_location(self):
        errors = checker.check_package([self.ref], Mock(side_effect=checker.CheckError("HTTP 404")))
        self.assertEqual(errors[0].line, 7)
        self.assertIn("HTTP 404", errors[0].message)

    def test_malformed_or_duplicate_manifest_records(self):
        record = hashlib.sha256(b"x").hexdigest() + " main.bend\n"
        for manifest in [b"not a manifest\n", (record * 2).encode(),
                         (record.replace("main.bend", "../main.bend")).encode()]:
            with self.subTest(manifest=manifest):
                package_hash = "0x" + hashlib.sha256(manifest).hexdigest()[:32]
                with self.assertRaises(checker.CheckError):
                    checker.read_manifest(package_hash, manifest)


class TransportTests(unittest.TestCase):
    def test_transient_error_recovers_then_caches(self):
        opener = Mock()
        opener.open.side_effect = [HTTPError("url", 503, "unavailable", {}, None), io.BytesIO(b"ok")]
        sleep = Mock()
        client = checker.HubClient(opener, sleep)
        self.assertEqual(client.fetch("name/example@1.2.3.4"), b"ok")
        self.assertEqual(client.fetch("name/example@1.2.3.4"), b"ok")
        self.assertEqual(opener.open.call_count, 2)
        sleep.assert_called_once_with(1)
        self.assertTrue(opener.open.call_args.args[0].full_url.startswith(checker.HUB + "/"))

    def test_retry_after_is_bounded(self):
        opener = Mock()
        opener.open.side_effect = [HTTPError("url", 429, "rate limited", {"Retry-After": "999"}, None), io.BytesIO(b"ok")]
        sleep = Mock()
        checker.HubClient(opener, sleep).fetch("example")
        sleep.assert_called_once_with(10)

    def test_truncated_http_body_is_retried(self):
        opener = Mock()
        opener.open.side_effect = [IncompleteRead(b"partial", 20), io.BytesIO(b"complete")]
        self.assertEqual(checker.HubClient(opener, Mock()).fetch("example"), b"complete")
        self.assertEqual(opener.open.call_count, 2)

    def test_other_http_protocol_errors_are_retried(self):
        opener = Mock()
        opener.open.side_effect = [BadStatusLine("invalid response"), io.BytesIO(b"complete")]
        self.assertEqual(checker.HubClient(opener, Mock()).fetch("example"), b"complete")
        self.assertEqual(opener.open.call_count, 2)

    def test_retry_exhaustion_fails(self):
        for error in [URLError("timeout"), HTTPError("url", 404, "not found", {}, None),
                      IncompleteRead(b"partial", 20), BadStatusLine("invalid response")]:
            with self.subTest(error=error):
                opener = Mock()
                opener.open.side_effect = error
                with self.assertRaisesRegex(checker.CheckError, "after 3 attempt"):
                    checker.HubClient(opener, Mock()).fetch("example")
                self.assertEqual(opener.open.call_count, 3)

    def test_permanent_error_is_not_retried(self):
        opener = Mock()
        opener.open.side_effect = HTTPError("url", 410, "gone", {}, None)
        with self.assertRaisesRegex(checker.CheckError, "HTTP 410"):
            checker.HubClient(opener, Mock()).fetch("example")
        self.assertEqual(opener.open.call_count, 1)

    def test_oversized_response_is_rejected(self):
        opener = Mock()
        opener.open.return_value = io.BytesIO(b"x" * (checker.MAX_BYTES + 1))
        with self.assertRaisesRegex(checker.CheckError, "exceeds"):
            checker.HubClient(opener, Mock()).fetch("example")

    def test_redirects_are_rejected(self):
        self.assertIsNone(checker.NoRedirect().redirect_request(None, None, 302, "", {}, "http://127.0.0.1/"))

    def test_annotations_cannot_inject_commands(self):
        self.assertEqual(checker.escape_annotation("bad%\n::error::oops\r"), "bad%25%0A::error::oops%0D")
        self.assertEqual(checker.escape_annotation("a,b:c", property=True), "a%2Cb%3Ac")


if __name__ == "__main__":
    unittest.main()
