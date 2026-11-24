# Design skills: impeccable, Emil Kowalski's skills, Playwright

Read this at the start of step 3b, and in `kickstart-design` before creating or adopting a design system. These are optional; each one that is installed replaces a weaker default of this skill. This skill still owns the files: `design/tokens.json`, `docs/DESIGN.md`, the components and the confirmed list.

**What they are for: reviewing, not inventing.** In testing, design skills asked to invent a direction produced generic pages. Asked to review a first draft and the components, they caught real problems. So the direction comes from the Claude Design canvas (`design-canvas.md`) or the user's source, and these skills review it.

## Which are installed

Check once, in one batch, and say in one line which you found.

**Using a skill means invoking it with the Skill tool** (`impeccable:impeccable`, `emil-design-eng`, `playwright-cli`) at the moment the table below names. Reading this file, or applying a skill's rules from memory, is not using it. Before showing the direction, and before the step 4 report, check that every installed skill the table names for that moment was invoked in this run; if one wasn't, invoke it and redo that part.

| Skill | Installed when | Install (for the README line and the report) |
|-------|----------------|-----------------------------------------------|
| **impeccable** | `impeccable` or `impeccable:impeccable` is in your available skills | `/plugin marketplace add pbakaus/impeccable`, then `/plugin install impeccable@impeccable` |
| **Emil Kowalski's skills** | `emil-design-eng` is in your available skills (others from the set: `animate`, `review-animations`, `break-ui`) | `npx skills@latest add emilkowalski/skills` |
| **Playwright** | a `playwright-cli` skill, `playwright-cli` on the PATH (`command -v playwright-cli`), or Playwright MCP tools | `npm install -g @playwright/cli@latest && playwright-cli install --skills` |

Never install one unasked. If none are installed, carry on with `frontend-design` or this skill's own defaults, and list the missing ones in the step 5 report with their install line.

taste-skill is not used by the kickstart: it builds whole marketing sites with its own look, and in testing its directions came out generic.

## Who does what

| Moment | impeccable | Emil's skills | Playwright |
|--------|-----------|---------------|------------|
| Before the direction | `docs/PRODUCT.md` (below) | | |
| First draft of the direction | `critique` and `detect`, from source | interactions | |
| Generic-defaults check | its absolute bans | | |
| Tokens | | motion and shadow values | |
| Components | craft floor before writing | states, press and hover, transitions | |
| After step 4 builds | `audit` | `review-animations` when there's motion | screenshots of local pages |
| `CLAUDE.md` | a line | a line | a line |

### impeccable

- **PRODUCT.md first.** Before the direction, draft `PRODUCT.md` in a temporary directory, in impeccable's product schema (its `reference/init.md`, "Write PRODUCT.md": copy the `impeccable:product-schema` comment and only the sections the design answered). Fill it from the step 1 design: users, purpose, positioning, constraints, brand commitments, evidence on hand. Point impeccable at the draft when you invoke it, so it doesn't interview the user again. It goes to `docs/PRODUCT.md` in step 4, as part of the 3b list (impeccable also finds it there later).
- **Review the first draft** as `design-canvas.md` step 4 says: `critique` from source in this context, plus `impeccable detect --json <file>`. A quick direction in text gets its bans as the generic-defaults check instead.
- **No second design doc.** impeccable writes a root `DESIGN.md` and `.impeccable/` config when asked to create. Here the design is `docs/DESIGN.md` plus `design/tokens.json`: don't let it create others.
- **Before writing UI** (the base and signature components): read its `reference/craft-floor.md` once, right before the first of these, and follow it.
- **After step 4 builds:** run its `audit` on the design-system page or the base components. Fix the P0 and P1 findings; list the rest in the report.

### Emil Kowalski's skills

- **First draft:** invoke `emil-design-eng` on the interactions of the canvas page: buttons, the key interaction, form fields.
- **Tokens:** set `motion` (durations and easing curves) and `shadow` by its rules: a strong ease-out for entering, no ease-in for UI, under 300ms, reduced motion respected, and semi-transparent shadows over solid borders where it says so.
- **Components:** build the interaction states of the base and signature components with it: hover (only on pointer devices), press at `scale(0.97)`, focus, disabled; transitions instead of keyframes for state changes.
- **Review:** when a component animates, run `review-animations` on it before the step 4 checks.
- `animate`, `break-ui` and `prototype` are for screens built after the kickstart; they go in `CLAUDE.md`, not in this run.

### Playwright

For pages served locally (the dev server, `design/preview.html`) at real widths, including 390 for a phone. It can't open the Claude Design canvas, which is private on claude.ai: that look goes through Claude in Chrome (`design-canvas.md` step 5).
- After the build: the design-system preview and the app's first screen, at 1440×900 and 390×844, light and dark.
- With `playwright-cli`: `playwright-cli open <url>`, `playwright-cli resize 1440 900`, `playwright-cli screenshot`; then `resize 390 844` and `screenshot` again; for dark, `playwright-cli set-color-scheme dark` and repeat, then `clear-color-scheme`; `playwright-cli close` at the end.
- It blocks `file://` URLs: serve a local page with `python3 -m http.server <port> --bind 127.0.0.1` from its folder (in the background, stopped afterwards), or use the dev server. Run `playwright-cli` from a temporary directory, because it saves screenshots in `.playwright-cli/` under the current one.
- With another browser tool available (Claude in Chrome, the built-in browser), it does this instead, and Playwright isn't needed.

## The CLAUDE.md lines

In the UI block, one line per installed skill, real paths, nothing for skills that aren't installed:

```markdown
- Product context lives in [docs/PRODUCT.md](docs/PRODUCT.md); `/impeccable critique` and `/impeccable audit` review a screen before a UI change is done, `/impeccable polish` finishes it.
- Interactions and motion follow the emil-design-eng skill; new animations go through `animate`, and `break-ui` stress-tests a screen with worst-case data.
- Check UI changes in a real browser with `playwright-cli` at desktop and mobile widths before saying they are done.
```

## Conflicts

- **One DESIGN.md:** `docs/DESIGN.md` plus `design/tokens.json`. If a skill offers to create another, decline it and point at these.
- **The direction wins.** A review fixes problems; it doesn't replace the approved direction with the skill's own taste. When a skill disagrees with what the user said about the look, the user's words win.
- **No double work.** `build_tokens.py contrast` is the source of truth for the token pairs; don't redo by hand what impeccable's audit already covered.
