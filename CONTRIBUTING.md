# Contributing

## Adding a stack

A stack is a folder under `skills/kickstart/templates/<stack>/`. It holds only what differs from `_base/`.

1. **Pick the name.** Lowercase kebab-case, named after the ecosystem, e.g. `java-gradle`, `ruby`, `elixir`.
2. **Write `stack.md`** (required). Copy the shape of an existing one, e.g. `templates/go/stack.md`:
   - `## Commands`: a table with install, build, test, single test, lint, format, run. Standard, widely used commands only; the skill replaces them with what a repo actually defines.
   - `## Conventions`: four to six rules that are idiomatic for the ecosystem and that an agent might get wrong.
   - `## Don'ts`: one to three.
   - `## Permissions`: one or two lines on what to allow and what never to allow.
3. **Add overrides** (each optional):
   - `gitignore`: appended to `_base/gitignore`. Build output, dependency folders, caches.
   - `editorconfig`: appended to `_base/editorconfig`. Only sections for the stack's own file types.
   - Any other file mirroring `_base/` (e.g. `CLAUDE.md`) replaces the base file. Avoid this unless the stack really needs a different structure.
4. **Register detection.** Add a row to the Markers table in `skills/kickstart/references/stacks.md`, and a bullet under "Reading the real commands" if the ecosystem has lockfiles or tool configs that change the commands.
5. **Test it.** In a scratch directory with only the stack's manifest file, run the skill and check that it picks your template, the generated `CLAUDE.md` stays within 80 lines, no `{{` placeholders remain, and `.claude/settings.json` is valid JSON with no destructive commands.

## Adding a UI platform to the design system

1. Add `skills/kickstart/templates/_design-system/platforms/<platform>.md` with the same sections as `web.md`: detection, token build command, wiring, fonts, components location, check, and its lint rule. Link it from `references/design-system.md`.
2. If the platform needs a new token output, add a `build_<platform>` function and a flag to `skills/kickstart/scripts/build_tokens.py`. Keep it standard-library only, and run it on `tokens.example.json` and compile the output.
3. Add a lint snippet under "Enforcement" for the platform's usual linter, as a warning that exempts token files.

## Rules for permission allow-lists

Never add: whole-tool wildcards (`Bash(npm *)`), package install or publish commands, `rm`, `git push`, `git reset`, `git clean`, network fetches, deploy commands, or long-running servers. When in doubt, leave it out; users can allow more in their own `settings.local.json`.

## Changing the skill itself

- Keep `SKILL.md` short; move detail into `references/` and keep references one level deep.
- The `description` in the frontmatter says when to use the skill, not how it works.
- Test changes with a fresh agent session against at least: an empty directory, a repo with an existing `README.md` and `.gitignore`, and a stack without a template. Run each with and without Superpowers installed.
- Templates and docs stay in English and generic: no names, organizations or project-specific references.
