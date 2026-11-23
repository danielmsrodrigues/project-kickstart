# Generating the files (step 4)

`<skill>` is this skill's directory. The mechanical files come from a script, so you only write what needs judgement:

| Job | How |
|-----|-----|
| `.gitignore`, `.editorconfig`, and `design/build_tokens.py` for a UI | `python3 <skill>/scripts/kickstart_files.py files --stack <stack> --dest . [--ui] [--merge]` |
| `.claude/settings.json` | `... settings --allow "<cmd>" "<cmd>" ...` prints it; write it with your file tool |
| `AGENTS.md` | `... agents --dest .`, after `CLAUDE.md` exists (symlink, or a marked copy on Windows) |
| Checks | `... check --dest . <every file you wrote>` |

`--stack` is the template folder name (`node-typescript`, `python`, `dotnet`, `swift`, `go`, `rust`); leave it empty for other stacks. `--merge` is only for a `.gitignore` a scaffolder created in this run. Exit code 3 means an existing file was left alone and its diff printed: show it and ask (see Existing files).

## Writing the rest

Read the templates you need in one batch (parallel reads), then write the independent files in one batch: `_base/CLAUDE.md`, `_base/README.md`, `_base/docs/ARCHITECTURE.md`, `_base/docs/CONVENTIONS.md`, `_base/docs/decisions/0001-adr.md` and the stack's `stack.md`. Each template has `{{PLACEHOLDERS}}` and an instruction comment. Fill every placeholder from the design, the repo and `stack.md`, delete any section that would only hold a guess, and remove the comment.

- **CLAUDE.md:**
  - At most 80 lines.
  - Commands follow "Real beats default"; drop a line when no working command exists for it.
  - Structure is the real tree; planned directories are marked `(planned)`.
  - Conventions are only the three to six rules an agent would get wrong; the rest stays in CONVENTIONS.md.
  - The Superpowers line appears only if Superpowers is installed. The UI block appears only if 3b ran, and frontend-design and the design skills (`design-skills.md`) are mentioned there only if they're installed.
- **ARCHITECTURE.md:** what's decided. Unknowns go under "Open questions".
- **CONVENTIONS.md:** the `stack.md` conventions plus what the design or code establishes. Name the linter or formatter instead of restating its rules.
- **ADR 0001:** the design's main decision, with a short imperative title and today's date. Its options are the approaches actually considered. If none were, say so instead of inventing any.
- **README.md:** for humans. A runtime version only if the repo pins one.
- **settings allow-list:** pass only the exact build, test, lint, format, type-check and token commands written in CLAUDE.md. The script refuses `rm`, installs, publishes, `git push/reset/clean`, network fetches and wildcards. Claude Code protects `.claude/settings.json`: if the write is blocked, show the content and ask for approval; don't save it anywhere else.

## Existing files

Never write over a file that exists. Read it, prepare the smallest change that adds what's missing, keeping everything the user wrote, and show it as a diff. Ask whether to apply it, skip it, or write `<file>.kickstart`. An existing `CLAUDE.md` or `AGENTS.md` gets additions, never a rewrite. Files a scaffolder created in this run are not the user's: edit them directly (see `scaffolding.md`).

## Checks

Run `check` with every file you wrote, and fix failures. A link to a file the user dropped is removed, not left dangling. If dependencies are installed, also run the build, test and lint commands, together in one shell call (`cmd1; cmd2; cmd3`), and report each result. Don't install dependencies only to run checks.
