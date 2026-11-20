# project-kickstart

A Claude Code plugin that sets up a new or empty repo with what AI coding agents and humans need on day one:

- **Agent guides:** a short `CLAUDE.md` (at most ~80 lines) and `AGENTS.md` (a symlink, or a copy on Windows)
- **Docs:** `docs/ARCHITECTURE.md`, `docs/CONVENTIONS.md`, and a first ADR in `docs/decisions/`
- **Configs:** `.gitignore`, `.editorconfig`, `README.md`, and `.claude/settings.json` with a safe allow-list for the stack's build, test and lint commands
- **A design system in code, for projects with a UI:** `design/tokens.json` as the single source, generated native tokens, six base components, `docs/DESIGN.md`, a component inventory, and a lint warning for hardcoded values

It designs before it writes, and starts an empty repo with the stack's official scaffolder (create-vite, `dotnet new`, `uv init`, ...), so every command in `CLAUDE.md` has actually run. Nothing is written or installed until you confirm the list. It never overwrites an existing file; it shows a diff and asks instead. It commits only when you say so.

## Install

```
/plugin marketplace add danielmsrodrigues/project-kickstart
/plugin install project-kickstart@project-kickstart
```

From a shell:

```bash
claude plugin marketplace add danielmsrodrigues/project-kickstart
```

```bash
claude plugin install project-kickstart@project-kickstart
```

## Use

In a new, empty or existing repo:

```
/kickstart booking web app for a small climbing gym
```

`/project-kickstart:kickstart` works too, and so does asking in your own words: "kickstart this repo", "bootstrap an empty project", "set up CLAUDE.md". The docs are generated in English unless you ask for another language.

## Example output

A React + TypeScript + Tailwind web app, started from an empty folder (create-vite's own files, like `vite.config.ts`, `tsconfig*.json` and `src/main.tsx`, are left out for brevity):

```
climbing-gym-booking/
├── CLAUDE.md                         # ≤80 lines: purpose, stack, commands, structure, rules, don'ts
├── AGENTS.md -> CLAUDE.md
├── README.md
├── .gitignore
├── .editorconfig
├── .claude/
│   └── settings.json                 # allow: npm run build/test/lint, token build/check; ask: git push
├── design/
│   ├── tokens.json                   # single source of truth (W3C design tokens)
│   └── build_tokens.py               # tokens → CSS/Tailwind, diff, hardcoded-value check
├── docs/
│   ├── ARCHITECTURE.md
│   ├── CONVENTIONS.md
│   ├── DESIGN.md                     # direction, token roles, layout, motion, "Avoid"
│   └── decisions/
│       └── 0001-use-react-and-vite-for-the-booking-app.md
├── package.json                      # scaffolded; + test (vitest) and tokens scripts
├── eslint.config.js                  # scaffolded; + warning rule for hardcoded colors and arbitrary values
└── src/
    ├── index.css                     # imports tailwindcss, then the tokens
    ├── styles/
    │   └── tokens.css                # generated: CSS variables + Tailwind @theme
    └── components/ui/
        ├── README.md                 # component inventory: check before creating one
        ├── Button.tsx
        ├── Input.tsx
        ├── Card.tsx
        ├── Text.tsx
        ├── Heading.tsx
        └── Stack.tsx
```

A CLI, API or library gets everything except `design/`, `DESIGN.md` and the components.

## How it works

1. **Design.** With Superpowers installed, the design runs through its `brainstorming` skill. Without it, the plugin asks up to five questions of its own, one at a time, and only ones the repo doesn't already answer.
2. **Detect the stack** from the files present (`package.json`, `*.csproj`, `Package.swift`, `pyproject.toml`, `go.mod`, `Cargo.toml`, ...) and read the real commands from them.
3. **Propose the list** and wait for your yes. In an empty repo, it starts with the scaffold and install commands. Existing files are marked and will get a diff. Choices come as buttons, with the recommendation first.
4. **Design system (UI projects only).** The plugin asks where the design comes from:
   - a Claude Design export or handoff;
   - another source: a tokens file, Figma variables, or a reference site;
   - nothing yet, in which case it asks two or three questions about tone, references and what to avoid.

   It then settles the tokens, base components and docs. If the repo already has a design system, it documents that one instead of creating a second.
5. **Scaffold and generate.** It runs the scaffolder (in a temporary folder if yours isn't empty, with git turned off) and installs dependencies. Then it writes the files, wires in the design system and runs the checks: build, test and lint, CLAUDE.md length, no placeholders left, links resolve, valid JSON, token build, hardcoded-value check.
6. **Git:** `git init` and the initial commit, only after you confirm.
7. **Hand off** to Superpowers' `writing-plans` when it's installed.

### `/tokens-sync`

For a project that already exists:

```
/tokens-sync ~/Downloads/new-export     # a new Claude Design, Figma or tokens export
/tokens-sync move our design system into tokens.json
```

- **Sync:** shows the token diff, the contrast of each change and every component that uses a changed or removed token, and applies only what you approve.
- **Adopt:** turns an informal system (CSS variables, a Tailwind theme, a Swift `Theme`) into `design/tokens.json` without changing how anything looks.

The design system lives in the repo; design tools are import sources.

## Stacks

Templates exist for Node + TypeScript, Python, .NET, Swift, Go and Rust. Any other stack starts from a generic base, adapted to what the plugin detects.

Design-system outputs:
- **Web:** CSS custom properties, plus a Tailwind v4 or v3 theme.
- **SwiftUI:** a `Theme` with dynamic light/dark colors.
- **Blazor:** CSS variables.
- **React Native:** a typed theme object.

The token tools (`build_tokens.py`) need only Python 3.8+, no packages.

## Works best with

Both are optional. The plugin checks whether each is installed and adapts.

| Plugin | What it adds here | Install |
|--------|-------------------|---------|
| [Superpowers](https://github.com/obra/superpowers) | Runs the design conversation (`brainstorming`) before any file is written, and takes over afterwards with an implementation plan (`writing-plans`). Its spec feeds the ADR and the architecture doc. | `/plugin install superpowers@claude-plugins-official` |
| [frontend-design](https://github.com/anthropics/claude-plugins-public/tree/main/plugins/frontend-design) | Sets a distinctive visual direction when the design system starts from scratch, and guides the base components and later UI work. | `/plugin install frontend-design@claude-plugins-official` |

Both live in the official marketplace (`claude-plugins-official`). If yours doesn't have it yet: `/plugin marketplace add anthropics/claude-plugins-official`.

## Contributing

New stacks and UI platforms are the most useful contributions. A stack is a folder in `skills/kickstart/templates/<stack>/` containing a `stack.md` (commands, conventions, permissions) plus optional `.gitignore`, `.editorconfig` and settings overrides. [CONTRIBUTING.md](CONTRIBUTING.md) has the steps, the allow-list rules and how to test.

Repository layout:

```
.claude-plugin/
  plugin.json                # plugin manifest
  marketplace.json           # this repo is also its own marketplace
skills/kickstart/
  SKILL.md                   # the workflow (/kickstart)
  references/                # loaded on demand: Superpowers, mini-design, stacks, generation, design system
  templates/_base/           # generic templates
  templates/<stack>/         # per-stack overrides and stack.md
  templates/_design-system/  # tokens, DESIGN.md, component inventory and contract, one file per platform
  scripts/build_tokens.py    # tokens.json → CSS / Tailwind / SwiftUI / TypeScript; diff; check
  scripts/kickstart_files.py # .gitignore, .editorconfig, settings, AGENTS.md and checks, without the model
skills/tokens-sync/
  SKILL.md                   # /tokens-sync: sync, adopt or create a design system
  references/                # importing exports (Claude Design, Figma) and the sync steps
```

To try a local checkout without installing it: `claude --plugin-dir /path/to/project-kickstart`. Before opening a PR, run `claude plugin validate .` and `claude plugin validate skills`.

## License

[MIT](LICENSE)
