# Awesome Bend [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[<img src="media/logo.png" align="right" width="128" alt="Bend">](https://bend-lang.com)

> High-level language for massively parallel CPU and GPU programs, with an affine dependent type system.

This list is **current Bend**: `bendlang/bend`, 2.0.x. It is not Bend 1 (`HigherOrderCO/Bend1`, `cargo install bend-lang`, `bend run-cu`).

```sh
curl -fsSL https://bend-lang.com/install.sh | sh
```

The hub has no package names, versions, or search. You `import 0x…/file.bend` from a project's README, or clone the repo until it publishes a hash. To find a published library, use the community catalog below.

## Contents

- [Official](#official)
- [Catalog](#catalog)
- [Packages](#packages)
- [Tools](#tools)
- [Packaging](#packaging)
- [Learning](#learning)
- [Demos](#demos)
- [Papers](#papers)
- [Community](#community)
- [Related](#related)

## Official

- [Bend](https://github.com/bendlang/bend) - Compiler, `Base` library, guide, demos, and papers.
- [Lab](https://bend-lang.com/#lab) - In-browser playground.
- [Hub](https://hub.bend-lang.com) - Content-hash registry: publish, fetch, and a newest-first listing. No names or search. `?hub=` can point a local hub at the same page.
- [Bender](https://bend-lang.com/bender) - Official proving agent for `LAWS.bend` / `PROOF.bend`.
- [Base](https://github.com/bendlang/bend/blob/main/bend2/base.bend) - Bundled standard library, also printed by `bend base`.

## Catalog

- [Bend Packages](https://777genius.github.io/bend-packages/) - Community catalog with search, filters, and copy-import. Not the official hub.

## Packages

Clone until a project prints a hub `import 0x…` line.

- [gauss](https://github.com/pjdotson/gauss) - Unit-aware engineering calculation engine with SI dimensions.
- [unsga3-bend](https://github.com/AppSprout-dev/unsga3-bend) - U-NSGA-III optimiser, on the hub as `import 0x527a2a4fa91b05a0250d7be0e11d232a/lib.bend`.
- [bend-lemmas](https://github.com/caiodomingues/bend-lemmas) - Reusable Nat, List, and Bool lemmas for `PROOF.bend` files.
- [bend-tty](https://github.com/caiodomingues/bend-tty) - Raw-mode terminal effects, escapes, and a proof-checked key decoder.
- [scrapanium](https://github.com/0x5f3759df-fs/scrapanium) - HTTP/1.1, HTTP/2, and TLS WebSockets via a native transport.
- [openai-bend](https://github.com/gouveags/openai-bend) - Typed OpenAI Responses client, on the hub as `import 0x7d1714d98ca88352be07e0302e547a19/openai.bend`.
- [anthropic-bend](https://github.com/gouveags/anthropic-bend) - Typed Anthropic Messages client, on the hub as `import 0x44dbbb9fe7023c9f8cc89550f8343cd3/anthropic.bend`.
- [bend-codec](https://github.com/777genius/bend-codec) - RFC 4648 hex, Base64, and UTF-8, on the hub as `import 0x888714bde93f46c139372bb9fdc57a19/hex.bend`.
- [bend-parse](https://github.com/777genius/bend-parse) - Cursor, digits, and finish, on the hub as `import 0xe49a3e6521e1b71e55654a885f27bcc1/parse.bend`.
- [bend-time](https://github.com/777genius/bend-time) - Gregorian dates, Instant, Duration, Period, ISO week, `P`/`PT`, RFC 3339 subset, IANA zones, and RFC 9557. Core `import 0x9b6a4fc7ceea91864a75396e1b8365e5/date.bend`; zone `import 0x5118d7c8d8a6cbdfca48647d1a5a6fde/zone.bend`.
- [shake](https://github.com/Emerging-Patterns/shake) - CLI argument parser for flags, options, and nested commands, on the hub as `import 0xba6940aab8a335b70bf79944bd9b53c4/main.bend`.
- [bend-sha256](https://github.com/Giulio2002/bend-sha256) - SHA-256 with machine-checked proofs against FIPS 180-4, on the hub as `import 0xda83506fb9f059ead7afcfa2f498df5f/sha256.bend`.
- [bend-json](https://github.com/rootagi/bend-json) - JSON parser and serializer with formal proofs, on the hub as `import 0x1f4d6c03caf955232d0b0dc6e6f36cf4/json.bend`.
- [bend-net](https://github.com/naoeosavio/bend-net) - HTTP/1.1, HTTP/2, HTTPS, DNS, TLS, and WebSockets, on the hub as `import 0xd66ee682d4ce8c656782ca9e0e4634cb/http.bend`.
- [eztoml](https://github.com/Emerging-Patterns/eztoml) - TOML for Bend 2, on the hub as `import 0x04b9afdd6d6a56039c5ce6dfb1e55294/main.bend`.
- [ezjson](https://github.com/Emerging-Patterns/ezjson) - JSON for Bend 2, on the hub as `import 0xa3c2445eb44c5d8406e6229be518fccb/main.bend`.
- [mylsm](https://github.com/FabianVegaA/mylsm) - Durable LSM key-value store, on the hub as `import 0x05fa0e42448e8e221df592b204de523d/mylsm.bend`.
- [bend-tui](https://github.com/caiodomingues/bend-tui) - Terminal views, a proof-checked frame shape, and a `Tui.run` loop on bend-tty.
- [toon_bend](https://github.com/Dicklesworthstone/toon_bend) - JSON ↔ TOON codec and CLI, golden-tested against the original.
- [ezhttp](https://github.com/Emerging-Patterns/ezhttp) - HTTP client and server with RFC 9110/9112/3986 laws. Install with `ez add Emerging-Patterns/ezhttp`.
- [ezaudio](https://github.com/Emerging-Patterns/ezaudio) - PCM clips (`s16` / `f32`) for Bend 2. Install with `ez add Emerging-Patterns/ezaudio`.
- [ezimg](https://github.com/Emerging-Patterns/ezimg) - Raster images for Bend 2. Install with `ez add Emerging-Patterns/ezimg`.
- [bend-conv](https://github.com/Kaz9487/bend-conv) - FP32 convolution with proofs and a pretrained YOLOv5n example.

## Tools

- [bolt](https://github.com/Emerging-Patterns/bolt) - Linter, checker, and LSP written in Bend, with a VS Code extension, on the hub as `import 0x729eecea86ea5a2cdba3a2856a313bca/bolt/main.bend`.
- [tree-sitter-bend2](https://github.com/nicolas-abril/tree-sitter-bend2) - Tree-sitter grammar with highlight, symbol, and indent queries.
- [bend2-fuzzer](https://github.com/nicolas-abril/bend2-fuzzer) - Differential fuzzer for the JavaScript and C backends.
- [bend-fmt-lsp](https://github.com/bendlang/bend/tree/main/tools/bend-fmt-lsp) - Official formatting-only language server (full document, no diagnostics).
- [bURL](https://github.com/rosdyana/bURL) - HTTP/1.1 and HTTPS client with DNS in Bend and a proof-checked parser.
- [godot-bend](https://github.com/aricarmo/godot-bend) - Proof-of-concept GDExtension for writing Godot games in Bend.
- [bendirstat](https://github.com/kirillleventcov/bendirstat) - Disk-usage analyzer with a parallel scan and a zoomable treemap.
- [teamy-bend](https://github.com/TeamDman/teamy-bend) - Independent Rust implementation of a Bend 2 subset.
- [snap](https://github.com/Emerging-Patterns/snap) - Process runner (`run` / `start` / `par`), on the hub as `import 0x9bfd9d57916f3439316c2775fd1f10b4/main.bend`.
- [bend-init](https://github.com/gouveags/bend-init) - CLI that scaffolds a law-backed starter project, on the hub as `import 0x1e0cc3677d46304c29af14dfd5553385/main.bend`.
- [fire-bend](https://github.com/JonasLoos/fire-bend) - Experimental indentation-based syntax that compiles to Bend.
- [zed-bend](https://github.com/chhoumann/zed-bend) - Syntax highlighting for Zed.
- [bend-mode.el](https://github.com/davidawad/bend-mode.el) - Emacs major mode with Eglot formatting and Flymake diagnostics.
- [bend2-language-support](https://github.com/CaioWing/bend2-language-support) - VS Code diagnostics, completions, and snippets.
- [bend2-vscode](https://github.com/nuxyel/bend2-vscode) - VS Code client with a standalone language server.
- [davidawad/tree-sitter-bend2](https://github.com/davidawad/tree-sitter-bend2) - Vim/Neovim plugin with a Tree-sitter grammar.
- [bend-grammar](https://github.com/gouveags/bend-grammar) - TextMate grammar with tokenizer regression tests.
- [beads_bend](https://github.com/Dicklesworthstone/beads_bend) - Local-first issue tracker port, still early.
- [bendc](https://github.com/Lulzx/bendc) - Self-hosting Bend 2 compiler, written in Bend 2, targeting C.
- [bend2-lsp](https://github.com/don2e4/bend2-lsp) - Standalone language server: diagnostics, hover, go-to-definition, and formatting.
- [Giulio2002/bend-vscode](https://github.com/Giulio2002/bend-vscode) - VS Code highlighting, autocomplete, compiler diagnostics, and `.bend` file icons.

## Packaging

Do not use nixpkgs `bend`. That package is Bend 1.

- [nicolas-abril/bend2-nix](https://github.com/nicolas-abril/bend2-nix) - Nix flake that builds Bend from pinned upstream source.
- [y0usaf/bend2-nix](https://github.com/y0usaf/bend2-nix) - Nix flake on the official release tarball and bun.
- [ez](https://github.com/Emerging-Patterns/ez) - Project management for Bend.
- [kitevi/homebrew-bend](https://github.com/kitevi/homebrew-bend) - Unofficial Homebrew tap for Bend 2 on macOS (`brew install kitevi/bend/bend`).

## Learning

- [Guide](https://github.com/bendlang/bend/blob/main/guide/GUIDE.md) - Language guide, also printed by `bend guide`.
- [bend2-from-zero](https://github.com/nohzafk/bend2-from-zero) - From-scratch tutorial ([book](https://nohzafk.github.io/bend2-from-zero/)), including probes that are supposed to fail.
- [aprendendo-bend2](https://github.com/erickweil/aprendendo-bend2) - Short examples in Portuguese.

## Demos

### Official demos

- [Winning Is Impossible](https://github.com/bendlang/bend/tree/main/demos/app_win_is_bug_2d) - 2D game plus a proof the player cannot win.
- [Slash Boss](https://github.com/bendlang/bend/tree/main/demos/app_slash_boss_3d) - 3D boss-fight demo.
- [Rollback netcode](https://github.com/bendlang/bend/tree/main/demos/io_rollback_netcode) - Deterministic multiplayer networking example.

### Community demos

- [metal-bending](https://github.com/AdrielSantana/metal-bending) - Verified examples and CPU vs Metal measurements on Apple Silicon.
- [bend2-tar-demo](https://github.com/nicolas-abril/bend2-tar-demo) - Tape archive and gzip CLI with a byte-identical C twin.
- [bend2-svg-demo](https://github.com/nicolas-abril/bend2-svg-demo) - SVG viewer, renderer, and editor for native and web.
- [bend2-bendquest-demo](https://github.com/nicolas-abril/bend2-bendquest-demo) - Cooperative multiplayer RPG with a Bend server and client.
- [qmdb-bend2](https://github.com/patrick-ogrady/qmdb-bend2) - Membership-proof checker for the QMDB authenticated database.
- [portal-bend](https://github.com/danielhe4rt/portal-bend) - Raycaster with shootable portals, momentum, and a visible body crossing.
- [raytracing-bend2](https://github.com/aguspiza/raytracing-bend2) - Ray tracing in a weekend, ported from Nim, with parallel lets.
- [bend-night-train](https://github.com/kvcop/bend-night-train) - WebGL night-train scene rewritten as a Bend tile rasteriser.
- [bend2-quantum-simulator](https://github.com/splch/bend2-quantum-simulator) - Quantum circuit simulator with type-indexed amplitudes.
- [bendoom](https://github.com/eliesgalvira/bendoom) - Doom that reads a WAD at runtime, with laws and a Nix flake.
- [crud-api-bend](https://github.com/patote85/crud-api-bend) - In-process HTTP CRUD API with a file-backed store.
- [bend-playground](https://github.com/krymancer/bend-playground) - Ray tracing, Game of Life, pi collisions, and a Rubik cube graph.
- [bend-2-mandelbrot](https://github.com/tomc98/bend-2-mandelbrot) - Mandelbrot explorer on Apple Silicon with Metal and deep zoom.

## Papers

- [BendTT](https://github.com/bendlang/bend/blob/main/paper/BendTT.pdf) - Affine dependent type theory.
- [BendRT](https://github.com/bendlang/bend/blob/main/paper/BendRT.pdf) - Parallel runtime for CPUs and GPUs.
- [bend.lean](https://github.com/bendlang/bend/blob/main/bend2/bend.lean) - Core calculus in Lean.

## Community

- [Discord](https://discord.bend-lang.com) - Official chat.
- [X](https://x.com/bendlang) - Official account.
- [Reddit](https://www.reddit.com/r/bendlang/) - Official subreddit.
- [Issues](https://github.com/bendlang/bend/issues) - Bug reports and language discussion.

## Related

- [Bend 1](https://github.com/HigherOrderCO/Bend1) - Previous language (HVM2). Programs do not carry over.
- [awesome-bend (archived)](https://github.com/naoeosavio/awesome-bend) - Tools and editor plugins for Bend 1.

## Contributing

Contributions welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).
