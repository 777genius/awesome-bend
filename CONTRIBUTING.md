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
- Run `npx awesome-lint` and keep it green.

Thank you for your suggestions.
