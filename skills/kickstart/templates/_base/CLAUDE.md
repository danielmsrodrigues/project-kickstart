<!--
Template for the generated CLAUDE.md (and AGENTS.md).
Fill every {{PLACEHOLDER}}; delete any section that would only hold a TODO.
Hard limit: 80 lines after filling. Link to docs, never copy their content.
Delete this comment block.
-->
# {{PROJECT_NAME}}

{{ONE_OR_TWO_SENTENCES: what this project is, who uses it, why it exists}}

## Stack

{{BULLETS: language + version, framework, key libraries, data store, runtime/hosting. Only what is decided.}}

## Commands

```bash
{{INSTALL_COMMAND}}   # install dependencies
{{BUILD_COMMAND}}     # build
{{TEST_COMMAND}}      # run all tests
{{SINGLE_TEST_COMMAND}}   # run one test
{{LINT_COMMAND}}      # lint / format check
{{RUN_COMMAND}}       # run locally
```

## Structure

```
{{TOP_LEVEL_TREE: 4-8 lines, one comment per entry}}
```

## Conventions

{{3-6 BULLETS: only the rules an agent would get wrong without being told. Everything else lives in docs/CONVENTIONS.md.}}

- Full conventions: [docs/CONVENTIONS.md](docs/CONVENTIONS.md)
- Architecture and boundaries: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- Decisions and their reasons: [docs/decisions/](docs/decisions/)

{{UI_BLOCK: include ONLY when the project has a UI (design-system step ran). Real paths; keep it this short:
## UI and design system

- Tokens: `design/tokens.json` is the source; rebuild with `{{BUILD_TOKENS_COMMAND}}`. Never edit generated token files.
- Before creating a component, check [{{COMPONENTS_DIR}}/README.md]({{COMPONENTS_DIR}}/README.md). If something similar exists, extend it with a variant or prop.
- No hardcoded colors, sizes, spacing or radii in screens: tokens only. `{{CHECK_COMMAND}}` flags them.
- Screens compose components. New styles go into a component or the tokens, never into a screen.
- A new or changed component updates `{{COMPONENTS_DIR}}/README.md` in the same commit (and `design/system/entry.ts` when it's new); then `/kickstart-design` refreshes the published design system.
- For UI work, follow [docs/DESIGN.md](docs/DESIGN.md){{FRONTEND_DESIGN: append " and use the frontend-design skill" ONLY if it is installed}}.
}}

## Don'ts

- Don't commit secrets or `.env` files; use `.env.example` for the variable names.
- Don't add dependencies without saying why in the PR or commit message.
- Don't change public interfaces or data formats without a new ADR in `docs/decisions/`.
{{0-3 MORE STACK- OR PROJECT-SPECIFIC DON'TS}}

## Workflow

- Run `{{TEST_COMMAND}}` and `{{LINT_COMMAND}}` before saying a change is done.
- When a change alters architecture or conventions, update the matching doc in the same change.
{{SUPERPOWERS_LINE: include ONLY if Superpowers is installed, e.g.
"- Design work starts with superpowers:brainstorming (specs in docs/superpowers/specs/); implementation follows a plan from superpowers:writing-plans (docs/superpowers/plans/)."}}
