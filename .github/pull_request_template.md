## What this changes

<!-- One or two sentences. Link the issue if there is one: "Closes #12". -->

## How I tested it

<!-- For skill changes: the /kickstart or /kickstart-design prompt you ran, in what kind of folder, and what you checked. -->

- [ ] `claude plugin validate .` and `claude plugin validate skills` pass
- [ ] Ran the changed command in a scratch folder with `claude --plugin-dir <this checkout>`
- [ ] Templates and docs stay in English and generic: no names, companies or project-specific details
- [ ] If the change is user-visible: an entry under a new version in `CHANGELOG.md`, and the version bumped in `.claude-plugin/plugin.json`
