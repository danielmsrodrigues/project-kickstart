# Working with Superpowers

Read this when `superpowers:brainstorming` is in your available skills. Superpowers ([obra/superpowers](https://github.com/obra/superpowers)) owns design and planning; this skill only adds the kickstart files in between. Do not re-implement or paraphrase what its skills do.

## Skills and paths used

| What | Name / path |
|------|-------------|
| Design skill | `superpowers:brainstorming` |
| Design doc (spec) | `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` |
| Planning skill | `superpowers:writing-plans` |
| Plan | `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md` |

On harnesses that list skills without a plugin prefix, the same skills appear as `brainstorming` and `writing-plans`.

## Step 1: design

1. If an approved spec for this project already exists in `docs/superpowers/specs/`, use it and go to step 2 of the workflow.
2. Otherwise invoke `superpowers:brainstorming` and follow it. The subject of the design is the project the user wants to build, not the kickstart files.
3. Brainstorming saves the spec and commits it. If the directory is not a git repo yet, save the spec and leave it uncommitted: it goes into the initial commit in step 5. Do not run `git init` here.
4. Brainstorming ends by invoking `superpowers:writing-plans`. **Defer that one invocation**: once the spec is approved, come back to this skill, run steps 2 to 5, and invoke `superpowers:writing-plans` in step 6. Tell the user in one line that the project guides get generated before the plan.

**Question style:** brainstorming asks its first questions, about purpose and the why, as open text on purpose; keep them that way. When it reaches a question whose choices can be named (an approach, a technical option, approving the design), ask it with the structured question tool if you have one (`AskUserQuestion` in Claude Code), recommendation first.

If the user opted out of brainstorming's questions, respect that: take what the request and repo give you, and state the remaining calls as your own in the step 3 message.

## What the spec feeds

| Spec content | Goes to |
|--------------|---------|
| Intent and the why | `CLAUDE.md` purpose, `README.md`, `docs/ARCHITECTURE.md` Purpose |
| Constraints, decided parts of the how | `docs/ARCHITECTURE.md`, `docs/CONVENTIONS.md`, Don'ts |
| Approaches considered and the pick | `docs/decisions/0001-*.md` (options, decision, consequences) |
| Non-goals and anti-goals | `CLAUDE.md` Don'ts, when an agent could plausibly violate them |

Link the spec from `docs/ARCHITECTURE.md` (Related). Never copy it.

## The line in CLAUDE.md

Only when Superpowers is installed, the Workflow section of `CLAUDE.md` gets:

```markdown
- Design work starts with superpowers:brainstorming (specs in `docs/superpowers/specs/`); implementation follows a plan from superpowers:writing-plans (plans in `docs/superpowers/plans/`).
```

## Step 6: handoff

Invoke `superpowers:writing-plans` and give it the spec path. From there Superpowers runs its own flow; this skill is finished.
