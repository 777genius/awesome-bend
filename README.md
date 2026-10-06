# Awesome Bend [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[<img src="media/logo.png" align="right" width="128" alt="Bend">](https://bend-lang.com)

> High-level language for massively parallel CPU and GPU programs, with an affine dependent type system.

This list is **current Bend**: `bendlang/bend`, 2.0.x. It is not Bend 1 (`HigherOrderCO/Bend1`, `cargo install bend-lang`, `bend run-cu`).

Last checked: **6 October 2026**. Latest stable release: [Bend 2.0.35](https://github.com/bendlang/bend/releases/tag/v2.0.35).

```sh
curl -fsSL https://bend-lang.com/install.sh | sh
```

Hub packages are pinned to content hashes (`import 0x…/file.bend`); names and versions are aliases (`import name@version/file.bend`). Names of 12–64 characters can be claimed; shorter names are auctioned. The hub has search, hot/new, and posts. Use a published import below, or clone projects without one.

Bend 2.0.32 changed `TCP.listen` and `UDP.bind` to take a bind address, and `IO.args()` now includes the program at index 0. Bend 2.0.33-2.0.34 speed up checking shared terms; the proven `--verdict` kernel does not yet share every comparison. Bend 2.0.35 restores GPU execution on M1/M2, fixes imported-name isolation and busy-loop timers, and rejects combining `--verdict` with `--publish`. Check a package's compiler requirements; a published hash does not guarantee compatibility with every release.

## Contents

- [Official](#official)
- [Catalog](#catalog)
- [Packages](#packages)
- [Tools](#tools)
- [Packaging](#packaging)
- [Learning](#learning)
- [Demos](#demos)
- [Benchmarks](#benchmarks)
- [Papers](#papers)
- [Community](#community)
- [Related](#related)

## Official

- [Bend](https://github.com/bendlang/bend) - Compiler, `Base` library, guide, demos, and papers.
- [Lab](https://bend-lang.com/#lab) - In-browser playground.
- [Hub](https://hub.bend-lang.com) - Content-hash registry with optional names (`import name@version/file.bend`), search, hot/new, and posts. `?hub=` can point a local hub at the same page.
- [Bender](https://bend-lang.com/bender) - Official proving agent for `LAWS.bend` / `PROOF.bend`.
- [Base](https://github.com/bendlang/bend/blob/main/bend2/base.bend) - Bundled standard library, also printed by `bend base`.

## Catalog

- [Bend Packages](https://777genius.github.io/bend-packages/) - Community catalog with search, filters, and copy-import. Not the official hub.
- [bend-catalog](https://kbrianps.github.io/bend-catalog/) - Live hub index: every hash, laws, size, and import line ([repo](https://github.com/kbrianps/bend-catalog)).
- [Bend Docs](https://bendlib.github.io/bendlib/) - Generated API docs, checker status, and law search for BendHub packages ([repo](https://github.com/bendlib/bendlib)).

## Packages

Imports below identify published packages, not a claim that every package passes on the latest compiler. The Tools section includes compatibility matrices.

- [gauss](https://github.com/pjdotson/gauss) - Experimental unit-aware engineering calculation engine with SI dimensions.
- [unsga3-bend](https://github.com/AppSprout-dev/unsga3-bend) - U-NSGA-III optimiser with constrained problems, on the hub as `import unified-nsga-iii@0.2.2.0/lib.bend`.
- [bend-lemmas](https://github.com/caiodomingues/bend-lemmas) - Reusable Nat, List, and Bool lemmas for `PROOF.bend` files.
- [bend-tty](https://github.com/caiodomingues/bend-tty) - Raw-mode terminal effects, escapes, and a proof-checked key decoder.
- [scrapanium](https://github.com/0x5f3759df-fs/scrapanium) - HTTP/1.1, HTTP/2, and TLS WebSockets via a native transport.
- [openai-bend](https://github.com/gouveags/openai-bend) - Typed OpenAI Responses client through a localhost TypeScript SDK companion, on the hub as `import bend-openai-sdk@0.1.0.1/openai.bend`; requires Bend 2.0.34+.
- [anthropic-bend](https://github.com/gouveags/anthropic-bend) - Typed Anthropic Messages client through a localhost TypeScript SDK companion, on the hub as `import bend-anthropic-sdk@0.1.0.1/anthropic.bend`; requires Bend 2.0.34+.
- [bend-codec](https://github.com/777genius/bend-codec) - RFC 4648 hex, Base64, and UTF-8, on the hub as `import bend-encoding@0.2.0.0/hex.bend`.
- [bend-parse](https://github.com/777genius/bend-parse) - Cursor, digits, and finish, on the hub as `import bend-scanner@0.1.0.0/parse.bend`.
- [bend-time](https://github.com/777genius/bend-time) - Gregorian dates, Instant, Duration, Period, ISO week, `P`/`PT`, RFC 3339 subset, IANA zones, and RFC 9557. Core `import bend-datetime@0.4.0.1/date.bend` fixes compatibility with Bend 2.0.28+; zone `import 0x5118d7c8d8a6cbdfca48647d1a5a6fde/zone.bend` still depends on the older core.
- [shake](https://github.com/Emerging-Patterns/shake) - CLI argument parser for flags, options, and nested commands, on the hub as `import shake@0.5.0.0/main.bend`.
- [bend-sha256](https://github.com/Giulio2002/bend-sha256) - SHA-256 with machine-checked proofs against FIPS 180-4, on the hub as `import 0xda83506fb9f059ead7afcfa2f498df5f/sha256.bend`.
- [bend-json](https://github.com/rootagi/bend-json) - JSON parser and serializer with formal proofs, on the hub as `import 0xf776c27e08f75fc19a070c691bcbb111/json.bend`.
- [bend-net](https://github.com/naoeosavio/bend-net) - HTTP/1.1, HTTP/2, HTTPS, DNS, TLS, and WebSockets, on the hub as `import 0xd66ee682d4ce8c656782ca9e0e4634cb/http.bend`.
- [eztoml](https://github.com/Emerging-Patterns/eztoml) - TOML parser and renderer for Bend 2, on the hub as `import emerging-eztoml@0.8.0.0/main.bend`.
- [ezjson](https://github.com/Emerging-Patterns/ezjson) - JSON for Bend 2, on the hub as `import emerging-ezjson@1.1.0.0/main.bend`.
- [mylsm](https://github.com/FabianVegaA/mylsm) - Experimental durable LSM key-value store, on the hub as `import mylsm-lsm-store@0.4.0.0/mylsm.bend`; requires Bend 2.0.35+ and uses a disk format incompatible with earlier releases.
- [bend-tui](https://github.com/caiodomingues/bend-tui) - Terminal views, a proof-checked frame shape, and a `Tui.run` loop on bend-tty.
- [toon_bend](https://github.com/Dicklesworthstone/toon_bend) - JSON ↔ TOON codec and CLI, golden-tested against the original.
- [ezhttp](https://github.com/Emerging-Patterns/ezhttp) - HTTP/1.1 client and server with auth, cookie, and CORS helpers, on the hub as `import emerging-ezhttp@0.8.0.0/main.bend`.
- [ezaudio](https://github.com/Emerging-Patterns/ezaudio) - PCM clips, WAV codecs, and limited MPEG-1 Layer III support for Bend 2, on the hub as `import emerging-ezaudio@0.4.0.0/main.bend`.
- [ezimg](https://github.com/Emerging-Patterns/ezimg) - PNG and baseline JPEG codecs for Bend 2, on the hub as `import emerging-ezimg@1.2.0.0/main.bend`.
- [bend-collections](https://github.com/Giulio2002/bend-collections) - Verified containers, numeric utilities, and cryptography, on the hub as `import bend-collections@1.0.0.0/src/containers/hash_table.bend`.
- [bend-mathlib](https://github.com/bendlib/bendlib) - Machine-checked arithmetic, list, sorting, string, and algebra lemmas, on the hub as `import bend-mathlib@0.7.2.0/nat.bend`.
- [BendSR](https://github.com/k3ybladewielder/BendSR) - Parallel symbolic regression, on the hub as `import 0x07516e23611e5287ce89bcff661be83f/BendSR.bend`.
- [bend_tensors](https://hub.bend-lang.com/n/bend-tensors) - Dense linear algebra with shapes in the types, on the hub as `import bend-tensors@0.0.0.2/bend_tensors.bend`.
- [stiff](https://github.com/fraylabs/stiff) - Experimental native HTTP, routing, streaming, and SQLite-backed local state; version 0.4.0 targets Bend 2.0.35.
- [bendygrad](https://github.com/KapioKai/bendygrad) - Tinygrad front-end in Bend 2: views, buffers, autodiff, and SGD.
- [bend-machines](https://hub.bend-lang.com/0x9fc0cec754888f0fecabce899ddf2ee5/main.bend) - Root-of-Lisp, Core, STG, and STG→C in one hub package, `import 0x9fc0cec754888f0fecabce899ddf2ee5/main.bend`.
- [bend-kit](https://github.com/paymog/bend-kit) - Independently published Bend 2 packages for codecs, collections, networking, storage, cryptography, and services. Bytes `import bend-kit-bytes@0.3.2.0/bytes.bend`; HTTP `import bend-kit-http@0.30.0.0/http.bend`. The project currently requires Bend 2.0.32 or newer.
- [V](https://github.com/PedroAVJ/n) - Data structures and architecture as types. Arc `import near-architecture@0.9.1.0/arc.bend`; V `import near-v-framework@0.7.0.0/v.bend`.
- [jonlib](https://github.com/jonathanperis/jonlib) - Graphics and game-programming library working toward raylib 6.0 parity; requires its pinned Bend 2.0.27 Metal overlay.
- [bend-lawful-stdlib](https://hub.bend-lang.com/n/bend-lawful-stdlib) - Typeclass-style Ord, Semigroup, and Group with their laws, `import bend-lawful-stdlib@0.1.0.0/src/class.bend`.
- [ber](https://github.com/FabianVegaA/ber) - Version-controlled data on MyLSM with certified merges, on the hub as `import ber-core-store@0.1.2.0/ber.bend`.
- [bend-parallel](https://github.com/costamatheus97/bend-parallel) - Parallel prefix sums, histograms, and a stable counting sort, on the hub as `import bend-parallel@0.1.0.0/scan.bend`.
- [bend-schema](https://github.com/nohzafk/bend-schema) - JSON schema checker whose core is proved in Bend, used from TypeScript or Bend, with an optional Effect v4 codec adapter.
- [wordlib](https://github.com/Yazington/wordlib) - Machine-word laws on the hub as `import 0xb13667d52aa56e002b4d09883d7fce3e/PROOF.bend`; checkout also includes list laws and a sum prover.
- [bend-over](https://github.com/subtleGradient/bend-over) - SQLite and JavaScript interop with native, Bun, and browser examples. SQLite `import bend-over-sqlite@0.1.0.1/sqlite.bend`.
- [bend-trace-context](https://github.com/LucasGois1/bend-trace-context) - W3C Trace Context propagation for Bend, Node, and browsers, with proved protocol rules and context generation. Hub `import bend-trace-context@0.2.0.0/trace_context.bend`; requires exactly Bend 2.0.34.
- [bend-csv](https://github.com/nohzafk/bend-csv) - CSV parser with quoted and multiline fields, custom separators, a TypeScript bridge, and machine-checked core laws. Hub `import bend-csv-parser@0.1.0.1/core.bend`; requires Bend 2.0.35.
- [raptorq-bend](https://github.com/hotschmoe/raptorq-bend) - RFC 6330 RaptorQ encoder and decoder with parallel multi-block object support and Rust reference vectors.
- [bend-merkle-tree](https://github.com/adust09/bend-merkle-tree) - Hash-generic, capacity-bounded Merkle trees with SHA-256 and independent golden vectors; requires Bend 2.0.34.
- [bend-ml](https://github.com/nuxyel/bend-ml) - Shape-typed tensors over lists or arrays, automatic differentiation, and byte-level BPE, with CPU MNIST and GPT-2 demos; requires Bend 2.0.35. Tensor `import bend-ml-tensor-array@0.1.5.0/main.bend`.
- [bend-smtp](https://github.com/kbrianps/bend-smtp) - SMTP client with TLS, OAuth, DKIM, SMTPUTF8, and attachments; its pure core has a machine-checked proof that cleaned addresses and headers carry no CR or LF; native build only (C effects over OpenSSL), on the hub as `import 0x00e7af2de246c3a4c341d9ee49e68747/smtp.bend`.
- [bender-http](https://github.com/RevCBH/bender-http) - HTTP/1.1 and HTTPS client with a proved pure codec; tested on Linux with Bend 2.0.32 and OpenSSL 3.
- [bender-dns](https://github.com/RevCBH/bender-dns) - TCP DNS stub resolver, OS resolver delegation, and a CLI, with proved codec laws; tested on Linux with Bend 2.0.32.
- [bend-zcash-blake2b](https://github.com/Giulio2002/bend-zcash-blake2b) - Proved parameterized BLAKE2b with a C library and Rust blake2b_simd adapter; incremental buffering and host glue are tested, not proved.
- [gax-bend](https://github.com/jobstijl/gax-bend) - Geometric algebra with generated kernels proved against a multivector specification, geometric APIs, and a ray-tracing demo; uses Bend 2.0.35, with GPU experiments on the upstream HIP branch.
- [bend-stream](https://github.com/kbrianps/bend-stream) - RTSP and RTMP clients as sessions that give frames (H.264, H.265, AAC, and G.711 over both), with MPEG-TS and FLV recording, TLS, and reconnection; its laws check RFC vectors and prove that no RTSP request field carries CR or LF; play only, native build only (C effects over OpenSSL), tested with Bend 2.0.35, on the hub as `import 0xd6fc55bf65b187fec4175f80d08c165a/rtsp.bend`.

## Tools

- [bolt](https://github.com/Emerging-Patterns/bolt) - Linter, checker, and LSP written in Bend, with a VS Code extension, on the hub as `import bolt@1.12.0.0/main.bend`.
- [tree-sitter-bend2](https://github.com/nicolas-abril/tree-sitter-bend2) - Tree-sitter grammar with highlight, symbol, and indent queries.
- [bend2-fuzzer](https://github.com/nicolas-abril/bend2-fuzzer) - Differential fuzzer for the JavaScript and C backends.
- [bend-fmt-lsp](https://github.com/bendlang/bend/tree/main/tools/bend-fmt-lsp) - Official formatting-only language server (full document, no diagnostics).
- [bURL](https://github.com/rosdyana/bURL) - HTTP/1.1 and HTTPS client with DNS in Bend and a proof-checked parser.
- [godot-bend](https://github.com/aricarmo/godot-bend) - Proof-of-concept GDExtension for writing Godot games in Bend.
- [bendirstat](https://github.com/kirillleventcov/bendirstat) - Disk-usage analyzer with a parallel scan and a zoomable treemap.
- [teamy-bend](https://github.com/TeamDman/teamy-bend) - Independent Rust implementation of a Bend 2 subset.
- [snap](https://github.com/Emerging-Patterns/snap) - Process runner (`run` / `start` / `par`), on the hub as `import snap@1.2.0.0/main.bend`.
- [bend-init](https://github.com/gouveags/bend-init) - CLI that scaffolds a law-backed starter project, on the hub as `import 0x1e0cc3677d46304c29af14dfd5553385/main.bend`.
- [fire-bend](https://github.com/JonasLoos/fire-bend) - Experimental indentation-based syntax that compiles to Bend.
- [zed-bend](https://github.com/chhoumann/zed-bend) - Syntax highlighting for Zed.
- [bend-mode.el](https://github.com/davidawad/bend-mode.el) - Emacs major mode with Eglot formatting and Flymake diagnostics.
- [bend2-language-support](https://github.com/CaioWing/bend2-language-support) - VS Code diagnostics, completions, and snippets.
- [bend2-vscode](https://github.com/nuxyel/bend2-vscode) - VS Code client with a standalone language server.
- [davidawad/tree-sitter-bend2](https://github.com/davidawad/tree-sitter-bend2) - Vim/Neovim plugin with a Tree-sitter grammar.
- [bend-grammar](https://github.com/gouveags/bend-grammar) - TextMate grammar with tokenizer regression tests.
- [beads_bend](https://github.com/Dicklesworthstone/beads_bend) - Local-first issue tracker port, golden-tested against the original, still early.
- [bendc](https://github.com/Lulzx/bendc) - Self-hosting Bend 2 compiler targeting C, with a type checker, parallel CPU runtime, and Metal GPU backend.
- [bend2-lsp](https://github.com/don2e4/bend2-lsp) - Standalone language server: diagnostics, hover, go-to-definition, and formatting.
- [Giulio2002/bend-vscode](https://github.com/Giulio2002/bend-vscode) - VS Code highlighting, autocomplete, compiler diagnostics, and `.bend` file icons.
- [bend-idea](https://github.com/dearlordylord/bend-idea) - IntelliJ IDEA plugin with completion, navigation, refactoring, formatting, proof workflows, and optional compiler diagnostics.
- [bendler](https://github.com/lukaszsamson/bendler) - Call Bend from Elixir through a supervised port or an experimental NIF.
- [bend-frontend](https://github.com/ind-igo/bend-frontend) - Checks full Bend and exports a typed `Core.Program` for backends.
- [bend-evm](https://github.com/ind-igo/bend-evm) - EVM backend: contracts in Bend, certified IR, and Yul lowering.
- [FabianVegaA/tree-sitter-bend](https://github.com/FabianVegaA/tree-sitter-bend) - Tree-sitter grammar for Bend 2 syntax.
- [web3signer_bend](https://github.com/eserilev/web3signer_bend) - Web3Signer-compatible Ethereum consensus remote signer, with slashing-protection laws.
- [knot](https://github.com/MatheusBBarni/knot-node-tooling) - JavaScript package manager, TypeScript transformer, and bundler written in Bend 2. Published as `@matheusbbarni/knot`; test runner still planned.
- [jev-fabric](https://github.com/fabric-runtime/jev-fabric) - Native process orchestration with bounded logs and optional typed Jev calls.
- [bend-ldd](https://github.com/nohzafk/bend-ldd) - Agent skill for law-driven Bend 2: state laws, falsify them, prove them, then mutate the core.
- [bend-falsify](https://github.com/nohzafk/bend-falsify) - Falsifies Bend 2 laws on literal instances and checks each proof against a mutant.
- [bend-emit](https://github.com/nohzafk/bend-emit) - Compiles a pure Bend core to a typed ES module; requires exactly Bend 2.0.35.
- [BendVerify](https://github.com/kingcharlezz/bendverify) - Proof-carrying compiler optimisation: a Lean-checked equivalence proof before any benchmark.
- [kbrianps/bend-vscode](https://github.com/kbrianps/bend-vscode) - VS Code highlighting, live diagnostics, hover, and formatting, with bend2-lsp bundled.
- [bendcheck](https://github.com/Yazington/bendcheck) - Property-based testing with generators, shrinking, and a `lawcheck` script for `LAWS.bend`. Library `import 0x738b30530890e825e0ab81092b94cbfc/check.bend`.
- [PedroVIOliv/bend-crater](https://github.com/PedroVIOliv/bend-crater) - Hub package type-checking matrix across Bend releases; records errors, timeouts, and missing dependencies.
- [costamatheus97/bend-crater](https://github.com/costamatheus97/bend-crater) - Nightly Hub compatibility matrix for recent releases and upstream main, with checker timings and CPU/JS lane comparisons.
- [bend2-nvim](https://github.com/nuxyel/bend2-nvim) - Neovim completion, navigation, diagnostics, formatting, and a compiler-backed Proof Explorer.
- [IlyaGulya/bend2-zed](https://github.com/IlyaGulya/bend2-zed) - Zed development extension with Bend 2 highlighting and the Rust bend2-lsp-rs language server.
- [ericfode/zed-bend2](https://github.com/ericfode/zed-bend2) - Zed development extension with Tree-sitter highlighting and a bundled compiler-backed language server.
- [ProofPack State](https://github.com/bkase/proofpack-state) - Read-only Git object reachability, missing-object, and retention queries with a proved set-algebra core.
- [Bend verdict investigation](https://github.com/leo-guinan/bend-verdict-investigation) - Reproducible probes for Bend 2.0.32's checker and BendTT kernel, including a reported mismatch that the kernel rejects.
- [bend2-lsp-rs](https://github.com/IlyaGulya/bend2-lsp-rs) - Rust language server with completion, compiler diagnostics, source navigation, rename, formatting, and semantic tokens; requires a local Bend 2 CLI.
- [Bend for Hermes](https://github.com/kvnloo/bend-native) - Hermes plugin for Bend proof verification with hashed receipts and offline replay; requires Bend 2.0.32+ and Lean 4.34.0.
- [lawcheck](https://github.com/bendlib/bendlib/tree/main/tools/lawcheck) - Finds and shrinks counterexamples to Bend laws, with mutation testing and optional checker/native comparison; tested on Bend 2.0.35.

## Packaging

Do not use nixpkgs `bend`. That package is Bend 1.

- [nicolas-abril/bend2-nix](https://github.com/nicolas-abril/bend2-nix) - Nix flake that builds Bend from pinned upstream source.
- [y0usaf/bend2-nix](https://github.com/y0usaf/bend2-nix) - Nix flake on the official release tarball and bun.
- [ez](https://github.com/Emerging-Patterns/ez) - Project management for Bend, on the hub as `import ezx@1.5.0.0/main.bend`.
- [bend.nix](https://github.com/lukasl-dev/bend.nix) - Unofficial Nix flake tracking Bend 2 `main`, with NixOS and Home Manager modules, an overlay, and optional CUDA support.
- [Official Nix flake](https://github.com/bendlang/bend/blob/main/flake.nix) - Installs verified Bend release archives on Linux and macOS (`nix profile install github:bendlang/bend`).

## Learning

- [Guide](https://github.com/bendlang/bend/blob/main/guide/GUIDE.md) - Language guide, also printed by `bend guide`.
- [bend2-from-zero](https://github.com/nohzafk/bend2-from-zero) - From-scratch tutorial ([book](https://nohzafk.github.io/bend2-from-zero/)), including probes that are supposed to fail.
- [aprendendo-bend2](https://github.com/erickweil/aprendendo-bend2) - Short examples in Portuguese.
- [Bend, Explained](https://raunak-11.github.io/bend-explainer/) - Interactive beginner explainer of parallelism, laws, and proofs ([repo](https://github.com/raunak-11/bend-explainer)).
- [bend2.dev](https://bend2.dev/) - Independent notes, syntax primer, and example programs.
- [bend-math](https://github.com/lilalittle/bend-math) - Small executable example of symbolic differentiation and forward-mode automatic differentiation, with a machine-checked agreement proof.

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
- [bend-voxel](https://github.com/aivv73/bend-voxel) - Editable voxel sculpture scene with a native Bend renderer, CPU/GPU execution, and material-aware carving; requires Bend 2.0.34+, with X11 headers on Linux.
- [bend2craft](https://github.com/lennix1337/bend2craft) - Minecraft-inspired voxel sandbox with shared Bend rules, a WebGL browser client, and a native CPU-rendered client.
- [birc](https://github.com/angerman/birc) - Formally verified terminal IRC client with a native DNS engine.
- [Eldergrove Faire](https://github.com/RedLynx101/eldergrove-faire) - RollerCoaster Tycoon-style park sim with sixteen machine-checked laws.
- [bend-voxel-bench](https://github.com/OkeyAmy/bend-voxel-bench) - Luanti terrain ported to Bend, with a CPU voxel world and a live race against C++.
- [BendJVM](https://github.com/MatheusBBarni/bendJVM) - Java 8 class-file interpreter in Bend, differentially tested against `java`.
- [bend-craft](https://github.com/costamatheus97/bend-craft) - Fixed-point voxel game with generated terrain and first-person interaction. GPU measurements use an experimental CUDA-over-HIP compiler fork.
- [Peggie Bend Lab](https://github.com/absolukie/peggie-bend-lab) - Procedural peg-board generator with a proof that every requested cell produces exactly one target peg.
- [Rift Chess Bend 2 preview](https://github.com/HaileyStorm/rift-chess-bend2) - Browser preview of a Bend-rendered chess experiment; source and proofs remain in the main Rift Chess repository.
- [Bendcraft](https://github.com/AdrielSantana/bendcraft) - Walkable voxel world with weather, flowing water, and proofs; currently needs its dedicated Bend compiler branch for the documented performance and features.
- [Three Bodies](https://github.com/AdrielSantana/three-bodies) - Interactive gravitational simulation with software binary64 physics, GPU rendering, and a checker-verified theorem for a fixed figure-8 integration run; requires Bend 2.0.34+.
- [bocht](https://github.com/ckluis/bocht) - Native HTTP backend with auth, WAL storage, REST, and MCP; current source targets Bend 2.0.35.
- [shellOS](https://github.com/ckluis/shellOS) - Desktop shell with rendering and UI state in Bend and native effects; documented macOS arm64 build uses Bend 2.0.35.

## Benchmarks

- [Official benchmarks](https://github.com/bendlang/bend/tree/main/bench) - Compiler, proof-checker, CPU, and GPU workloads used for Bend's published charts, including a parallel histogram benchmark with C, TypeScript, and Lean comparisons.
- [bend-bench](https://github.com/wakamex/bend-bench) - Independent CPU/OpenMP and GPU/CUDA comparisons, with reproducible output checks and separate startup and workload measurements. Published results measure Bend 2.0.3, with a separate 2.0.26 comparison.

## Papers

- [BendTT](https://github.com/bendlang/bend/blob/main/paper/BendTT.pdf) - Affine dependent type theory.
- [BendRT](https://github.com/bendlang/bend/blob/main/paper/BendRT.pdf) - Parallel runtime for CPUs and GPUs.
- [bendtt.lean](https://github.com/bendlang/bend/blob/main/bend2/bendtt.lean) - BendTT kernel and its proofs in Lean, used to recheck proofs with `bend PROOF.bend --verdict`.

## Community

- [Discord](https://discord.bend-lang.com) - Official chat.
- [X](https://x.com/bendlang) - Official account.
- [Reddit](https://www.reddit.com/r/bendlang/) - Official subreddit.
- [Issues](https://github.com/bendlang/bend/issues) - Bug reports and language discussion.
- [Built with Bend](https://builtwithbend.com) - Human-reviewed directory of Bend 2 apps and demos ([repo](https://github.com/LVTD-LLC/built-with-bend)).

## Related

- [Bend 1](https://github.com/HigherOrderCO/Bend1) - Previous language (HVM2). Programs do not carry over.
- [awesome-bend (archived)](https://github.com/naoeosavio/awesome-bend) - Tools and editor plugins for Bend 1.

## Contributing

Contributions welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).
