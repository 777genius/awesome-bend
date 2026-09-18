# Contributing

This list is **Bend 2 only**: `bendlang/bend`, `bend 2.0.x`, hub imports of the form `0x<hash>/file.bend`.

Do **not** add:

- Bend 1 / HVM2 (`HigherOrderCO/Bend`, `cargo install bend-lang`, `bend run-cu`)
- Editor plugins and LSPs for Bend 1
- Repos named “Bend” that are unrelated (Oregon, BendDAO, hardware Bender, …)
- Empty READMEs, generated dumps with no runnable `.bend` entry, or copies of `Base`

A good entry has a one-line job (“RFC 4648 hex”, “Tree-sitter for Bend 2”) and a URL someone can open today. Prefer a working example over a star count.

Open a PR that adds one bullet in the right section. If you maintain a library that just grew a hub hash, add the `import 0x…` line next to the GitHub link.

## This list’s own libraries

When codec (hex / Base64), parse, and time have public GitHub repos, they belong under [Libraries](README.md#libraries). Until then, do not link unpublished trees.
