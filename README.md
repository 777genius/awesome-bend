# Awesome Bend [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[<img src="media/logo.png" align="right" width="128" alt="Bend">](https://bend-lang.com)

> High-level language for massively parallel CPU and GPU programs, with an affine dependent type system.

This list is **current Bend**: `bendlang/bend`, 2.0.x. It is not Bend 1 (`HigherOrderCO/Bend1`, `cargo install bend-lang`, `bend run-cu`).

Last checked: **24 October 2026**. Latest stable release: [Bend 2.0.39](https://github.com/bendlang/bend/releases/tag/v2.0.39).

```sh
curl -fsSL https://bend-lang.com/install.sh | sh
```

Hub packages are pinned to content hashes (`import 0x…/file.bend`); names and versions are aliases (`import name@version/file.bend`). Names of 12–64 characters can be claimed; shorter names are auctioned. The hub has search, hot/new, and posts. Use a published import below, or clone projects without one.

Bend 2.0.32 changed `TCP.listen` and `UDP.bind` to take a bind address, and `IO.args()` now includes the program at index 0. Bend 2.0.33-2.0.34 speed up checking shared terms; the proven `--verdict` kernel does not yet share every comparison. Bend 2.0.35 restores GPU execution on M1/M2, fixes imported-name isolation and busy-loop timers, and rejects combining `--verdict` with `--publish`. Bend 2.0.36 adds timeout-aware channel and socket operations and byte-oriented UDP, improves checking and BendTT verdict handling, fixes native callbacks, and renames the proving agent to BendAI. Bend 2.0.37 changes the JS host boundary for `Nat` to plain numbers instead of bigint, adds `IO.exit`, and changes the parameter mode of `F32.show`; JS callers and higher-order uses may need migration. Bend 2.0.38 moves a compiled program's runtime options between `+RTS` and `-RTS`, so `./main --threads 4` now reaches the program as an argument; a `BENDRTS` environment variable and `--` work too. JS module names now keep constructors apart across files, `TCP.send` returns unsent bytes to resume with `TCP.send_bytes`, native windows emit typed `Text` events, `Char` holds any u32 on every lane, and `--verdict` explains unsafe or foreign dependencies. The release also speeds up GPU bang chaining, `String.order`, and emission, and fixes Metal stack spilling, several C and IO memory bugs, and formatter and LSP edge cases. Bend 2.0.39 hardens `bend --publish` against escaping the entry's directory, adds `File.open(path, "x")`, byte-oriented arguments via `IO.args_bytes` and `File.open_bytes`, and makes `Process.run` run through one worker on Bun and Node. It also fixes the 2.0.38 Metal lane spill regression, several C, GPU, IO and CLI safety bugs, and formatter improvements. Check a package's compiler requirements; a published hash does not guarantee compatibility with every release.

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
- [BendAI](https://bend-lang.com/bendai) - Official proving agent for `LAWS.bend` / `PROOF.bend`.
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
- [bend-time](https://github.com/777genius/bend-time) - Gregorian dates, Instant, Duration, Period, ISO week, `P`/`PT`, RFC 3339 subset, IANA zones, and RFC 9557. Release v0.6.0 adds calendar quarter bounds and day-of-year helpers in its source checkout; the Hub core remains `import bend-datetime@0.4.0.1/date.bend`, checked on Bend 2.0.28, 2.0.34, and 2.0.36; zone `import 0x5118d7c8d8a6cbdfca48647d1a5a6fde/zone.bend` still depends on the older core.
- [shake](https://github.com/Emerging-Patterns/shake) - CLI argument parser for flags, options, and nested commands, on the hub as `import shake@0.7.0.0/main.bend`.
- [bend-sha256](https://github.com/Giulio2002/bend-sha256) - SHA-256 with machine-checked proofs against FIPS 180-4, on the hub as `import 0xda83506fb9f059ead7afcfa2f498df5f/sha256.bend`.
- [bend-json](https://github.com/rootagi/bend-json) - JSON parser and serializer with formal proofs, on the hub as `import 0xf776c27e08f75fc19a070c691bcbb111/json.bend`.
- [bend-net](https://github.com/naoeosavio/bend-net) - HTTP/1.1, HTTP/2, HTTPS, DNS, TLS, and WebSockets, on the hub as `import 0xd66ee682d4ce8c656782ca9e0e4634cb/http.bend`.
- [eztoml](https://github.com/Emerging-Patterns/eztoml) - TOML parser and renderer for Bend 2, on the hub as `import emerging-eztoml@0.9.0.0/main.bend`.
- [ezjson](https://github.com/Emerging-Patterns/ezjson) - JSON for Bend 2, on the hub as `import emerging-ezjson@1.3.0.0/main.bend`.
- [mylsm](https://github.com/FabianVegaA/mylsm) - Experimental durable LSM key-value store; source 0.6.0.0 alpha adds cursors, snapshots, backups, and a coordinated local owner, with explicit migration from 0.5 storage. Current source requires Bend 2.0.37; the released Hub package remains `import mylsm-lsm-store@0.5.0.0/mylsm.bend`, requiring Bend 2.0.36+.
- [bend-tui](https://github.com/caiodomingues/bend-tui) - Terminal views, a proof-checked frame shape, and a `Tui.run` loop on bend-tty.
- [toon_bend](https://github.com/Dicklesworthstone/toon_bend) - JSON ↔ TOON codec and CLI, golden-tested against the original.
- [ezhttp](https://github.com/Emerging-Patterns/ezhttp) - HTTP/1.1 client and server with auth, cookie, and CORS helpers, on the hub as `import emerging-ezhttp@0.21.0.0/main.bend`.
- [ezaudio](https://github.com/Emerging-Patterns/ezaudio) - PCM clips, WAV codecs, and limited MPEG-1 Layer III support for Bend 2, on the hub as `import emerging-ezaudio@0.4.0.0/main.bend`.
- [ezimg](https://github.com/Emerging-Patterns/ezimg) - PNG and baseline JPEG codecs for Bend 2, on the hub as `import emerging-ezimg@1.2.0.0/main.bend`.
- [bend-collections](https://github.com/Giulio2002/bend-collections) - Verified containers, numeric utilities, and growing proved cryptography (SHA-3, BLAKE2/BLAKE3, Argon2id, ChaCha20-Poly1305, AES-GCM, X25519, Ed25519, secp256k1), on the hub as `import bend-collections@1.0.0.0/src/containers/hash_table.bend`.
- [bend-mathlib](https://github.com/bendlib/bendlib) - Machine-checked arithmetic, list, sorting, string, and algebra lemmas, on the hub as `import bend-mathlib@0.7.5.0/nat.bend`.
- [BendSR](https://github.com/k3ybladewielder/BendSR) - Parallel symbolic regression, on the hub as `import 0x07516e23611e5287ce89bcff661be83f/BendSR.bend`.
- [bend_tensors](https://hub.bend-lang.com/n/bend-tensors) - Dense linear algebra with shapes in the types, on the hub as `import bend-tensors@0.0.0.2/bend_tensors.bend`.
- [stiff](https://github.com/fraylabs/stiff) - Experimental native HTTP, routing, streaming, and SQLite-backed local state; version 0.6.1 targets Bend 2.0.36 (0.6.0 remains for Bend 2.0.35).
- [bendygrad](https://github.com/KapioKai/bendygrad) - Tinygrad front-end in Bend 2: views, buffers, autodiff, and SGD.
- [bend-machines](https://hub.bend-lang.com/0x9fc0cec754888f0fecabce899ddf2ee5/main.bend) - Root-of-Lisp, Core, STG, and STG→C in one hub package, `import 0x9fc0cec754888f0fecabce899ddf2ee5/main.bend`.
- [bend-kit](https://github.com/paymog/bend-kit) - Independently published Bend 2 packages for codecs, collections, networking, storage, cryptography, services, proto3 codecs with typed `protoc` generation, and binary64 soft-float. Bytes `import bend-kit-bytes@0.3.2.0/bytes.bend`; HTTP `import bend-kit-http@0.37.0.0/http.bend`. The project currently requires Bend 2.0.38 or newer.
- [V](https://hub.bend-lang.com/n/near-v-framework) - Data structures and architecture as types. Arc `import near-architecture@0.9.1.0/arc.bend`; V `import near-v-framework@0.7.0.0/v.bend`. The source repository is no longer accessible, so this entry links its hub package.
- [jonlib](https://github.com/jonathanperis/jonlib) - Graphics, image-codec, and math library working toward raylib 6.0 parity; requires its pinned Bend 2.0.27 Metal overlay.
- [bend-lawful-stdlib](https://hub.bend-lang.com/n/bend-lawful-stdlib) - Typeclass-style Ord, Semigroup, and Group with their laws, `import bend-lawful-stdlib@0.1.0.0/src/class.bend`.
- [ber](https://github.com/FabianVegaA/ber) - Version-controlled data on MyLSM with certified merges, on the hub as `import ber-core-store@0.1.2.0/ber.bend`.
- [bend-parallel](https://github.com/costamatheus97/bend-parallel) - Parallel prefix sums, histograms, and a stable counting sort, on the hub as `import bend-parallel@0.1.0.0/scan.bend`.
- [bend-schema](https://github.com/nohzafk/bend-schema) - JSON schema checker whose core is proved in Bend, used from TypeScript or Bend, with an optional Effect v4 codec adapter and tested JSON Schema 2020-12 export; exported schemas omit refinement predicates and runtime budgets.
- [wordlib](https://github.com/Yazington/wordlib) - Machine-word laws on the hub as `import 0xb13667d52aa56e002b4d09883d7fce3e/PROOF.bend`; checkout also includes list laws and a sum prover.
- [bend-over](https://github.com/subtleGradient/bend-over) - SQLite and JavaScript interop with native, Bun, and browser examples. SQLite `import bend-over-sqlite@0.1.0.1/sqlite.bend`.
- [bend-trace-context](https://github.com/LucasGois1/bend-trace-context) - W3C Trace Context propagation for Bend, Node, and browsers, with proved protocol rules and context generation. Hub `import bend-trace-context@0.2.0.0/trace_context.bend`; requires exactly Bend 2.0.34.
- [bend-csv](https://github.com/nohzafk/bend-csv) - CSV parser with quoted and multiline fields, custom separators, a TypeScript bridge, and machine-checked core laws. Hub `import bend-csv-parser@0.1.0.1/core.bend`; requires Bend 2.0.35.
- [raptorq-bend](https://github.com/hotschmoe/raptorq-bend) - RFC 6330 RaptorQ encoder and decoder with parallel multi-block object support and Rust reference vectors.
- [bend-merkle-tree](https://github.com/adust09/bend-merkle-tree) - Hash-generic, capacity-bounded Merkle trees with SHA-256 and independent golden vectors; requires Bend 2.0.34.
- [bend-ml](https://github.com/nuxyel/bend-ml) - Shape-typed tensors over lists or arrays, automatic differentiation, and byte-level BPE, with CPU MNIST and GPT-2 demos; requires Bend 2.0.37. Tensor `import bend-ml-tensor-array@0.1.14.0/main.bend`; its hub packages now include a GPU tensor package (`import bend-ml-tensor-gpu@0.1.2.1/main.bend`) and a Llama-model package (`import bend-ml-llama@0.2.0.0/main.bend`).
- [bend-smtp](https://github.com/kbrianps/bend-smtp) - SMTP client with TLS, OAuth, DKIM, SMTPUTF8, and attachments; its pure core has a machine-checked proof that cleaned addresses and headers carry no CR or LF; native build only (C effects over OpenSSL), tested with Bend 2.0.36, on the hub as `import 0x650cd729029c76d9f6151ee977dc0ae8/smtp.bend`.
- [bender-http](https://github.com/RevCBH/bender-http) - HTTP/1.1 and HTTPS client and CLI with a proved pure codec; uses the sibling bender-dns checkout and is tested on Linux with Bend 2.0.32 and OpenSSL 3.
- [bender-dns](https://github.com/RevCBH/bender-dns) - TCP DNS stub resolver, OS resolver delegation, and a CLI, with proved codec laws; tested on Linux with Bend 2.0.32.
- [bend-zcash-blake2b](https://github.com/Giulio2002/bend-zcash-blake2b) - Proved parameterized BLAKE2b with a C library and Rust blake2b_simd adapter; incremental buffering and host glue are tested, not proved.
- [gax-bend](https://github.com/jobstijl/gax-bend) - Geometric algebra with generated kernels proved against a multivector specification, geometric APIs, and a ray-tracing demo; uses Bend 2.0.35, with GPU experiments on the upstream HIP branch.
- [bend-stream](https://github.com/kbrianps/bend-stream) - RTSP and RTMP clients as sessions that give frames (H.264, H.265, AAC, and G.711 over both), with MPEG-TS and FLV recording, TLS, and reconnection; its laws check RFC vectors and prove that no RTSP request field carries CR or LF; play only, native build only (C effects over OpenSSL), requires Bend 2.0.36+, on the hub as `import 0x2355f41b6f5561f50104a75ccca27cf7/rtsp.bend`.
- [Chromi](https://github.com/amage-si/chromi) - Experimental AMAGE 2D renderer with a CPU reference, retained frames, and a Vulkan GPU path through Voltra; tested on Bend 2.0.35 with Linux X11/XWayland.

- [chelokot/bend-math](https://github.com/chelokot/bend-math) - Experimental exact mathematics with checked rational ordered-field, polynomial-identity, and inequality-certificate laws; its general Cauchy-real model remains incomplete.

- [BendKV](https://github.com/littleBro/BendKV) - Experimental Redis-compatible RESP2/RESP3 key-value server with proved command, storage, and session laws; implements a Redis subset and requires a dedicated patched Bend 2.0.35. No license has been granted yet.

- [Bendvy](https://github.com/dearlordylord/bendvy) - Experimental Bend 2 entity-component system with typed queries, deferred commands, and native/browser examples, including a browser swarm demo whose build is checked on Bend 2.0.36; its API and Bevy parity remain in progress. No license file is provided.

- [Stelliferous](https://github.com/Kaz9487/Stelliferous) - F32 tensor library with source-level convolution proofs against a fixed FP32 specification, on the hub as `import stelliferous@0.0.3.0/tensor_f32.bend`; checked on official Bend 2.0.36. Its training package (convolution, batch norm, activation, and pool layers) is in the same package as `import stelliferous@0.0.3.0/tensor_training.bend`.
- [bend-edit-distance](https://github.com/jware-solutions/bend-edit-distance) - Experimental Edlib-style edit distance and alignment library and CLI, on the hub as `import bend-edit-distance@0.2.2.0/lib.bend`; requires Bend 2.0.37+ and implements only part of Edlib.

- [bend-sat](https://github.com/sebastian-griego/bend-sat) - Experimental SAT solver with watched literals, first-UIP learning, and a proved result checker with DPLL fallback; validated on a pinned Bend 2.0.37 macOS arm64 setup. No license file is provided.
- [bendtorch](https://github.com/aaaxn/bendtorch) - Experimental CPU F32 tensor library with shape-indexed storage, tensor operations, and scalar autograd; numerical results are tested against PyTorch, and model training is not implemented. Requires its pinned Bend compiler checkout.
- [bend-osdev](https://github.com/ScottMoore0/bend-osdev) - MIT-licensed operating-system libraries: file systems, archives, compression, ELF, partition tables, network headers, capability and LSM policy models, and kernel data structures, each with laws, `--verdict`-accepted proofs, and differential tests; pinned to Bend 2.0.37 and published incrementally on the hub as `bend-osdev-<package>` (for example `import bend-osdev-bytes@0.1.0.0/bytes.bend`).
- [bend2-libs](https://github.com/nicolas-abril/bend2-libs) - Text, XML, CSS, PNG, JPEG, TrueType, SVG-render, byte, and archive libraries unpacked from nicolas-abril's demos onto the hub under the `gralha-` prefix (for example `import gralha-text-scan@0.1.0.0/scan.bend` and `import gralha-ustar@0.1.0.0/ustar.bend`); requires Bend 2.0.37+.
- [bentdelta](https://github.com/michaelsproul/bentdelta) - VCDIFF (RFC 3284) delta encoder and decoder compatible with xdelta3, with a machine-checked round-trip law covering targets under 2 GiB less 1 MiB; no license file is provided.
- [MailBend](https://github.com/albertc71/MailBend) - IMAP/SMTP connector for AI agents with a CLI and MCP server; its mail-safety rules are proved laws, a Rust helper handles TLS, and it pins Bend 2.0.35.
- [bend-keccak](https://github.com/Giulio2002/bend-keccak) - Ethereum Keccak-256 with packed arrays and a kernel-checked sponge refinement proof, on the hub as `import 0x48cee57f42dae6ba4c727fbf982cdd4d/keccak.bend`.
- [bend-visgraph](https://github.com/aaaxn/bend-visgraph) - Visibility graphs of time series ported from ts2vg, natural and horizontal with directed and weighted edges, on the hub as `import 0xe3a7f78ee5245da17fe27e3556f94e74/bend_visgraph.bend`; requires Bend 2.0.37.
- [mlbend-hf](https://github.com/adeerkhan/mlbend-huggingface) - Hugging Face dataset client with dataset metadata, file trees, file bytes, and rows-server reads over JSON HTTP, on the hub as `import mlbend-huggingface@0.1.1.0/main.bend`.
- [mlbend-datasets](https://github.com/adeerkhan/mlbend-datasets) - scikit-learn's benchmark datasets fetched from Hugging Face at run time, with pure estimators over the returned values, on the hub as `import mlbend-datasets@0.1.4.0/main.bend`.
- [mlbend-metrics](https://github.com/adeerkhan/mlbend-metrics) - Regression and classification metrics (MSE, MAE, RMSE, accuracy, precision, recall, F1) with an `ALL PROOFS CHECK` gate and no `@unsafe`, on the hub as `import mlbend-metrics@0.1.0.0/main.bend`.
- [bend-env](https://github.com/adeerkhan/bend-env) - Project and environment manager: a manifest, lockfile, and pinned package environment resolved and verified against BendHub; no package-hub release of its own.
- [Bendo](https://github.com/opencoredev/bendo) - Pre-alpha Hono-style web framework with routing, parsing, JSON, and validation proved in `LAWS.bend`, plus a typed TypeScript client; not published on the hub.
- [BendTorch](https://github.com/nuxyel/BendTorch) - Typed layers with forward and backward passes, losses, optimizers and checkpoints over bend-ml's tensors, trained step for step against PyTorch twins on MNIST, a two-layer Llama and SmolLM2 (135M to 1.7B), with structural laws checked by `--verdict` and parallel CPU and GPU builds of the same layers, on the hub as `import bendtorch@1.1.1.0/main.bend`; requires Bend 2.0.39.

## Tools

- [bolt](https://github.com/Emerging-Patterns/bolt) - Linter, checker, and LSP written in Bend, with a VS Code extension, on the hub as `import bolt@1.18.0.0/main.bend`.
- [tree-sitter-bend2](https://github.com/nicolas-abril/tree-sitter-bend2) - Tree-sitter grammar with highlight, symbol, and indent queries.
- [bend2-fuzzer](https://github.com/nicolas-abril/bend2-fuzzer) - Differential fuzzer for the JavaScript and C backends.
- [bend-fmt-lsp](https://github.com/bendlang/bend/tree/main/tools/bend-fmt-lsp) - Official formatting-only language server (full document, no diagnostics).
- [bURL](https://github.com/rosdyana/bURL) - HTTP/1.1 and HTTPS client with DNS in Bend and a proof-checked parser.
- [godot-bend](https://github.com/aricarmo/godot-bend) - Proof-of-concept GDExtension for writing Godot games in Bend.
- [bendirstat](https://github.com/kirillleventcov/bendirstat) - Disk-usage analyzer with a parallel scan and a zoomable treemap.
- [teamy-bend](https://github.com/TeamDman/teamy-bend) - Independent Rust implementation of a Bend 2 subset.
- [snap](https://github.com/Emerging-Patterns/snap) - Process runner (`run` / `start` / `par`), on the hub as `import snap@1.3.0.0/main.bend`.
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
- [jev-fabric](https://github.com/fabric-runtime/jev-fabric) - Native process orchestration with bounded logs and typed Jev calls; version 0.8.0 adds experimental TypeSafe image references, Box questions, and opt-in long context, alongside decision APIs preserving provider JSON, refusals, and provenance. Requires Bend 2.0.37 when building from source.
- [bend-ldd](https://github.com/nohzafk/bend-ldd) - Agent skill for law-driven Bend 2: state laws, falsify them, prove them, then mutate the core.
- [bend-falsify](https://github.com/nohzafk/bend-falsify) - Falsifies Bend 2 laws on literal instances and checks each proof against a mutant, with optional bounded parallel mutation checks.
- [bend-emit](https://github.com/nohzafk/bend-emit) - Compiles a pure Bend core to a typed ES module, including tagged-tree `Map` boundary declarations; source version 0.3.9 also emits runtime definitions from laws/facts files after stripping recognized proofs and proof-only dependencies; recognized Bool-selector calls become lazy branches. Requires exactly Bend 2.0.37.
- [BendVerify](https://github.com/kingcharlezz/bendverify) - Proof-carrying compiler optimisation: a Lean-checked equivalence proof before any benchmark.
- [kbrianps/bend-vscode](https://github.com/kbrianps/bend-vscode) - VS Code highlighting, live diagnostics, hover, and formatting, with bend2-lsp bundled.
- [bendcheck](https://github.com/Yazington/bendcheck) - Property-based testing with generators, shrinking, and a `lawcheck` script for `LAWS.bend`. Library `import 0x738b30530890e825e0ab81092b94cbfc/check.bend`.
- [PedroVIOliv/bend-crater](https://github.com/PedroVIOliv/bend-crater) - Hub package type-checking matrix across Bend releases; records errors, timeouts, and missing dependencies.
- [costamatheus97/bend-crater](https://github.com/costamatheus97/bend-crater) - Nightly Hub compatibility matrix for recent releases and upstream main, with checker timings and CPU/JS lane comparisons.
- [bend2-nvim](https://github.com/nuxyel/bend2-nvim) - Neovim completion, navigation, diagnostics, formatting, and a compiler-backed Proof Explorer.
- [IlyaGulya/bend2-zed](https://github.com/IlyaGulya/bend2-zed) - Zed development extension with Bend 2 highlighting and the Rust bend2-lsp-rs language server, pinned to v0.6.1 with import completion and indexed symbol auto-import.
- [ericfode/zed-bend2](https://github.com/ericfode/zed-bend2) - Zed development extension with Tree-sitter highlighting and a bundled compiler-backed language server.
- [ProofPack State](https://github.com/bkase/proofpack-state) - Read-only Git object reachability, missing-object, and retention queries with a proved set-algebra core.
- [Bend verdict investigation](https://github.com/leo-guinan/bend-verdict-investigation) - Reproducible probes for Bend 2.0.32's checker and BendTT kernel, including a reported mismatch that the kernel rejects.
- [bend2-lsp-rs](https://github.com/IlyaGulya/bend2-lsp-rs) - Rust language server with compiler diagnostics, source navigation, rename, formatting, and semantic tokens; version 0.6.1 discovers workspace files in the background for navigation and auto-import. Native multi-error diagnostics are verified only on Apple Silicon with Bend 2.0.32-2.0.36; other compiler/platform combinations use CLI text diagnostics. Requires a local Bend 2 CLI.
- [Bend for Hermes](https://github.com/kvnloo/bend-native) - Hermes plugin for Bend proof verification with hashed receipts and offline replay; requires Bend 2.0.32+ and Lean 4.34.0.
- [lawcheck](https://github.com/bendlib/bendlib/tree/main/tools/lawcheck) - Finds and shrinks counterexamples to Bend laws, with mutation testing and optional checker/native comparison; tested on Bend 2.0.36.
- [eco-build](https://github.com/amage-si/eco-build) - Experimental cached, parallel native C build helper for the AMAGE ecosystem; supports official Bend 2.0.37.

- [bend-lint](https://github.com/MattCozendey/bend-lint) - Checker-backed linter and formatter with Bend rule programs and performance diagnostics; uses Bun and an automatically downloaded tested compiler. Windows uses a Bend fork; most fixes need `--fix-dangerously`.

- [bend-tools](https://github.com/viridale/bend-tools) - Shell and Python helpers for emitted-C reference counts, per-law checks, proof diagnostics, and native benchmarks; pinned to Bend 2.0.36.
- [baton](https://github.com/Flip-Engineering/baton) - Deterministic coordinator that drives vendor CLI coding agents (Claude Code, Codex, Grok, GLM) as trust-gated session workers, written in Bend 2.
- [bend-python](https://github.com/lucaswiman/bend-python) - Builds CPython extension modules from Bend 2 code with laws proved during the build; published on PyPI and pins Bend 2.0.28.
- [cha](https://github.com/mintktkr/cha) - Forge CLI for Gitea, Forgejo, and GitHub with issue, pull-request, and run commands, written in Bend 2 with proved laws; requires Bend 2.0.34.
- [bird](https://github.com/bangedorrunt/bird) - Command-line client for reading and posting to X, rewritten in Bend 2 with a pure law-proved core and shell/network effects at the edge.
- [reflex](https://github.com/monotykamary/reflex) - Mac menu-bar and phone companion for monitoring and routing terminal coding-agent sessions, with a Bend 2 routing core and proved safety laws; requires Apple Silicon and Bend 2.0.37.
- [bend-cad](https://github.com/Phylliida/bend-cad) - Experimental CAD sketch-solver design with Bend source for geometry and constraint solving, machine-checked with a `PROOF.bend` gate against a local Bend checkout.
- [helix-bend](https://github.com/davidawad/helix-bend) - Helix language entry, highlight queries, and install script for the pinned Bend 2 grammar; Helix has no plugin system, so it is configuration rather than a plugin.
- [bend.vim](https://github.com/davidawad/bend.vim) - Vim and Neovim plugin with a classic syntax layer and optional Tree-sitter highlighting built from the pinned `tree-sitter-bend2` grammar.
- [bend-cli](https://github.com/viridale/bend-cli) - Command-line interface library: one declaration yields help, typed argument decoding, shell completions, and man pages, with the behavior stated as Bend laws; on the hub as `import cli@0.1.0.0/cli.bend`, requires Bend 2.0.38+.
- [bend-ipp](https://github.com/davidawad/bend-ipp) - Pure IPP (RFC 8010/8011) codec over byte lists, tested against Bend 2.0.38; not published on the hub.
- [bend-iac](https://github.com/erayack/bend-iac) - Proof-oriented infrastructure-as-code planner for Cloudflare that returns an authorized, ordered plan or a blocked explanation, with three safety laws checked by `PROOF.bend`; uses a pinned Bend checkout.

## Packaging

Do not use nixpkgs `bend`. That package is Bend 1.

- [nicolas-abril/bend2-nix](https://github.com/nicolas-abril/bend2-nix) - Nix flake that builds Bend from pinned upstream source.
- [y0usaf/bend2-nix](https://github.com/y0usaf/bend2-nix) - Nix flake on the official release tarball and bun.
- [ez](https://github.com/Emerging-Patterns/ez) - Project management for Bend, on the hub as `import ezx@1.9.0.0/main.bend`.
- [bend.nix](https://github.com/lukasl-dev/bend.nix) - Unofficial Nix flake tracking Bend 2 `main`, with NixOS and Home Manager modules, an overlay, and optional CUDA support.
- [Official Nix flake](https://github.com/bendlang/bend/blob/main/flake.nix) - Installs verified Bend release archives on Linux and macOS (`nix profile install github:bendlang/bend`).

## Learning

- [Guide](https://github.com/bendlang/bend/blob/main/guide/GUIDE.md) - Language guide, also printed by `bend guide`.
- [bend2-from-zero](https://github.com/nohzafk/bend2-from-zero) - From-scratch tutorial ([book](https://nohzafk.github.io/bend2-from-zero/)), including probes that are supposed to fail.
- [aprendendo-bend2](https://github.com/erickweil/aprendendo-bend2) - Short examples in Portuguese.
- [Bend, Explained](https://raunak-11.github.io/bend-explainer/) - Interactive beginner explainer of parallelism, laws, and proofs ([repo](https://github.com/raunak-11/bend-explainer)).
- [bend2.dev](https://bend2.dev/) - Independent notes, syntax primer, and example programs.
- [bend-math](https://github.com/lilalittle/bend-math) - Small executable example of symbolic differentiation and forward-mode automatic differentiation, with a machine-checked agreement proof.

- [Bend 2 pocket workshop](https://np.github.io/bend-workshop/) - Independent browser workshop with the checker, compiler, proof-hole goals, and proof tools in one page, including a phone interface ([repo](https://github.com/np/bend-workshop)); uses a pinned compiler checkout.

- [bend-tutorial](https://github.com/Ivo-Balbaert/Bend-Tutorial) - Bend hands-on tutorial for beginners coming from Python.
- [bend2-intro-with-life](https://github.com/Nasu726/bend2-intro-with-life) - Japanese beginner's book that teaches Bend 2 by building a Game of Life, with downloadable PDF and sample code.
- [bend2-spike](https://github.com/YSRKEN/bend2-spike) - Japanese Bend 2 verification notes: a small proved HTTP server, language probes, benchmark data, and slides covering Bend 2.0.34-2.0.36.
- [bend-pitfalls](https://github.com/rofrol/bend-pitfalls) - Single-file list of Bend 2 language and compiler pitfalls found in real projects, each entry tagged with the compiler version it was seen with.

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
- [bendoom](https://github.com/eliesgalvira/bendoom) - Doom that reads a WAD at runtime, with laws and a Nix flake.
- [crud-api-bend](https://github.com/patote85/crud-api-bend) - In-process HTTP CRUD API with a file-backed store.
- [bend-playground](https://github.com/krymancer/bend-playground) - Ray tracing, Game of Life, pi collisions, and a Rubik cube graph.
- [bend-2-mandelbrot](https://github.com/tomc98/bend-2-mandelbrot) - Mandelbrot explorer on Apple Silicon with Metal and deep zoom.
- [bend-voxel](https://github.com/aivv73/bend-voxel) - Editable voxel sculpture scene with a native Bend renderer, CPU/GPU execution, and material-aware carving; requires Bend 2.0.34+, with X11 headers on Linux.
- [bend2craft](https://github.com/lennix1337/bend2craft) - Minecraft-inspired voxel sandbox with shared Bend rules, a WebGL browser client, and a native CPU-rendered client.
- [birc](https://github.com/angerman/birc) - Formally verified terminal IRC client with a native DNS engine.
- [Eldergrove Faire](https://github.com/RedLynx101/eldergrove-faire) - RollerCoaster Tycoon-style park sim with sixteen machine-checked laws.
- [bend-voxel-bench](https://github.com/OkeyAmy/bend-voxel-bench) - Luanti terrain ported to Bend, with a CPU voxel world and a live race against C++.
- [BendJVM](https://github.com/MatheusBBarni/bendJVM) - Java 8 class-file interpreter in Bend, with bounded reflection, annotations, and interface proxies, differentially tested against `java`.
- [bend-craft](https://github.com/costamatheus97/bend-craft) - Fixed-point voxel game with generated terrain and first-person interaction. GPU measurements use an experimental CUDA-over-HIP compiler fork.
- [Peggie Bend Lab](https://github.com/absolukie/peggie-bend-lab) - Procedural peg-board generator with a proof that every requested cell produces exactly one target peg.
- [Rift Chess Bend 2 preview](https://github.com/HaileyStorm/rift-chess-bend2) - Browser preview of a Bend-rendered chess experiment; source and proofs remain in the main Rift Chess repository.
- [Bendcraft](https://github.com/AdrielSantana/bendcraft) - Walkable voxel world with weather, flowing water, and proofs; currently needs its dedicated Bend compiler branch for the documented performance and features.
- [Three Bodies](https://github.com/AdrielSantana/three-bodies) - Interactive gravitational simulation with software binary64 physics, GPU rendering, and a checker-verified theorem for a fixed figure-8 integration run; requires Bend 2.0.34+.
- [kbrianps/bendoom](https://github.com/kbrianps/bendoom) - Doom and Doom II with menus, saves, OPL and General MIDI music, and PWADs, whose demos play tic for tic as in Chocolate Doom; native build, or in the browser at [kbrianps.com/bendoom](https://kbrianps.com/bendoom/); tested with Bend 2.0.36.
- [bocht](https://github.com/ckluis/bocht) - Native HTTP backend with auth, WAL storage, REST, and MCP; current source targets Bend 2.0.35.
- [shellOS](https://github.com/ckluis/shellOS) - Desktop shell with rendering and UI state in Bend and native effects; documented macOS arm64 build uses Bend 2.0.35.

- [llama.bend](https://github.com/nuxyel/llama.bend) - CPU SmolLM2 inference with shape-typed weights and cache laws, tested against Transformers; requires Bend 2.0.37.
- [rubend](https://github.com/yuzyayvri/rubend) - 3×3 Rubik's cube solver written in Bend 2 with proved cube rules and pruning-table generators, plus a Three.js workbench; requires Nix and Bend 2.0.37.
- [bendSVM](https://github.com/CrocSwap/bendSVM) - Bounded Bend 2 to Solana SBF compiler and SDK exercised by token, vesting, exchange, and AMM applications with proved laws; requires a pinned Bend checkout and platform-tools.

## Benchmarks

- [Official benchmarks](https://github.com/bendlang/bend/tree/main/bench) - Compiler, proof-checker, CPU, and GPU workloads used for Bend's published charts, including a parallel histogram benchmark with C, TypeScript, and Lean comparisons.
- [bend-bench](https://github.com/wakamex/bend-bench) - Independent CPU/OpenMP and GPU/CUDA comparisons, with reproducible output checks and separate startup and workload measurements. Non-ML results measure Bend 2.0.3, with a separate 2.0.26 comparison; newer ML comparisons against PyTorch use pinned upstream main.
- [eco-bench](https://github.com/amage-si/eco-bench) - Reproducible AMAGE Eco and GPUI comparisons with raw logs and methodology; measured on Bend 2.0.35 with X11/XWayland, without native Wayland results.

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
