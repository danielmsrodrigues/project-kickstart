---
name: kickstart-design
description: Brings a design into a project's design system in code. Use when the user has a new Claude Design export or handoff, Figma variables, a design-tokens file or a reference to apply to an existing project, says "sync the design system", "update the tokens", "import this design", "show me the design system", or wants a project's hardcoded colors and CSS variables turned into a token source of truth (design/tokens.json).
argument-hint: "[path to the export, or what changed]"
---

# Kickstart Design

Invoked as `/kickstart-design` (or `/project-kickstart:kickstart-design`). Text after the command is the export's location or what changed.

**Principle:** the design system lives in the repo as code: `design/tokens.json` is the single source, and generated files, components, `docs/DESIGN.md` and the component inventory follow it. Claude Design, Figma and other tools are import sources. Nothing is applied before the user has seen the diff and said yes.

`<skill>` is this skill's base directory; the shared design-system files live in `<skill>/../kickstart/`.

## Rules

- **Diff first, apply on a yes.** Ask with the structured question tool when you have one (`AskUserQuestion` in Claude Code), recommendation first.
- **Never overwrite** a file you weren't asked to change; generated token files are rebuilt, never hand-edited.
- **Work in few round trips:** read in parallel batches, chain shell commands, never read a file only to copy it (`build_tokens.py --help` shows its usage).
- **Git:** offer a commit at the end; don't make one unasked.

## Pick the mode

Look at the repo once (one batch): `design/tokens.json`, other `tokens.*`, CSS custom properties, a Tailwind theme, a Swift `Theme`/`Colors` type, a component-library theme, a components folder and its `README.md`.

| The repo has | Mode |
|--------------|------|
| `design/tokens.json`, and the user only wants to see it | **Show**: follow `<skill>/../kickstart/references/preview.md` |
| `design/tokens.json` | **Sync**: follow `references/design-sync.md` |
| A design system in another form (CSS variables, a Tailwind theme, a `Theme` type) but no `tokens.json` | **Adopt**, below |
| No design system | **Create**: follow `<skill>/../kickstart/references/design-system.md` from "1. Origin", and generate only the design-system files (no CLAUDE.md, ADR or configs). If the repo has no `CLAUDE.md` either, suggest `/kickstart` instead. |

For reading the export itself (Claude Design bundle, Figma variables JSON, a tokens file, a reference site), see `references/design-import.md`.

## Adopt

Turn an existing system into `design/tokens.json` without changing how anything looks.

Until the user says yes, the repo stays untouched: draft and build in a temporary directory.

1. **Draft** the tokens file in the temporary directory: every value from the current source, in W3C DTCG with the structure of `<skill>/../kickstart/templates/_design-system/tokens.example.json`. Keep the existing names wherever they already describe a role, so usages don't change. Where a name is a raw value (`blue-600`), propose a role name.
2. **Framework defaults the code relies on.** With Tailwind v4 the generator clears the default color palette, so every class that uses it (`text-white`, `bg-gray-100`, `border-red-500`) would silently lose its color. Search for them, give each one a role token with the exact same value, and add them to the renames.
3. **Build, compare, and check contrast.** Run `python3 <skill>/../kickstart/scripts/build_tokens.py contrast <draft>`, and report failures as findings: adopting must not change the look, so fixing them is a follow-up, not part of adopting. Then build the draft with `python3 <skill>/../kickstart/scripts/build_tokens.py build <draft> --css <tmp>/tokens.css ...`. The values must match the current source exactly, except for the listed renames.
4. **Show and wait.** Show the token list, the renames with their usage counts, and the files that would change. Wait for a yes.
5. **On yes:**
   - Write `design/tokens.json`, and `cp` the script to `design/build_tokens.py`.
   - Build into the real output path and point the app at it, replacing the hand-written source.
   - Apply the renames.
   - Write or update `docs/DESIGN.md` and the inventory from the kickstart templates.
   - Add the platform's lint warning (`<skill>/../kickstart/templates/_design-system/platforms/<platform>.md`).
   - Add the token commands to `CLAUDE.md` if it exists.
6. Verify: compare the compiled output before and after (every class the app uses resolves to the same value), the build passes, `python3 design/build_tokens.py check <ui source>` runs (report its findings; fixing hardcoded values in screens is a follow-up, not part of adopting), and the UI looks the same where you can check it.

If the user brought a new export too, adopt first, then sync the export.

## After any change

Whenever `design/tokens.json` was created or changed (sync, adopt, create), end by showing it: follow `<skill>/../kickstart/references/preview.md`. It republishes to the `Preview:` link in `docs/DESIGN.md` when there is one.
