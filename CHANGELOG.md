# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [0.2.0] - 2026-11-20

### Added

- Scaffolding for empty repos: once the stack is settled, the skill offers the stack's official scaffolder (create-vite, create-next-app, `uv init`, `dotnet new`, `swift package init`, `cargo init`, `go mod init`) and the dependency install as `run` lines in the confirmed list. The generated `CLAUDE.md` then lists commands that were actually run, and the design system is wired in at once: CSS entry, Tailwind plugin, `tokens` script, lint rule.
- Questions with nameable choices (stack, template, design origin, file-list confirmation, git) are asked as buttons through the structured question tool (`AskUserQuestion` in Claude Code), with the recommendation first. Open questions about purpose stay as text.
- Checks after generating run the build, test and lint commands when dependencies are installed.

### Changed

- Scaffolders run with flags that keep them from running `git init` (`--vcs none`, `--disable-git`). When the folder isn't empty, they run in a temporary directory and the result is moved in without replacing existing files.
- The marketplace entry no longer repeats the version; `plugin.json` is the single source.
- `.claude/settings.json` is a protected file: if writing it is blocked, the skill shows its content and asks for approval.

## [0.1.0] - 2026-11-20

### Added

- `/kickstart` skill: design, stack detection, confirmed file list, generation without overwriting, optional `git init` and initial commit.
- Generated files: `CLAUDE.md` (≤80 lines), `AGENTS.md` (symlink or copy), `docs/ARCHITECTURE.md`, `docs/CONVENTIONS.md`, a first ADR, `.gitignore`, `.editorconfig`, `README.md`, and `.claude/settings.json` with a non-destructive allow-list.
- Stack templates: Node + TypeScript, Python, .NET, Swift, Go and Rust, with a generic base for any other stack.
- Design-system step for UI projects. It imports from Claude Design, Figma variables, token files or a reference, or starts from scratch. It produces `design/tokens.json`, generated tokens for the web (CSS, Tailwind v4/v3), SwiftUI, Blazor and React Native, six base components, `docs/DESIGN.md`, a component inventory and a lint warning for hardcoded values.
- Sync mode for new design exports: token diff and affected components before anything is applied.
- `build_tokens.py` (Python 3.8+ standard library): `build`, `diff` and `check`.
- Optional integration with Superpowers (`brainstorming`, `writing-plans`) and frontend-design.
- Plugin manifest and a single-plugin marketplace in the same repo.
