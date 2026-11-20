<!--
Template for docs/CONVENTIONS.md. Start from the stack's stack.md "Conventions" list,
then add anything the design or the existing code already establishes.
Prefer rules a linter/formatter enforces; name the tool instead of restating its rules.
Delete this comment block.
-->
# Conventions

## Code style

- Formatting is enforced by {{FORMATTER}}; run `{{FORMAT_COMMAND}}`. Don't hand-format.
- Linting: {{LINTER}} (`{{LINT_COMMAND}}`).
{{STACK CONVENTIONS FROM stack.md}}

## Naming

{{FILES, TYPES, FUNCTIONS, TESTS: the stack's idiomatic casing, plus project-specific prefixes/suffixes}}

## Project layout

{{WHERE NEW CODE GOES: one bullet per kind of thing (feature, test, script, config)}}

## Testing

- Tests live in {{TEST_LOCATION}} and run with `{{TEST_COMMAND}}`.
- Every bug fix comes with a test that fails without the fix.
{{TEST NAMING AND FIXTURE RULES}}

## Errors and logging

{{HOW ERRORS ARE RAISED/RETURNED AND WHAT GETS LOGGED; never log secrets or personal data}}

## Dependencies

- Add a dependency only when it saves real work; note why in the commit message.
- Pin versions with the lockfile ({{LOCKFILE}}); commit it.

## Git

- Small commits with imperative messages ("Add invoice export", not "Added stuff").
{{BRANCH AND PR CONVENTIONS, if decided}}

## Documentation

- Significant decisions get an ADR in [decisions/](decisions/) (copy the format of 0001).
- Keep [ARCHITECTURE.md](ARCHITECTURE.md) and this file current in the same change that makes them stale.
