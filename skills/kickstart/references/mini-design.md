# Mini-design (without Superpowers)

Read this when `superpowers:brainstorming` is not available. The goal is just enough design to write honest guides: at most five questions, one per message. Zero is fine when the request and the repo answer everything that matters.

## Before asking

Read the request and the repo (manifest files, existing README, source layout, CI config). Cross off every topic below that they already answer.

## Topics

Ask in this order, skipping what is already known. A topic that can be recorded as an open question without making any generated file wrong (for example which CSV library to use) does not need a question: list it as open. Make a stated call on anything else still open after five questions.

If the user said to proceed without them, ask nothing here: make stated calls, record the rest as open, and put the play-back in the step 3 message.

| # | Topic | Changes |
|---|-------|---------|
| 1 | What the project is and who uses it | Purpose in `CLAUDE.md`, `README.md`, `docs/ARCHITECTURE.md` |
| 2 | Stack: language, framework, runtime (only if the repo does not show it) | Which template, all commands, `.gitignore`, `.claude/settings.json` |
| 3 | Shape: kind of thing (CLI, library, service, app), its main parts, what it talks to | Components and boundaries in `docs/ARCHITECTURE.md` |
| 4 | Decisions already made and hard constraints (hosting, data store, must-use, must-not-use) | `docs/decisions/0001-*.md`, Don'ts |
| 5 | Conventions that differ from the stack's defaults (package manager, test framework, branch flow) | `docs/CONVENTIONS.md`, commands, allow-list |

Phrase each question for this project, and say in a few words what the answer changes. When the choices can be named, offer two or three with your pick first, as buttons through the structured question tool when you have one (`AskUserQuestion` in Claude Code). Topic 1 (what it is) stays an open question in plain text.

Example, for "new project: an API for our booking app" in an empty repo:

> Which stack should this use? It decides the commands, ignore rules and permissions I generate. If you have no preference I'd go with TypeScript on Node, since the app side is likely JavaScript already.

## Play it back

Before step 2 of the workflow, summarize in five to eight lines: purpose, stack, parts, decisions, deviations from defaults. Mark anything you decided yourself as your call. Ask what is wrong or missing. This can share a message with the step 3 file list.

## At the end (step 6)

After reporting the result, add one short suggestion, once:

> For the next step (a detailed design and an implementation plan), the Superpowers skill library pairs well with this setup: https://github.com/obra/superpowers

Point to that page for installation; it differs per harness. Do not add anything about Superpowers to the generated files.
