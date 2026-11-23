# Design skills: impeccable, taste-skill, Emil Kowalski's skills, Playwright

Read this at the start of step 3b, and in `kickstart-design` before creating or adopting a design system. These are optional; each one that is installed replaces a weaker default of this skill. This skill still owns the files: `design/tokens.json`, `docs/DESIGN.md`, the components and the confirmed list. The design skills bring judgement, rules and checks.

## Which are installed

Check once, in one batch, and say in one line which you found.

| Skill | Installed when | Install (for the README line and the report) |
|-------|----------------|-----------------------------------------------|
| **impeccable** | `impeccable` or `impeccable:impeccable` is in your available skills | `/plugin marketplace add pbakaus/impeccable`, then `/plugin install impeccable@impeccable` |
| **taste-skill** | `design-taste-frontend` (or `taste-skill:design-taste-frontend`) is in your available skills | `/plugin marketplace add Leonxlnx/taste-skill`, then `/plugin install taste-skill@taste-skill` |
| **Emil Kowalski's skills** | `emil-design-eng` is in your available skills (others from the set: `animate`, `review-animations`, `break-ui`) | `npx skills@latest add emilkowalski/skills` |
| **Playwright** | a `playwright-cli` skill, `playwright-cli` on the PATH (`command -v playwright-cli`), or Playwright MCP tools | `npm install -g @playwright/cli@latest && playwright-cli install --skills` |

Never install one unasked. If none are installed, carry on with `frontend-design` or this skill's own defaults, and list the missing ones in the step 5 report with their install line.

## Who does what

| Moment | impeccable | taste-skill | Emil's skills | Playwright |
|--------|-----------|-------------|---------------|------------|
| Before the direction | `docs/PRODUCT.md` (below) | | | |
| Direction (quick or crafted) | leads, for app UI | leads, for a marketing or company site | | |
| Generic-defaults check | its absolute bans | its anti-slop rules, site surfaces only | | |
| Tokens | | | motion and shadow values | |
| Drawn directions, components | craft floor before writing | site sections only | states, press and hover, transitions | |
| Visual check | `audit` | | `review-animations` when there's motion | screenshots |
| `CLAUDE.md` | a line | a line, if the project has a site | a line | a line |

### impeccable

- **PRODUCT.md first.** Before the direction, write `docs/PRODUCT.md` in impeccable's product schema (its `reference/init.md`, "Write PRODUCT.md": copy the `impeccable:product-schema` comment and only the sections the design answered). Fill it from the step 1 design: users, purpose, positioning, constraints, brand commitments, evidence on hand. impeccable finds files in `docs/`, so it won't interview the user again. Add it to the confirmed list.
- **The direction.** Invoke `impeccable` for the direction of the product's main screen, with its mode from the surface (an app screen is Operate; a landing page is Persuade). Ask it for the visual world only, and tell it this skill writes `docs/DESIGN.md` and `design/tokens.json`: no root `DESIGN.md`, `.impeccable/` config, or code. Its answer becomes the quick direction, or the starting point of the three crafted directions.
- **Crafted depth:** the research and the user's reaction come first, as `design-research.md` says. Then use impeccable to build each of the three directions from the references the user picked, one world per direction; they must still differ as that file requires.
- **Before writing UI** (the drawn directions page, the base components, the signature components): read its `reference/craft-floor.md` once, right before the first of these, and follow it.
- **After step 4 builds:** run its `audit` on the design-system page or the base components. Fix the P0 and P1 findings; list the rest in the report.

### taste-skill

It is built for marketing and company websites: one section per screen, real photographs, a hero entrance, and a browser gate. **Use it only when the project has such a site** (a landing page, a company or shop site), and only for that surface. For app screens, dashboards and forms its rules don't fit: use impeccable or `frontend-design` instead.
- **For the site:** take its kind-of-business decision and its house rules into the direction, and its anti-slop rules into the generic-defaults check.
- **One design system for both.** The app and the site share `design/tokens.json`; there are no separate directions or tokens for the site. In the crafted depth, the drawn page shows each direction twice: the app screen, then the site's first screen (hero only) following taste-skill's rules, so the user judges the direction on both.
- **The pages themselves** are product code. They come after the plan, not in the kickstart.

### Emil Kowalski's skills

- **Tokens:** set `motion` (durations and easing curves) and `shadow` with `emil-design-eng`'s rules: ease-out for entering, no ease-in for UI, short durations, reduced motion respected, and semi-transparent shadows over solid borders where it says so.
- **Components:** build the interaction states of the base and signature components with `emil-design-eng`: hover, press, focus and disabled, popover origin, tooltip timing, transitions instead of keyframes for state changes.
- **Review:** when a component animates, run `review-animations` on it before the step 4 checks.
- `animate`, `break-ui` and `prototype` are for screens built after the kickstart; they go in `CLAUDE.md`, not in this run.

### Playwright

A browser check without a browser tool. Use it for the visual self-review in `design-research.md` and for step 4's look at the result:
- the drawn directions page at 1440×900, once;
- after the build: the design-system preview and the app's first screen, at 1440×900 and 390×844, light and dark.

With `playwright-cli`: `playwright-cli open <url>`, `playwright-cli resize 1440 900`, `playwright-cli screenshot`; then `playwright-cli resize 390 844` and `screenshot` again; for dark, `playwright-cli set-color-scheme dark` and repeat, then `clear-color-scheme`; `playwright-cli close` at the end. It blocks `file://` URLs: serve a local page with `python3 -m http.server <port> --bind 127.0.0.1` from its folder (in the background, stopped afterwards), or use the dev server. Run `playwright-cli` from a temporary directory, because it saves screenshots in `.playwright-cli/` under the current one. Read the screenshots, fix what reads as template or breaks at the narrow width, and look again once. With a browser tool available (Claude in Chrome, the built-in browser), it does this instead, and Playwright isn't needed.

## The CLAUDE.md lines

In the UI block, one line per installed skill, real paths, nothing for skills that aren't installed:

```markdown
- Product context lives in [docs/PRODUCT.md](docs/PRODUCT.md); new screens and redesigns go through the impeccable skill (`/impeccable`), and `/impeccable polish` and `/impeccable audit` run before a UI change is done.
- Marketing pages (landing, company site) are built with the taste-skill skill.
- Interactions and motion follow the emil-design-eng skill; new animations go through `animate`, and `break-ui` stress-tests a screen with worst-case data.
- Check UI changes in a real browser with `playwright-cli` at desktop and mobile widths before saying they are done.
```

## Conflicts

- **One DESIGN.md.** impeccable and taste-skill each have their own design doc. In a kickstarted project the design is `docs/DESIGN.md` plus `design/tokens.json`; if either skill offers to create another, decline it and point at these.
- **Generic defaults: every list applies.** Check the direction against all the lists that are installed (frontend-design's defaults, impeccable's bans, taste-skill's rules on a site) and this skill's own Avoid seed list. A match on any of them is a match.
- **The brief wins.** When a design skill's taste disagrees with what the user said about the look, the user's words win, as all three skills themselves say.
- **No double work.** Each check runs once: if impeccable's `audit` already covered contrast, still run `build_tokens.py contrast`, which is the source of truth for the token pairs, but don't redo the audit by hand.
