---
name: kickstart
description: Sets up the baseline files, AI agent guides and design system for a project. Use when starting a new project or working in an empty or near-empty repo that lacks agent guidance - the user says "new project", "kickstart", "bootstrap", "scaffold", "empty repo" or "set up CLAUDE.md", or asks for AGENTS.md, initial architecture docs, conventions, ADRs, or starter configs (.gitignore, .editorconfig, .claude/settings.json). Also use when the user brings a new Claude Design, Figma or design-token export to sync into a project's design system.
argument-hint: "[what you are building, e.g. \"booking web app for a climbing gym\"]"
---

# Project Kickstart

Invoked as `/kickstart` (or `/project-kickstart:kickstart`). Text after the command is the user's description of the project: treat it as their first answer.

Gives a new or empty repo what an agent and a human need on day one: a short `CLAUDE.md`/`AGENTS.md`, architecture and conventions docs, a first ADR, safe configs, the stack's official scaffold and, for a UI, a design system in code. **Core principle:** design first, then generate only what the design and the repo justify. A guide full of guesses is worse than none. Product code stops at the scaffold and the base UI components; planning belongs to Superpowers when it's installed.

`<skill>` below is this skill's base directory.

## Rules

- **Never overwrite an existing file.** Show a diff and ask.
- **Nothing is written or run before the list is confirmed** (step 3). No `git init` or commit before its own yes (step 5).
- **Ask only what changes the output**, and only what the request and repo don't answer, one question per message. When the choices can be named (stack, template, design origin, confirming the list, git), ask with the structured question tool if you have one (`AskUserQuestion` in Claude Code): two to four options, recommendation first. Questions about purpose stay open text.
- **Docs in the user's language** if they ask; otherwise English. File names in English.
- **Real beats default.** Commands, paths and names in the repo win over templates. A `stack.md` default goes in only when the repo defines nothing, and is marked unverified. **Unknown is a valid answer:** it goes under "Open questions", never guessed.
- **Work in few round trips.** Each tool call re-reads the whole context, so:
  - Read what a step needs in one parallel batch, and write independent files in one batch.
  - Chain shell commands in one call.
  - Use `<skill>/scripts/` for mechanical files and checks.
  - Never read a file only to copy it. Don't re-read files you just wrote, and don't print generated output (`tokens.css`, build logs) to inspect it: the build, `check` and lint commands verify it.

## Workflow

### 1. Design

Superpowers is installed if and only if `superpowers:brainstorming` is in your available skills.
- **Installed:** read `references/superpowers.md`, then run the design through `superpowers:brainstorming`.
- **Not installed:** read `references/mini-design.md` and run it.

You leave this step with the purpose, stack, main parts, decisions made, and conventions that differ from the defaults.

### 2. Detect the stack

Read `references/stacks.md`. Detect the stack from the files present and read the real commands from them; if there is no marker and the design didn't settle it, ask. With no template for the stack, use `templates/_base/` and adapt. **Empty repo:** also read `references/scaffolding.md`. The official scaffolder runs before anything is generated, unless the user declines.

### 3. Propose the list and confirm

One message with the design summary and every action:

```
run      npx --yes create-vite@latest <tmp> --template react-ts --eslint --no-interactive --no-immediate
run      npm install
create   CLAUDE.md
symlink  AGENTS.md -> CLAUDE.md
create   docs/ARCHITECTURE.md, docs/CONVENTIONS.md, docs/decisions/0001-<title>.md
create   .editorconfig, .claude/settings.json
edit     .gitignore   (scaffold's; base rules appended)
exists   README.md    (will show a diff and ask)
```

Flag commands that can't work yet. Then wait for the yes; this can't be skipped even if the user said to just go ahead.

### 3b. Design system (projects with a UI)

Read `references/design-system.md` and follow it. It covers asking where the design comes from (Claude Design, another source, or none), documenting an existing system instead of building a parallel one, the tokens, the base components, `DESIGN.md`, the inventory and the lint rule. It ends with its own additions to the list and a yes. A CLI, API or library skips 3b.

### 4. Generate

1. Run the `run` lines as `references/scaffolding.md` says.
2. Follow `references/generating-files.md`: the script makes `.gitignore`, `.editorconfig`, the settings JSON, `AGENTS.md` and the checks; you fill the doc templates.
3. Write the design-system files from 3b.
4. Run the checks, plus build, test and lint when the dependencies are installed. Fix what fails.

### 5. Git

Report what was created and what failed. Then ask once whether to run `git init` (if needed) and make the initial commit. On yes, stage only the files this skill created or the user approved changing.

### 6. Hand off

With Superpowers, invoke `superpowers:writing-plans` with the approved spec. Without it, say the kickstart is done and suggest Superpowers (see `references/mini-design.md`).

## Sync mode

A project that already has a design system and a new Claude Design, Figma or tokens export (or "sync the design system"): that's the `kickstart-design` skill (`/kickstart-design`), not this one. Invoke it instead of running steps 1-5.

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Writing right after the design | The list in step 3 always comes first. |
| Replacing a user's README or `.gitignore` | Diff and ask; appending is a change too. |
| A scaffolder running `git init`, or refusing a non-empty folder | Use the flags in `stack.md` and a temp directory. |
| `CLAUDE.md` restating the docs | Keep the rules an agent would get wrong; link the rest. |
| Leftover `{{PLACEHOLDER}}` or TODO sections | Fill them or delete the section. |
| A second design system next to an existing one | Document and extend the one that's there. |
| Applying a design export directly | `/kickstart-design`: diff first, apply on a yes. |
| Reading `build_tokens.py` or a template just to copy it | `kickstart_files.py` copies; `--help` explains. |
