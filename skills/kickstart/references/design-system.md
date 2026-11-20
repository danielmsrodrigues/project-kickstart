# Design system step

Read this when the project has a UI (step 3b), or when the user brings a new design export to an existing project (sync mode). CLIs, APIs, libraries and other projects without a UI skip this file.

**Principle:** the design system lives in the repo, as code: `design/tokens.json` (single source) → generated native token files → a few base components → `docs/DESIGN.md` and a component inventory. Design tools (Claude Design, Figma, a reference site) are import sources, not where the system lives.

**Timing:** step 3b decides. It runs the questions, settles the token values and the file list, and gets a yes. Step 4 writes and builds everything. The one exception is reading or unpacking an import source to look at it, which happens in 3b.

## Contents

- Has a UI?
- Existing design system
- 1. Origin
- Converting Figma variables
- 2. Tokens
- 3. Components
- 4. Docs
- 5. Enforcement
- Files and confirmation
- Checks after writing (step 4)
- Sync mode

Templates and helpers: `templates/_design-system/` (`tokens.example.json`, `DESIGN.md`, `components-README.md`, `components-spec.md`, `platforms.md`) and `scripts/build_tokens.py`.

## Has a UI?

Yes when the design or the repo shows a web frontend, a mobile or desktop app, or a Blazor/Razor UI; `platforms.md` lists the detection markers. A backend that serves only JSON, a CLI or a library is no. If it's unclear, ask once: the answer decides whether this step runs.

## Existing design system

Look before asking about origin. Signs of one: `design/tokens.json` or other `tokens.*`, CSS full of `--color-*`-style variables, a Tailwind theme, a `Theme`/`Colors` type in Swift, a component-library theme (MUI, MudBlazor, ...), a `components/ui` folder.

If one exists, **document it; don't create a parallel one**:
- `docs/DESIGN.md` describes the real tokens and points at their real source file.
- The inventory lists the real components.
- Add only what is missing (for example the lint rule), and only with the user's yes.
- Moving its tokens into `design/tokens.json` is a separate change: offer it, don't do it.

Then skip to 4.

## 1. Origin

Ask once, as one question with these three choices. If the user said to go ahead without them, still ask unless a source is already in the repo or the conversation: this answer decides every value.

**a) Claude Design export or handoff.** What the official docs state (Claude Design help center and launch post):
- The Export menu offers a `.zip` download, PDF, PPTX, Google Slides, standalone HTML, and sends to other tools.
- "Handoff to Claude Code" sends the design to a local coding agent or to Claude Code on the web, packaged as a handoff bundle.
- In Claude Code, `/design` imports a design into the codebase, and `/design-sync` brings a code design system into Claude Design.

The docs do not specify the bundle's file layout or any token export format. So:
- Inspect what arrived; don't assume a structure. List its files.
- Use structured tokens if present (a `tokens.json`, `tokens.css`, CSS custom properties, a theme file). Otherwise extract values from the HTML/CSS: colors, font families, the size scale, spacing steps, radii, shadows.
- Group raw values into roles and name them semantically. Merge near-duplicates and say which you merged.
- Note which components the design uses; they inform step 3.
- Afterwards, suggest running `/design-sync` in Claude Code so Claude Design builds from the repo's system from now on.

**b) Another source:**
- A tokens file (W3C DTCG, Style Dictionary, Tokens Studio).
- Figma variables exported as JSON (REST API or a plugin; the shape varies, so inspect it). See "Converting Figma variables" below.
- A reference site or app. For a site, read its CSS or computed styles if you have a browser tool; for an app, work from screenshots the user provides.

Values from a reference are a starting point; mark them as derived in DESIGN.md.

**c) None: start from scratch.** Ask two or three questions, one per message, skipping what the design step already answered:
1. Tone: three words for how it should feel, and who uses it.
2. References: a product, site or object whose look they like, and what about it.
3. What to avoid: looks they dislike or that competitors use.

Then turn the answers into a direction (palette, type, layout, principles):
- If the `frontend-design` skill is available, invoke it and use its output.
- Without it, propose the direction yourself: a one-sentence direction, a 4-6 color palette, one or two type families with a scale, and a spacing scale.

Either way, derive the full role set in step 2 from it, show it, and get a yes.

### Converting Figma variables

Figma exports differ (REST `GET /v1/files/:key/variables/local`, which needs an Enterprise plan, or one of several plugins). Read the file before converting, and apply these rules:

- **Collections → groups by role, not by name.** A primitives collection (raw colors, a numeric scale) goes to `color.palette.*` and the scales; a semantic collection (aliases with light/dark modes) goes to `color.ink/surface/action/edge`. Never keep collection names like `Primitives` or `Semantic` as top-level groups: unknown groups land in `Theme.Other` with no error.
- **Colors:** RGBA floats (0-1) → hex, with alpha as 8-digit hex (`#1a1d2414`), or a DTCG color object.
- **Aliases:** resolve `VARIABLE_ALIAS` ids to the dotted path of the target token (`{color.palette.amber-500}`).
- **Modes:** the light (or first) mode is `$value`; the dark mode goes to `$extensions.modes.dark`. Any other mode (high contrast, brand variants): ask what it maps to.
- **Numbers:** unitless FLOATs for spacing, radius and sizes become `px` dimensions. Rename numeric scale names (`spacing/4`) to step names (`4x`).
- **Line height** in points: convert to a ratio of its font size for `$extensions.lineHeight`, and round.
- **Not in variables:** shadows live in Figma effect styles and motion is usually absent. Read them from the styles if exported; otherwise derive them from the direction and mark them as your call.
- **Library (remote) variables** may be missing from the file's export; say which aliases could not be resolved.

Keep the converter you write as a scratch tool, not a repo file, unless the user wants syncing from Figma to be repeatable; then add it under `design/` and document the command in `DESIGN.md`.

## 2. Tokens

Settle the values for `design/tokens.json` (W3C DTCG), following the structure of `tokens.example.json`. Its values are placeholders, never output.

- **Groups:**
  - `color.palette` (primitives)
  - semantic `color.ink`, `color.surface`, `color.action`, `color.edge`
  - `spacing`, `radius`, `size`
  - `font` (`family`, `size` with paired `lineHeight`, `weight`)
  - `shadow`, `motion`
- **Roles the base components need:** every component state needs a token. That means `action.primary`, `action.primary-active` (hover on pointer platforms, pressed on touch), `action.danger`, `action.focus`, `ink.on-action`, `ink.on-danger`, `ink.danger`, and `size.touch-target`, `size.border`, `size.focus-ring`. A 4-6 color palette is the primitives; the roles are derived from it. Check text-on-fill pairs for contrast in both modes.
- **Semantic tokens alias primitives**, in both modes: dark values in `$extensions.modes.dark` are aliases too.
- **Names:**
  - spacing as steps (`1x`, `2x`, `4x`)
  - roles by meaning (`action.primary`, not `blue`)
  - a font family and a font weight never share a name
- **Shadows** use the DTCG object (`color`, `offsetX`, `offsetY`, `blur`, `spread`).

In step 4: write `design/tokens.json`, copy `scripts/build_tokens.py` to `design/build_tokens.py` (standard-library Python 3.8+), and run the platform's build command from `platforms.md`. Then:
- Wire the output in as the platform's row says (CSS entry, host page, `Package.swift`).
- Load the fonts as the platform's row says.
- Add a `tokens` script/target if the project has a task runner (`package.json` scripts, Makefile, justfile); otherwise the command lives in `CLAUDE.md`.
- Add the build and check commands to `CLAUDE.md` Commands.
- Add both commands to `.claude/settings.json` `allow`, in the `Bash(<command> *)` form only, because they always take arguments.

Generated files carry a "do not edit" header. Edits go to `tokens.json`, then rebuild.

## 3. Components

The base set from `components-spec.md`, written in the platform's idiom and location (`platforms.md`). With a component library, follow "Component libraries" there instead. For the UI code, invoke `frontend-design` when available.

## 4. Docs

- `docs/DESIGN.md` from `templates/_design-system/DESIGN.md`. It holds the direction in one sentence, the tokens explained, layout and motion principles, and an "Avoid" section filled with concrete defaults this product must not fall into.
- `<components dir>/README.md` from `components-README.md`, with one row per component (name, use, variants). It goes in the platform's components folder; `components/README.md` when there is none.
- `CLAUDE.md` gets the UI block from the `_base/CLAUDE.md` template, with the real paths and commands.

## 5. Enforcement

Add the warning rule for hardcoded values from `platforms.md` "Enforcement" to the linter the project already has. With no linter, wire `python3 design/build_tokens.py check <dirs>` into the lint command. Never install a linter without the user's yes.

## Files and confirmation

Show everything this step adds or changes in the step 3 format, then wait for a yes:

```
create   design/tokens.json
create   design/build_tokens.py
create   src/styles/tokens.css                 (generated)
create   src/components/ui/Button.tsx          (and Input, Card, Text, Heading, Stack)
create   src/components/ui/README.md           (inventory)
create   docs/DESIGN.md
exists   src/index.css                         (import tokens and fonts; will show a diff)
exists   package.json                          (add "tokens" script; will show a diff)
exists   eslint.config.js                      (add the warning rule; will show a diff)
         CLAUDE.md, .claude/settings.json      (UI block, commands and allow entries, included in their generation)
```

## Checks after writing (step 4)

Run these in addition to the checks in `generating-files.md`:

1. The token build exits 0.
2. The `check` command exits 0 on the UI source folders.
3. The project's lint and type-check pass, if their dependencies are installed.
4. The platform's wiring from `platforms.md` is in place (with Tailwind: the token file imported after `@import "tailwindcss"`).
5. Every name in `font.family` is loaded or registered somewhere; on Apple platforms also every weight token exists in the family's files.
6. The project builds (`swift build`, `npm run build`, `dotnet build`...).

## Sync mode

Use when the project already has `design/tokens.json` and the user brings a new export (Claude Design, Figma, a tokens file) or asks to "sync the design system".

1. **Candidate.** Convert the new source into a candidate tokens file in a temporary location, using the same extraction and names as the existing file. Keep a token's name when its role is the same. A renamed token counts as a removal plus an addition.
2. **Diff.** Run `python3 design/build_tokens.py diff design/tokens.json <candidate>`. Show added (`+`), removed (`-`) and changed (`~`) tokens, plus tokens that change only through an alias.
3. **Usages.** For every changed or removed token, search the codebase for all the forms it takes:
   - the dotted token name (`action.primary`), as used in `docs/DESIGN.md`
   - the CSS variable (`--color-action-primary`)
   - the code name (`actionPrimary`, `Theme.Colors.actionPrimary`); `diff` prints the CSS and code names for each token
   - with Tailwind, the utility suffix, which is the CSS name without its namespace (`action-primary`, as in `bg-action-primary` and `hover:bg-action-primary`)

   List the affected components from the inventory.
4. **Removed tokens still in use** are blockers. List each usage with `file:line`. On the web nothing fails at build time (Tailwind silently drops the class); in Swift and TypeScript it is a compile error, so building the candidate in a scratch copy is a quick extra check.
5. **Component changes.** List what the export implies (new components, new variants), checked against the inventory: extend before adding.
6. **Wait for the user's yes.** Apply only what they approve: update `design/tokens.json`, rebuild, update components, DESIGN.md and the inventory.
7. **Verify.** Search again for every removed token's forms (step 3) and expect zero hits. Then run `check`, the lint and the build. Offer a commit; don't make one unasked.
