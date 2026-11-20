# project-kickstart

**Start a software project the right way, by describing it in one sentence.**

project-kickstart is a plugin for [Claude Code](https://claude.com/claude-code). You type `/kickstart` and what you want to build. Claude then asks a few questions, shows you its plan, and once you agree, sets up the project:

- the starting code, created with the official tools for your technology;
- written guides, so Claude and your teammates understand the project from day one;
- safe settings, so Claude can build and test the project without asking each time, but never deletes or publishes anything on its own;
- **if the project has screens**, a *design system*: the app's colors, fonts and spacing in one place, plus a few ready-made building blocks (buttons, inputs, cards) that use them.

It never changes anything without showing you first, and it never writes over your files.

## Which command do I use?

| Your situation | Command |
|----------------|---------|
| Starting a **new project** (an empty folder) | `/kickstart` and a sentence about the project |
| A project that **already exists** but has no guides for Claude | `/kickstart` |
| Your designer sent a **new design** (from Claude Design, Figma, or a file of colors and fonts) for a project that already has a design system | `/kickstart-design` and where the file is |
| An existing project with colors and styles **scattered around the code**, which you want organised in one place | `/kickstart-design` |

**You don't need `/kickstart-design` for a new project.** `/kickstart` creates the design system by itself whenever the project has screens.

## Quick start

**1. Install it** (once). In Claude Code, type:

```
/plugin marketplace add danielmsrodrigues/project-kickstart
/plugin install project-kickstart@project-kickstart
```

**2. Open Claude Code in an empty folder** and describe what you want:

```
/kickstart booking app for a small barbershop
```

You don't have to choose the technology. If you don't say, Claude suggests one and explains why. If you already know ("in React", "in .NET"), say it and save a question.

**3. Answer the questions.** Most come with ready-made answers to click, with the recommended one first. Then:

- Claude shows you **the full list** of what it will do: commands to run, files to create, files to change. **Nothing happens until you say yes.**
- If the project has screens, it asks **where the design comes from**: a Claude Design export, another file, or nothing yet. With nothing yet, it asks about the look you want (for example "warm and classic, nothing like a generic app") and proposes colors and fonts for you to approve.
- At the end it asks before saving anything to git.

A complete kickstart takes about 10 to 20 minutes, most of it Claude working while you wait.

## Example prompts

One sentence is enough. Add more only if you already know it.

**Starting something new**

```
/kickstart booking app for a small barbershop
```
```
/kickstart online menu and table reservations for a restaurant, in React
```
```
/kickstart internal dashboard to track our team's support tickets
```
```
/kickstart iPhone app for logging gym workouts, in SwiftUI
```
```
/kickstart REST API for a library's book loans, in .NET, no screens
```
```
/kickstart command-line tool that renames photos by the date they were taken, in Python
```

**With details you already know**

```
/kickstart booking app for a hair salon. Clients book online, staff see the day's schedule. Next.js and Supabase. Write the docs in Portuguese.
```
```
/kickstart landing page for a bakery. Warm and handmade look, nothing like a generic startup site.
```
```
/kickstart dashboard for our sales team. The design is in this Claude Design export: ~/Downloads/sales-dashboard.zip
```

**A project that already exists**

```
/kickstart
```
```
/kickstart this is our company website, set it up so Claude understands it
```

**Bringing in a design later** (`/kickstart-design`)

```
/kickstart-design ~/Downloads/new-brand-colors.zip
```
```
/kickstart-design the designer changed the main color and the fonts in Figma, here's the export: ~/Downloads/figma-variables.json
```
```
/kickstart-design our colors are scattered around the CSS, put them in one place without changing how the site looks
```

## What you get

For a web app with screens, started from an empty folder:

| What | In plain words |
|------|----------------|
| `CLAUDE.md` and `AGENTS.md` | A one-page guide for AI assistants: what the project is, how to run it, the rules to follow. Every command in it has actually been run. |
| `README.md` | The project's front page, for people. |
| `docs/ARCHITECTURE.md` | How the project is organised, plus the questions still open. |
| `docs/CONVENTIONS.md` | The team's rules for code: naming, tests, folders. |
| `docs/decisions/0001-….md` | The first important decision and why it was made, so nobody has to guess later. |
| `docs/DESIGN.md` | The visual direction in one sentence, what each color and size is for, and a list of looks to avoid. |
| `design/tokens.json` | **The single place where colors, fonts and spacing are defined.** Change a color here and the whole app follows. |
| `src/components/ui/` | Six building blocks (button, input, card, text, heading, layout), plus a list of them that is checked before anyone creates a new one, so the same button isn't built twice. |
| `.claude/settings.json` | What Claude may run without asking (build, test, check). It always asks before publishing code, and can't read secret files. |
| The starting code | Created with the official tool for the technology (for example Vite for React), with packages installed and the design system already connected. |

A project without screens (a command-line tool, a backend, a library) gets the same minus the design part.

## Promises

- **Nothing is written, installed or run before you see the list and say yes.**
- **Your files are never replaced.** If a file already exists, you see exactly what would change and decide.
- **Nothing is saved to git or published unless you ask.**
- **No guessing.** What isn't decided yet is written down as an open question, not invented.

## Questions

**Does it create the design system by itself?**
Yes, in `/kickstart`, for any project with screens. `/kickstart-design` is only for projects that already exist: bringing in a new design later, or organising styles that are scattered around the code.

**What if my project already has code?**
`/kickstart` reads it, uses the commands it finds, and writes the guides around what's there. If it finds an existing set of colors and styles, it documents it rather than creating a second one, and offers `/kickstart-design` to organise it without changing how anything looks.

**Can the docs be in my language?**
Yes, just ask (for example "write the docs in Portuguese"). English is the default.

**How do I get updates?**
In Claude Code, type `/plugin`, open **Marketplaces**, choose **project-kickstart** and turn on **auto-update**. Or update by hand:

```bash
claude plugin update project-kickstart@project-kickstart
```

**I typed `/kick` and the menu shows `project-kickstart:kickstart`. Is that right?**
Yes. That's the full name; typing `/kickstart` on its own works the same.

## Works best with

Both are optional. Install them and project-kickstart uses them automatically.

| Plugin | What it adds | Install |
|--------|--------------|---------|
| [Superpowers](https://github.com/obra/superpowers) | A better design conversation before anything is built, and a step-by-step plan for building the app afterwards. | `/plugin install superpowers@claude-plugins-official` |
| [frontend-design](https://github.com/anthropics/claude-plugins-public/tree/main/plugins/frontend-design) | A more distinctive look when the design starts from scratch, and better-looking screens later. | `/plugin install frontend-design@claude-plugins-official` |

If Claude Code doesn't find them, add the official marketplace first: `/plugin marketplace add anthropics/claude-plugins-official`.

---

## For developers

### How `/kickstart` works

1. **Design.** With Superpowers installed, the design runs through its `brainstorming` skill. Without it, up to five questions of its own, one at a time, skipping what the repo already answers.
2. **Detect the stack** from `package.json`, `*.csproj`, `Package.swift`, `pyproject.toml`, `go.mod`, `Cargo.toml`, ... and read the real commands from them.
3. **Propose the list** (`run`, `create`, `edit`, `exists` lines) and wait for a yes. Choices are asked through `AskUserQuestion` when available.
4. **Design system** for UI projects: origin (Claude Design, another source, or none), `design/tokens.json` in W3C DTCG format, generated native tokens, six base components, `docs/DESIGN.md`, an inventory, and a lint warning for hardcoded values. An existing system is documented, never duplicated.
5. **Scaffold and generate.** The official scaffolder runs first (create-vite, create-next-app, `uv init`, `dotnet new`, `swift package init`, `cargo init`, `go mod init`): in a temporary directory if the folder isn't empty, with git turned off. Then dependencies are installed, files written, and checks run: build, test, lint, `CLAUDE.md` ≤ 80 lines, no placeholders, links resolve, valid JSON, token build, hardcoded-value check.
6. **Git:** `git init` and the initial commit only after a yes.
7. **Hand off** to Superpowers' `writing-plans` when it's installed.

### `/kickstart-design`

```
/kickstart-design ~/Downloads/new-export
/kickstart-design move our design system into tokens.json
```

- **Sync:** diffs a new export against `design/tokens.json`, with the contrast of each change, every usage of changed or removed tokens, and blockers (removed tokens still in use). Applies only what's approved.
- **Adopt:** turns CSS variables, a Tailwind theme or a Swift `Theme` into `design/tokens.json`. The compiled output is identical before and after.
- **Create:** only the design-system files, for a repo with none.

### Example tree

React + TypeScript + Tailwind, from an empty folder (create-vite's own `vite.config.ts`, `tsconfig*.json` and `src/main.tsx` left out):

```
barbershop-booking/
├── CLAUDE.md                         # ≤80 lines: purpose, stack, commands, structure, rules, don'ts
├── AGENTS.md -> CLAUDE.md
├── README.md
├── .gitignore, .editorconfig
├── .claude/settings.json             # allow: build/test/lint/tokens; ask: git push; deny: .env
├── design/
│   ├── tokens.json                   # single source of truth (W3C design tokens)
│   └── build_tokens.py               # tokens → CSS/Tailwind, diff, hardcoded-value check
├── docs/
│   ├── ARCHITECTURE.md, CONVENTIONS.md, DESIGN.md
│   └── decisions/0001-build-against-a-booking-service-interface.md
├── package.json                      # scaffolded; + test (vitest) and tokens scripts
├── eslint.config.js                  # scaffolded; + warning for hardcoded colors and arbitrary values
└── src/
    ├── index.css                     # @import "tailwindcss", then the tokens and fonts
    ├── styles/tokens.css             # generated
    └── components/ui/                # Button, Input, Card, Text, Heading, Stack + README.md inventory
```

### Stacks and platforms

Stack templates: Node + TypeScript, Python, .NET, Swift, Go and Rust. Any other stack starts from a generic base. Design-system outputs:
- **Web:** CSS custom properties, plus a Tailwind v4 or v3 theme.
- **SwiftUI:** a `Theme` with dynamic light/dark colors.
- **Blazor:** CSS variables.
- **React Native:** a typed theme object.

The bundled scripts need only Python 3.8+.

### Contributing

New stacks and UI platforms are the most useful contributions; [CONTRIBUTING.md](CONTRIBUTING.md) has the steps. Layout:

```
.claude-plugin/
  plugin.json                # plugin manifest
  marketplace.json           # this repo is also its own marketplace
skills/kickstart/
  SKILL.md                   # /kickstart
  references/                # loaded on demand: Superpowers, mini-design, stacks, scaffolding, generation, design system
  templates/_base/           # generic templates
  templates/<stack>/         # stack.md (commands, scaffold, conventions) and overrides
  templates/_design-system/  # tokens, DESIGN.md, component inventory and contract, one file per platform
  scripts/build_tokens.py    # tokens.json → CSS / Tailwind / SwiftUI / TypeScript; diff; check
  scripts/kickstart_files.py # .gitignore, .editorconfig, settings, AGENTS.md and checks, without the model
skills/kickstart-design/
  SKILL.md                   # /kickstart-design: sync, adopt or create
  references/                # importing exports (Claude Design, Figma) and the sync steps
```

Try a local checkout with `claude --plugin-dir /path/to/project-kickstart`. Before a PR, run `claude plugin validate .` and `claude plugin validate skills`.

## License

[MIT](LICENSE)
