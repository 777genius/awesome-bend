"""Offline regressions for catalog validation and the BendHub wire protocol."""

import hashlib
import io
from http.client import BadStatusLine, IncompleteRead
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import Mock, patch
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

    def test_known_base_and_explicit_local_imports_are_not_hub_references(self):
        text = "\n".join(["import Base # Standard library", "import ./local.bend as Local # Local module",
                          "import ../shared/lib.bend as Shared", "import ./../upper.bend as Upper",
                          "`import tensor@1.2.3.4/main.bend`"])
        refs, errors, examples = checker.parse_references(text)
        self.assertEqual(([ref.target for ref in refs], errors, examples),
                         (["tensor@1.2.3.4/main.bend"], [], 0))
        for target in ["Base as Alias", "./local.bend", "./package@bad/main.bend as P",
                       "../foo/../main.bend as P", "./file.bend?x=1 as P", "./1file.bend as P"]:
            with self.subTest(target=target):
                self.assertEqual(len(checker.parse_references("import " + target)[1]), 1)


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

    def test_temporary_failure_type_survives_every_fetch_stage(self):
        for unavailable in ["name/example@1.2.3.4", f"{self.package_hash}/manifest",
                            f"{self.package_hash}/main.bend"]:
            with self.subTest(unavailable=unavailable):
                def fetch(path):
                    if path == unavailable:
                        raise checker.UnavailableError("HTTP 503")
                    return self.responses[path]
                errors = checker.check_package([self.ref], fetch)
                self.assertEqual([(item.line, item.transient) for item in errors], [(7, True)])
        errors = checker.check_package([self.ref], Mock(side_effect=checker.CheckError("HTTP 404")))
        self.assertFalse(errors[0].transient)

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

    def test_only_known_temporary_failures_are_classified_as_unavailable(self):
        for error in [URLError("timeout"), TimeoutError("timed out"), BadStatusLine("bad status"),
                      *(HTTPError("url", code, "unavailable", {}, None) for code in [408, 425, 429, 500, 503])]:
            with self.subTest(error=error):
                opener = Mock()
                opener.open.side_effect = error
                with self.assertRaises(checker.UnavailableError):
                    checker.HubClient(opener, Mock()).fetch("example")
        for code in [301, 400, 403, 404, 410]:
            with self.subTest(code=code):
                opener = Mock()
                opener.open.side_effect = HTTPError("url", code, "unavailable", {}, None)
                with self.assertRaises(checker.CheckError) as caught:
                    checker.HubClient(opener, Mock()).fetch("example")
                self.assertNotIsInstance(caught.exception, checker.UnavailableError)

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


class CommandTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.readme, self.base, self.summary = [self.root / name for name in ["README.md", "base.md", "summary.md"]]
        self.package_hash, self.responses = package_fixture({"main.bend": b"one", "next.bend": b"two"})
        for version in ["1.2.3.4", "1.2.3.5"]:
            self.responses[f"name/example@{version}"] = self.package_hash.encode()
        self.reference = "`import example@1.2.3.4/main.bend`"

    def run_check(self, text, options=(), *, fetch=None, actions=False):
        self.readme.write_text(text, encoding="utf-8")
        if self.summary.is_file():
            self.summary.unlink()
        output = io.StringIO()
        fetch = Mock(side_effect=AssertionError("Unexpected network request")) if fetch is None else fetch
        env = {"GITHUB_ACTIONS": "true" if actions else "false", "GITHUB_STEP_SUMMARY": str(self.summary)}
        with patch.object(checker, "HubClient", return_value=Mock(fetch=fetch)) as client, \
                patch.dict(os.environ, env), redirect_stdout(output), redirect_stderr(output):
            code = checker.main([str(self.readme), *map(str, options)])
        summary = self.summary.read_text() if self.summary.is_file() else ""
        return code, output.getvalue(), summary, client

    def test_offline_checks_real_input_and_never_fetches(self):
        code, output, summary, client = self.run_check(self.reference, ["--offline"])
        self.assertEqual(code, 0)
        client.assert_not_called()
        self.assertNotIn("::", output)
        self.assertIn("Scope: Offline syntax", summary)
        self.assertIn("Live checks attempted: 0. Verified: 0", summary)
        self.assertIn("Publication and integrity were not checked", summary)

    def test_syntax_errors_fail_before_any_network_in_all_modes(self):
        self.base.write_text(self.reference)
        for options in [[], ["--offline"], ["--base-readme", self.base]]:
            with self.subTest(options=options):
                code, output, summary, client = self.run_check(
                    self.reference + "\n`import example@1.2.3/main.bend`", options)
                self.assertEqual(code, 1)
                client.assert_not_called()
                self.assertIn("Invalid BendHub reference", output)
                self.assertIn("**Failed.**", summary)

    def test_prose_moves_and_duplicate_existing_targets_do_not_fetch(self):
        self.base.write_text("Original prose " + self.reference)
        code, _, summary, client = self.run_check(
            "Changed prose\n\n" + self.reference + "\nDuplicate " + self.reference,
            ["--base-readme", self.base])
        self.assertEqual(code, 0)
        client.assert_not_called()
        self.assertIn("Scope: New or changed imports", summary)
        self.assertIn("Live checks attempted: 0. Verified: 0", summary)
        self.assertIn("No new or changed BendHub imports", summary)

    def test_old_unavailable_import_does_not_fail_valid_new_target(self):
        old = "`import old-library@1.0.0.0/main.bend`"
        self.base.write_text(old)
        def fetch(path):
            if path.startswith("name/old-library"):
                raise checker.UnavailableError("HTTP 503")
            return self.responses[path]
        mocked = Mock(side_effect=fetch)
        code, _, summary, _ = self.run_check(old + "\n" + self.reference,
                                            ["--base-readme", self.base], fetch=mocked)
        self.assertEqual(code, 0)
        self.assertIn("Concrete imports parsed: 2. Live checks attempted: 1. Verified: 1", summary)
        self.assertEqual(mocked.call_count, 3)
        self.assertNotIn("name/old-library@1.0.0.0", [item.args[0] for item in mocked.call_args_list])

    def test_new_versions_and_paths_are_verified(self):
        self.base.write_text(self.reference)
        for target in ["example@1.2.3.5/main.bend", "example@1.2.3.4/next.bend"]:
            with self.subTest(target=target):
                fetch = Mock(side_effect=self.responses.__getitem__)
                code, _, summary, _ = self.run_check(f"`import {target}`",
                                                    ["--base-readme", self.base], fetch=fetch)
                self.assertEqual(code, 0)
                self.assertIn("Verified: 1", summary)
                self.assertIn("name/" + target.split("/")[0], [item.args[0] for item in fetch.call_args_list])
                self.assertIn(self.package_hash + "/" + target.split("/", 1)[1],
                              [item.args[0] for item in fetch.call_args_list])

    def test_missing_base_is_not_silently_empty(self):
        code, _, summary, client = self.run_check(self.reference, ["--base-readme", self.base])
        self.assertEqual(code, 1)
        self.assertIn("**Failed.**", summary)
        client.assert_not_called()

    def test_bad_base_import_can_be_repaired_with_full_verification(self):
        self.base.write_text(self.reference + "\n`import example@bad/next.bend`")
        fetch = Mock(side_effect=self.responses.__getitem__)
        code, output, summary, _ = self.run_check(
            self.reference + "\n`import example@1.2.3.4/next.bend`",
            ["--base-readme", self.base], fetch=fetch)
        self.assertEqual(code, 0)
        self.assertIn("Scope: Full catalog (base README invalid)", summary)
        self.assertIn("Live checks attempted: 2. Verified: 2", summary)
        self.assertIn("every current import is selected", summary)
        self.assertNotIn("new or changed imports", output)
        for path in ["main.bend", "next.bend"]:
            self.assertIn(f"{self.package_hash}/{path}", [item.args[0] for item in fetch.call_args_list])

    def test_offline_mode_can_repair_bad_base_without_network(self):
        self.base.write_text("`import example@bad/main.bend`")
        code, _, summary, client = self.run_check(self.reference, ["--offline", "--base-readme", self.base])
        self.assertEqual(code, 0)
        client.assert_not_called()
        self.assertIn("Scope: Offline syntax", summary)
        self.assertIn("current README's full syntax was checked instead", summary)
        self.assertIn("Live checks attempted: 0. Verified: 0", summary)

    def test_invalid_base_encoding_also_uses_full_current_verification(self):
        self.base.write_bytes(b"\xff")
        fetch = Mock(side_effect=self.responses.__getitem__)
        code, _, summary, _ = self.run_check(self.reference, ["--base-readme", self.base], fetch=fetch)
        self.assertEqual(code, 0)
        self.assertIn("Scope: Full catalog (base README invalid)", summary)
        self.assertIn("Live checks attempted: 1. Verified: 1", summary)

    def test_valid_empty_base_allows_the_first_hub_import(self):
        self.base.write_text("No published imports yet.\nimport Base\n")
        code, _, summary, _ = self.run_check(self.reference, ["--base-readme", self.base],
                                            fetch=Mock(side_effect=self.responses.__getitem__))
        self.assertEqual(code, 0)
        self.assertIn("Live checks attempted: 1. Verified: 1", summary)

    def test_transient_only_has_distinct_exit_and_one_actions_warning(self):
        refs = self.reference + "\n" + self.reference
        problem = "timeout\n::error::injected <script>"
        for actions in [False, True]:
            with self.subTest(actions=actions):
                code, output, summary, _ = self.run_check(
                    refs, fetch=Mock(side_effect=checker.UnavailableError(problem)), actions=actions)
                self.assertEqual(code, 3)
                self.assertEqual(output.count("::warning::"), int(actions))
                self.assertNotIn("\n::error::", output)
                self.assertNotIn("::error file=", output)
                self.assertIn("**Incomplete.**", summary)
                self.assertIn("Verified: 0", summary)
                self.assertIn("Reference errors: 0. Temporarily unverified: 2", summary)
                self.assertNotIn("<script>", summary)

    def test_mixed_hard_and_transient_is_a_hard_failure(self):
        def fetch(path):
            if path.startswith("name/example"):
                raise checker.UnavailableError("HTTP 503")
            raise checker.CheckError("HTTP 404")
        code, output, summary, _ = self.run_check(
            self.reference + "\n`import missing@1.0.0.0/main.bend`", fetch=fetch, actions=True)
        self.assertEqual(code, 1)
        self.assertEqual(output.count("::warning::"), 1)
        self.assertEqual(output.count("::error file="), 1)
        self.assertIn("**Failed.**", summary)
        self.assertIn("Reference errors: 1. Temporarily unverified: 1", summary)

    def test_summary_write_failure_is_not_success(self):
        self.summary.mkdir()
        code, output, _, client = self.run_check(self.reference, ["--offline"])
        self.assertEqual(code, 1)
        self.assertIn("Cannot write job summary", output)
        client.assert_not_called()


if __name__ == "__main__":
    unittest.main()
