---
name: kickstart
description: Sets up the baseline files, AI agent guides and design system for a project. Use when starting a new project or working in an empty or near-empty repo that lacks agent guidance - the user says "new project", "kickstart", "bootstrap", "scaffold", "empty repo" or "set up CLAUDE.md", or asks for AGENTS.md, initial architecture docs, conventions, ADRs, or starter configs (.gitignore, .editorconfig, .claude/settings.json). Also use when the user brings a new Claude Design, Figma or design-token export to sync into a project's design system.
argument-hint: "[what you are building, e.g. \"booking web app for a climbing gym\"]"
---

# Project Kickstart

Invoked as `/kickstart` (or `/project-kickstart:kickstart`). Text after the command is the user's description of the project: treat it as their first answer.

## Overview

Give a new or empty repo the files an AI agent and a human need on day one: a short `CLAUDE.md`/`AGENTS.md`, architecture and conventions docs, a first ADR, safe configs and, for projects with a UI, a design system in code.

**Core principle:** design first, then generate only what the design and the repo justify. A guide full of guesses is worse than no guide.

This skill does not scaffold product code beyond the base UI components, and does not plan implementation. With Superpowers installed, design and planning are delegated to it.

## Rules

- **Never overwrite an existing file.** Show a diff of what you would change and ask.
- **Nothing is written before the file list is confirmed** (step 3). No `git init` or commit before its own confirmation (step 5).
- **Ask a question only when its answer changes a generated file** and neither the request nor the repo answers it. One question per message.
- **Generated docs use the language the user asked for; otherwise English.** File names stay in English.
- **Real beats default:** commands, paths and names found in the repo win over template defaults. A `stack.md` default goes in only when the repo defines nothing for that purpose, and the step 3 message marks it unverified. Never write a command from anywhere else.
- **Unknown is a valid answer.** What neither the user nor the repo settles goes under "Open questions" in `docs/ARCHITECTURE.md` or is left out, never guessed.

## Workflow

Follow the steps in order (one todo per step if you have a task list).

### 1. Design

Superpowers is installed if and only if `superpowers:brainstorming` is in your available skills.

- **Installed:** read [references/superpowers.md](references/superpowers.md), then run the design through `superpowers:brainstorming`.
- **Not installed:** read [references/mini-design.md](references/mini-design.md) and run the mini-design.

Either way you leave this step with: purpose, stack, main components, decisions already made, and conventions that differ from the stack's defaults.

### 2. Detect the stack

Read [references/stacks.md](references/stacks.md). Detect from the files present (`package.json`, `*.csproj`, `Package.swift`, `pyproject.toml`, `go.mod`, `Cargo.toml`, ...) and read the real commands from them. If the repo has no stack marker and the design did not settle it, ask.

No template for the stack: use `templates/_base/` and adapt it to what you detected.

### 3. Propose the file list and confirm

Show every file with its action, then wait for a yes:

```
create   CLAUDE.md
symlink  AGENTS.md -> CLAUDE.md
create   docs/ARCHITECTURE.md
create   docs/CONVENTIONS.md
create   docs/decisions/0001-use-postgresql-for-persistence.md
create   .editorconfig
create   .claude/settings.json
exists   .gitignore   (will show a diff and ask)
exists   README.md    (will show a diff and ask)
```

In the same message, flag commands that exist but cannot work yet (for example a `build` script with no `tsconfig.json`). The user may drop or add entries. Generate exactly the confirmed list.

If the user said to go ahead without them ("just do it", "I'm stepping away"), still stop here: send the design summary and this list in one message and wait. This confirmation cannot be skipped, and neither can the design-system origin question in 3b when no design source is in the repo or the conversation.

### 3b. Design system (projects with a UI)

Required when the project has a UI; a CLI, API or library skips to step 4. Read [references/design-system.md](references/design-system.md) and follow it: check for an existing design system (document it, never build a parallel one), ask the origin (Claude Design export, another source, or none), turn it into `design/tokens.json` plus native token files, write the base components, `docs/DESIGN.md` and the component inventory, and add a lint warning for hardcoded values.

The design system lives in the repo as code. External design tools are import sources only.

Step 3b decides (questions, token values, file list) and gets a yes; step 4 writes and builds.

### 4. Generate

Read [references/generating-files.md](references/generating-files.md) before writing anything. It covers template resolution (`templates/_base/` plus `templates/<stack>/` overrides), per-file rules, the existing-file protocol, the `AGENTS.md` symlink-or-copy rule, and the checks to run afterwards.

Files, when confirmed in step 3:

| File | Shape |
|------|-------|
| `CLAUDE.md` | At most 80 lines: purpose, stack, commands (build/test/run/lint), structure, essential conventions, don'ts. Links to the docs instead of repeating them. |
| `AGENTS.md` | Same content as `CLAUDE.md`: symlink where supported, copy on Windows. |
| `docs/ARCHITECTURE.md` | Components, boundaries, data, open questions. |
| `docs/CONVENTIONS.md` | Style, naming, layout, testing, git. |
| `docs/decisions/0001-<title>.md` | ADR recording the design's main decision. |
| `.gitignore`, `.editorconfig`, `README.md` | Base plus stack section. |
| `.claude/settings.json` | Allow-list for the stack's build/test/lint commands only. Nothing destructive. |
| UI only: `design/`, token outputs, base components, `docs/DESIGN.md`, inventory | As set in step 3b. |

Run the checks in the reference and fix what fails before moving on.

### 5. Git

Report what was created. Then ask once: initialize git (if there is no repo) and make the initial commit? On yes, run `git init` if needed, stage only the files this skill created or the user approved changing, and commit. On no, leave everything uncommitted.

### 6. Hand off

- **Superpowers installed:** invoke `superpowers:writing-plans` with the approved spec.
- **Not installed:** say the kickstart is done and suggest Superpowers, as described in [references/mini-design.md](references/mini-design.md).

## Sync mode

When a project already has `design/tokens.json` and the user brings a new Claude Design export or another design source ("sync the design system", "here's the new export"), skip steps 1-5 and run "Sync mode" in [references/design-system.md](references/design-system.md): show the token diff and the affected components, and apply only what the user approves.

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Writing files right after the design, skipping the list | Step 3 always runs, even for an empty repo. |
| Replacing a hand-written `README.md` or `.gitignore` | Existing file: diff and ask. Appending is still a change. |
| `CLAUDE.md` that restates the conventions doc | Keep the few rules an agent would get wrong; link the rest. |
| Template defaults for commands the repo defines differently | Read `package.json` scripts, `Makefile`, CI files first. |
| Leaving `{{PLACEHOLDER}}` or "TODO" sections | Fill it or delete the section. |
| `Bash(npm *)`, `Bash(rm *)` or `git push` in the allow-list | Exact build/test/lint commands only. |
| Mentioning Superpowers in `CLAUDE.md` when it is not installed | Include that line only when step 1 found it. |
| Asking the mini-design questions as a form | One at a time, skipping any the repo already answers. |
| A second token set or component folder next to an existing one | Existing design system: document it and extend it. |
| Treating the Claude Design project as the source of truth | Import into `design/tokens.json`; the repo wins on the next sync. |
| Applying a new design export directly | Sync mode: diff first, apply on a yes. |
