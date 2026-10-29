# Contribution Guidelines

Please ensure your pull request adheres to the following:

- **Current Bend only** (`bendlang/bend`, 2.0.x). Do not add Bend 1 / HVM2 (`HigherOrderCO/Bend`, `cargo install bend-lang`, `bend run-cu`), Bend 1 editor plugins, or unrelated “Bend” projects (Oregon, BendDAO, hardware Bender, …).
- Search previous suggestions before opening a new one. This is a curation, not a dump of every `bend2-*` repository.
- Use the format `- [Name](url) - Description.`
- The description starts with an uppercase character and ends with a period.
- Keep descriptions short and objective: what the project is, not a tagline.
- Add new items at the bottom of the relevant category.
- Check your spelling and grammar. Do not hard-wrap lines.
- One item per pull request, with a useful title (`Add bolt`, not `Update README.md`).
- A working example or README beats a star count. Empty, generated, or undocumented trees will be closed.
- If a library publishes to the hub, add its documented `import name@version/file.bend` or `import 0x…/file.bend` line next to the GitHub link. Verify that the version resolves and the file exists in its published manifest.
- State meaningful limitations, such as a development-only editor extension or a planned feature. A published package is not evidence that it works on every compiler release.
- When refreshing an existing entry, check its README and the live hub; remove inaccessible projects instead of preserving broken links.
- New categories, or improvements to the existing ones, are welcome.
- Run the checks below and keep them green.

## Version policy

Keep concrete imports pinned to an exact published version or content hash. A newer package is a candidate for review, not an automatic replacement: check its entrypoint, compiler requirements, and upstream documentation before updating the example. Compare versions within the same Hub package name; a repository release tag can differ from its published Hub version. Do not infer package renames or a newer release from a content hash.

Avoid repeating a release number in prose when the import already conveys it. Keep versions that explain a source-versus-Hub difference, minimum or exact compiler requirement, compiler patch, or tested configuration. Do not replace these with the latest compiler number. Update `Last checked` only after reviewing the list's descriptions and sources; a metadata-only freshness run is not a full audit.

## Validation

```sh
npx --yes awesome-lint@2.3.0
python3 -m unittest discover -s tests -v
python3 scripts/check_bendhub.py
```

The BendHub check uses Python 3.10+ and its standard library. It resolves every concrete `import` reference in README, verifies the package manifest, and checks the referenced file's SHA-256. It reads published files without executing them; a passing check confirms publication and integrity, not compiler compatibility or proof correctness. The generic `name@version/file.bend` and `0x…/file.bend` examples are excluded.

CI runs this check on relevant pull requests, after changes reach `main`, and weekly. Network errors are retried briefly; an unavailable package remains a failed check with its README line, so retry after a temporary Hub outage rather than hiding the reference.

## Version freshness

The separate **Version freshness** workflow checks named Hub imports and the README's explicit `Latest stable release` claim for Bend. It runs weekly, manually, and after relevant changes reach `main`; pull requests run its offline regression tests without extra live freshness requests. It reads metadata without installing, compiling, or running packages, and writes its findings to the Actions job summary.

Newer published versions produce notices and a successful audit, so an intentionally older working pin does not fail CI. Missing metadata, network failures, or invalid response data fail the audit as incomplete. Hash-only imports have no version ordering and are counted as outside this check. Compatibility prose and repository release versions are not compared automatically.

Run the Hub-only audit locally; without `--bend-release`, the compiler release check is explicitly skipped:

```sh
python3 scripts/check_freshness.py
```

To also check the official Bend release claim, supply GitHub's latest-release response:

```sh
curl -fsS --retry 2 --max-time 30 https://api.github.com/repos/bendlang/bend/releases/latest -o /tmp/bend-release.json && \
  python3 scripts/check_freshness.py --bend-release /tmp/bend-release.json
```

Thank you for your suggestions.
