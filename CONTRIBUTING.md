# Contribution Guidelines

You can edit README directly on GitHub and open a pull request. CI checks the change automatically; installing local tools is optional.

Please ensure your pull request adheres to the following:

- **Current Bend only** (`bendlang/bend`, 2.0.x). Do not add Bend 1 / HVM2 (`HigherOrderCO/Bend`, `cargo install bend-lang`, `bend run-cu`), Bend 1 editor plugins, or unrelated “Bend” projects (Oregon, BendDAO, hardware Bender, …).
- Search previous suggestions before opening a new one. This is a curation, not a dump of every `bend2-*` repository.
- Use the format `- [Name](url) - Description.`
- The description starts with an uppercase character and ends with a period.
- Keep descriptions short and objective: what the project is, not a tagline.
- Add new items at the bottom of the relevant category.
- Check your spelling and grammar. Do not hard-wrap lines.
- For new entries, add one item per pull request, with a useful title (`Add bolt`, not `Update README.md`). Related corrections or maintenance changes can be grouped in one PR.
- A working example or README beats a star count. Empty, generated, or undocumented trees will be closed.
- If a library publishes to the hub, add its documented `import name@version/file.bend` or `import 0x…/file.bend` line next to the GitHub link. Verify that the version resolves and the file exists in its published manifest.
- State meaningful limitations, such as a development-only editor extension or a planned feature. A published package is not evidence that it works on every compiler release.
- When refreshing an entry, check its README and published imports. Fix moved links and remove only confirmed unavailable projects; temporary network errors or rate limits are not a reason to remove an entry.
- New categories, or improvements to the existing ones, are welcome.

## Version policy

Keep concrete imports pinned to an exact published version or content hash. A newer package is a candidate for review, not an automatic replacement: check its entrypoint, compiler requirements, and upstream documentation before updating the example. Compare versions within the same Hub package name; a repository release tag can differ from its published Hub version. Do not infer package renames or a newer release from a content hash.

Keeping a reviewed pin is fine. Explain a meaningful compatibility reason in the entry; contributors and agents do not need to empty the freshness report or update a working example just to remove a candidate. The report does not create issues, pull requests, or a notice for each outdated import.

Avoid repeating a release number in prose when the import already conveys it. Keep versions that explain a source-versus-Hub difference, minimum or exact compiler requirement, compiler patch, or tested configuration. Do not replace these with the latest compiler number. Update `Last checked` only after reviewing the list's descriptions and sources; a metadata-only freshness run is not a full audit.

## Validation

For a README edit, the PR checks validate formatting and any added or changed Hub references. An unrelated existing package does not need to be reachable for a description-only change. You do not need to run a full catalog or freshness audit before contributing.

For optional local checks, run these commands from the repository root:

```sh
python3 scripts/check_bendhub.py --offline
npx --yes awesome-lint@2.3.0
```

The syntax check needs only Python 3.10+ and its standard library; `npx` needs Node.js/npm and can download the pinned linter. The validator accepts the catalog's abbreviated package/file references. In Bend source, add `as Name` to a non-Base import; this check does not compile or type-check a program. Ordinary `Base` and aliased local imports, and the generic `name@version/file.bend` and `0x…/file.bend` examples, are outside Hub verification.

If you change the validators or workflows, also run their offline regression tests:

```sh
python3 -m unittest discover -s tests -v
```

CI obtains the base README automatically. For a local or agent comparison, `--base-readme PATH` accepts a real previous README and verifies only added or changed import targets; the whole current README still receives syntax validation.

### Optional full-catalog check

For maintenance, check publication and integrity across the entire list with:

```sh
python3 scripts/check_bendhub.py
```

This resolves the aliases, verifies the package manifests, and checks the referenced files' SHA-256 without executing packages. It can report problems in entries unrelated to your change. Publication and integrity do not establish compiler compatibility or proof correctness.

PRs and pushes check added or changed imports. Changes to the integrity checker or its workflow, weekly runs, and manual runs check the whole catalog. If the base README is unavailable or cannot be parsed, CI explicitly falls back to a full check of the current catalog. A temporary source failure leaves a PR or push check unsuccessful so a changed import is never silently accepted without verification. Scheduled and manual audits report temporary outages as incomplete without requiring a README edit.

## Version freshness

The separate **Version freshness** workflow checks named Hub imports and the README's explicit `Latest stable release` claim for Bend. It runs weekly, manually, and when its checker, tests, or workflow change on `main`. Routine README edits do not launch another freshness audit, and PRs run only its offline regression tests. It reads metadata without installing, compiling, or running packages, and writes optional update candidates to the Actions job summary.

Newer versions are successful audit results. Temporary source failures leave an explicit incomplete report and one grouped warning; they do not block this maintenance workflow. Invalid metadata or input, missing published references, and checksum failures still fail the relevant check. Hash-only imports have no version ordering and are counted as outside freshness coverage. Compatibility prose and repository release versions need manual review.

For an optional local maintenance audit, run the Hub-only check; without `--bend-release`, the compiler release check is explicitly skipped:

```sh
python3 scripts/check_freshness.py
```

To also check the official Bend release claim, supply GitHub's latest-release response:

```sh
curl -fsS --retry 2 --max-time 30 https://api.github.com/repos/bendlang/bend/releases/latest -o /tmp/bend-release.json && \
  python3 scripts/check_freshness.py --bend-release /tmp/bend-release.json
```

## Reading results

On a PR, open **Checks** and select the relevant job to see its result. For a maintenance audit, open [BendHub imports](https://github.com/777genius/awesome-bend/actions/workflows/bendhub.yml) or [Version freshness](https://github.com/777genius/awesome-bend/actions/workflows/freshness.yml), then select a run or choose **Run workflow** if you have write access. Contributors can use the existing reports and PR checks without running a workflow manually.

The summary states what was checked, what needs review, and whether any source could not be checked. A completed maintenance job can contain an incomplete audit; read that result before treating references as verified or current. After a temporary failure, a maintainer can use **Re-run failed jobs** on an unsuccessful PR check, or **Run workflow** for a completed but incomplete maintenance audit. If these controls are unavailable to you, ask a maintainer to retry; no README change is needed just to trigger a new run.

The import and freshness scripts use these exit codes, including when run by an agent:

| Exit | Result | What to do |
| --- | --- | --- |
| `0` | Requested check completed, possibly with optional updates. | Review update candidates when useful; retain intentional pins. |
| `1` | Invalid input or metadata, missing published content, or failed integrity. | Fix the reported problem before accepting the change. |
| `2` | Invalid command arguments. | Check the command's `--help`. |
| `3` | A required source is temporarily unavailable. | Retry later; the audit is incomplete. |

CI keeps real errors and unexpected failures unsuccessful. Only the documented temporary-unavailability result is advisory for freshness and for scheduled or manual catalog audits.

Thank you for your suggestions.
