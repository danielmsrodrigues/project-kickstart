# Scaffolding an empty repo

Read this when the repo has no stack marker and the stack is settled (end of step 2). Running the stack's official scaffolder before generating means the commands in `CLAUDE.md` are real and verified, and the design system can be wired in straight away (CSS entry, lint rule, `tokens` script) instead of left as "can't run yet".

## When

- **Offer it** when the repo has no manifest for the chosen stack (`package.json`, `*.csproj`, `pyproject.toml`, `Package.swift`, `go.mod`, `Cargo.toml`).
- **Skip it** when the repo already has code, when the user says no, or when the stack has no command-line scaffolder for what they're building (for example an iOS app, which needs an Xcode project: offer a Swift package for the shared code, or ask the user to create the Xcode project first).

## In the step 3 list

Scaffolding runs commands, downloads packages and creates files, so it goes in the confirmed list as `run` lines, before the files:

```
run      cd <tmp> && npx --yes create-vite@latest app --template react-ts --eslint --no-interactive --no-immediate
run      npm install
run      npm install -D vitest                    (the scaffold has no test runner)
create   CLAUDE.md
...
```

Use the command from the stack's `stack.md` "Scaffold" section. Take the template and options from the design (React vs Vue, Blazor vs Web API, library vs app), and say which you picked.

## Running it (step 4, before writing anything else)

1. **Never let the scaffolder run git.** Git happens only in step 5. Use the flags in `stack.md` (`--vcs none`, `--disable-git`). If a scaffolder created `.git` anyway, remove that new `.git` only if the repo had none before, and say so.
2. **Scaffold into a temporary directory when the repo is not empty**, or when the scaffolder refuses non-empty directories (create-vite and create-next-app both do; a Superpowers spec or `.claude/` is enough to trigger it). Create it outside the repo (`T=$(mktemp -d)`), `cd` into it and give the scaffolder a relative name (`app`), then move everything from `$T/app` in, dotfiles included. Never pass the absolute temp path to the scaffolder: create-vite reads `/var/folders/.../app` as a relative path and scaffolds into `./var/folders/...` inside the repo. If that happens anyway, move the project out and delete the stray `var/` folder this run created. A file that already exists in the repo is never replaced: keep the repo's version and handle the scaffold's version with the existing-file protocol in `generating-files.md`.
3. **Install dependencies** with the stack's install command, plus any additions confirmed in the list (test runner, Tailwind).
4. **Read the real commands** from what the scaffold produced (`package.json` scripts, the project file) and use those in `CLAUDE.md`, not the `stack.md` defaults.
5. **Edit scaffold files in place.** Files the scaffolder created in this run are not the user's: add to them directly (ignore rules, the token import, the lint rule) and list the changes in the report. Replace scaffold demo content (a counter page, a placeholder README) only where the confirmed list says so. When writing that list, look at every demo file the scaffold creates (pages, styles, images in `src/assets/` and `public/`) and give each one a `delete` or `keep` line, so nothing unused is left behind.

## After generating

Run the build, test and lint commands once. Report each as passed or failed, with the error; a command that fails is fixed or flagged in `CLAUDE.md`, never listed as if it works.
