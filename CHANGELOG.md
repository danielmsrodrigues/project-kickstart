# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [0.5.3] - 2026-11-20

### Fixed

- Scaffolding into a temporary directory no longer lands inside the repo. create-vite treats an absolute target such as `/var/folders/.../app` as relative, so `npx create-vite@latest "$(mktemp -d)/app"` created `./var/folders/.../app` in the current folder. The scaffold commands now `cd` into the temporary directory and pass a relative name (`app`); create-next-app follows the same pattern for consistency. Found while kickstarting a sample Vite app.

## [0.5.2] - 2026-11-20

### Fixed

- Contrast is computed, never estimated. `build_tokens.py contrast` checks every text/background pair, every filled button and status color against the ink declared on it (`textOn`), and borders and focus rings at 3:1, in light and dark. A fill with no declared ink fails, so no pair goes unchecked. `--pairs` checks a draft palette before any tokens file exists.
- `/kickstart` must run it before showing a visual direction and again after writing the tokens. `/kickstart-design` runs it on every new export and when adopting. Found by a test where a proposed "ready" green failed with both white and dark text, which the model had not checked.
- The example tokens failed their own check in dark mode (button text and active state); fixed.

## [0.5.1] - 2026-11-20

### Fixed

- Docs language is asked, not imposed: technical docs stay in English by default, but when the user writes in another language the skill asks once (English recommended), and an existing repo keeps its docs language. UI copy follows the product's audience. Code and file names stay in English.
- The visual direction is no longer settled in the Superpowers spec, where it skipped the design review: the spec records only the user's own words about the look. Every direction, including one already in a spec, is checked in the design-system step against generic defaults (such as cream with terracotta and a serif display) and revised before it's shown.

## [0.5.0] - 2026-11-20

### Changed

- `/tokens-sync` is renamed `/kickstart-design`, so it reads as part of the same plugin as `/kickstart`. Same modes (sync, adopt, create), same behaviour. `/tokens-sync` no longer exists.

## [0.4.0] - 2026-11-20

### Added

- `/tokens-sync`, a skill of its own for bringing a design into an existing project:
  - **Sync:** a new Claude Design, Figma or tokens export goes against `design/tokens.json`. It shows the token diff, the contrast of each change, where each changed or removed token is used, and the blockers (removed tokens still in use), then applies only what's approved.
  - **Adopt:** an informal design system (CSS variables, a Tailwind theme, a `Theme` type) becomes `design/tokens.json` without changing how anything looks. Framework defaults the code relies on get role tokens with identical values, and the compiled CSS is compared before and after.
  - **Create:** for a repo with no design system, only the design-system files.

### Changed

- `/kickstart` hands design exports for existing systems to `/tokens-sync`; the sync and import references moved into that skill.
- Tested on an existing repo with code, a hand-written README in another language, an informal Tailwind theme and git history. `/kickstart` documented the existing system instead of creating a second one, appended to the README and `.gitignore` without touching what was there, and recorded the problems it found as open questions without changing code.

## [0.3.0] - 2026-11-20

### Changed

- About 23% cheaper per kickstart, with the same output quality. On the same web-app test, 0.2.0 cost 3.89 USD with 71 model calls in generation; 0.3.0 cost 3.01 USD with 50, and re-read 58% less context. Build, tests, lint and every check passed in both.
- New `scripts/kickstart_files.py` does the mechanical work without the model: `.gitignore` and `.editorconfig` (base + stack, merged into a scaffold's), copying `build_tokens.py`, the settings JSON (refuses destructive commands), `AGENTS.md`, and the post-generation checks.
- `SKILL.md` is a third shorter, and adds a rule to work in few round trips: batch reads and writes, chain shell commands, never read a file only to copy it.
- Design-system references are split so each run loads only what it needs: `design-system.md` (core), `design-import.md` (Claude Design, Figma, other sources), `design-sync.md` (sync mode), and one platform file each for web, SwiftUI, Blazor, React Native and other stacks.

### Removed

- Per-stack `claude/settings.json` templates; the allow-list is now built from the commands actually written in `CLAUDE.md`.

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
