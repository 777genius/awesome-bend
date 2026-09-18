# Awesome Bend 2

A curated list of **[Bend 2](https://bend-lang.com)** — the language, libraries, tools, and demos.

This is **not** Bend 1 / HVM2 (`HigherOrderCO/Bend`). Older lists and editor plugins from 2024 target that language. The compiler here is `bendlang/bend` (`bend 2.0.x`). Packages on the hub are content hashes (`import 0x…/file.bend`), not names, so GitHub is the catalog.

## Contents

- [Official](#official)
- [Libraries](#libraries)
- [Editors and language tools](#editors-and-language-tools)
- [Packaging](#packaging)
- [Learning](#learning)
- [Demos](#demos)
- [Papers](#papers)
- [Community](#community)
- [Contributing](#contributing)

## Official

- [bendlang/bend](https://github.com/bendlang/bend) — compiler, `Base`, GUIDE, demos, papers.
- [bend-lang.com](https://bend-lang.com) — site, install, in-browser lab.
- [Install](https://bend-lang.com) — `curl -fsSL https://bend-lang.com/install.sh | sh`
- [Hub](https://hub.bend-lang.com) — publish/fetch by content hash. There is no package search; the import line is the handle.
- [bend2-landing](https://github.com/VictorTaelin/bend2-landing) — source for the landing page.
- [HigherOrderCO/Bend2](https://github.com/HigherOrderCO/Bend2) — redirect to `bendlang/bend`.

In the language repo:

- [GUIDE.md](https://github.com/bendlang/bend/blob/main/guide/GUIDE.md) — also `bend guide`
- [base.bend](https://github.com/bendlang/bend/blob/main/bend2/base.bend) — also `bend base`
- [demos/](https://github.com/bendlang/bend/tree/main/demos) — apps with `LAWS.bend` / `PROOF.bend`

## Libraries

Install via Git clone until a project prints a hub `0x…` import line.

- [bend-batteries](https://github.com/condensate-dev/bend-batteries) — pieces `Base` does not ship: **json** (shipped), http / tls / fetch / regex / test / fmt (planned). Laws and proofs in-tree.

Codec (RFC 4648 hex, then Base64), parse, and time libraries from the maintainers of this list will be linked here when they have a public repository.

## Editors and language tools

- [bolt](https://github.com/Emerging-Patterns/bolt) — linter, `bend`-shaped checker, and LSP written in Bend 2, with a VS Code extension.
- [tree-sitter-bend2](https://github.com/nicolas-abril/tree-sitter-bend2) — Tree-sitter grammar, highlight / symbol / indent queries.
- [bend2-fuzzer](https://github.com/nicolas-abril/bend2-fuzzer) — differential fuzzer for JS vs C backends.

Bend 1 VS Code / LSP crates (`bend-language-server` 0.2.x) do not apply.

## Packaging

`nixpkgs` attribute `bend` is **Bend 1**. Use a Bend 2 flake:

- [nicolas-abril/bend2-nix](https://github.com/nicolas-abril/bend2-nix) — flake, pinned upstream source.
- [y0usaf/bend2-nix](https://github.com/y0usaf/bend2-nix) — flake on the official release tarball + bun.

## Learning

- Official GUIDE — `bend guide` / [GUIDE.md](https://github.com/bendlang/bend/blob/main/guide/GUIDE.md)
- [bend2-from-zero](https://github.com/nohzafk/bend2-from-zero) — from-scratch tutorial ([book](https://nohzafk.github.io/bend2-from-zero/)), including probes that are supposed to fail.
- [aprendendo-bend2](https://github.com/erickweil/aprendendo-bend2) — short examples (Portuguese).

## Demos

Official (in `bendlang/bend`):

- [Winning Is Impossible](https://github.com/bendlang/bend/tree/main/demos/app_win_is_bug_2d) — game plus a proof you cannot win ([play](https://bend-lang.com/#lab)).
- [Slash Boss](https://github.com/bendlang/bend/tree/main/demos/app_slash_boss_3d)
- [Rollback netcode](https://github.com/bendlang/bend/tree/main/demos/io_rollback_netcode)

Community:

- [metal-bending](https://github.com/AdrielSantana/metal-bending) — verified examples and CPU vs Metal measurements on Apple Silicon.
- [bend2-tar-demo](https://github.com/nicolas-abril/bend2-tar-demo) — tar / gzip CLI.
- [bend2-svg-demo](https://github.com/nicolas-abril/bend2-svg-demo) — SVG viewer / editor, native and web.
- [bend2-bendquest-demo](https://github.com/nicolas-abril/bend2-bendquest-demo) — cooperative multiplayer RPG (Bend server + client).
- [qmdb-bend2](https://github.com/patrick-ogrady/qmdb-bend2) — QMDB membership-proof check in Bend 2.

## Papers

- [BendTT](https://github.com/bendlang/bend/blob/main/paper/BendTT.pdf) — affine dependent type theory.
- [BendRT](https://github.com/bendlang/bend/blob/main/paper/BendRT.pdf) — parallel runtime for CPUs and GPUs.
- [bend.lean](https://github.com/bendlang/bend/blob/main/bend2/bend.lean) — core in Lean.

## Community

- [Discord](https://discord.bend-lang.com)
- [X / Twitter](https://x.com/bendlang)
- [Reddit](https://www.reddit.com/r/bendlang/)
- [Issues](https://github.com/bendlang/bend/issues)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Bend 2 only.

## License

[CC0](https://creativecommons.org/publicdomain/zero/1.0/).
