# Design system step (3b)

Read this when the project has a UI. CLIs, APIs and libraries skip it. For a new export into an existing system, use the `kickstart-design` skill instead.

**Principle:** the design system lives in the repo as code: `design/tokens.json` (single source) → generated native token files → a few base components → `docs/DESIGN.md` and a component inventory. Design tools are import sources only.

**Timing:** 3b asks, settles the token values and the files, and gets a yes. Step 4 writes and builds.

Files (`<skill>` is this skill's directory): `templates/_design-system/` holds `tokens.example.json`, `DESIGN.md`, `components-README.md`, `components-spec.md` and `platforms/<web|swiftui|blazor|react-native|other>.md`. Read only the platform file you need.

## Has a UI?

Yes for a web frontend, a mobile or desktop app, or a Blazor/Razor UI. A JSON-only backend, a CLI or a library is no. If unclear, ask once.

## Existing design system

Look first: `tokens.*`, CSS full of `--color-*` variables, a Tailwind theme, a Swift `Theme`/`Colors` type, a component-library theme, a `components/ui` folder. If one exists, **document it; don't create a parallel one**. DESIGN.md and the inventory describe the real tokens and components. Add only what's missing (such as the lint rule), with a yes. Moving its tokens into `design/tokens.json` is a separate change: offer `/kickstart-design`, which adopts it without changing how anything looks. Then skip to Docs.

## 1. Origin

One question, three choices, as buttons when you have the question tool. Ask it even when the user said to go ahead without them, unless a source is already in the repo or the conversation.

- **a) Claude Design export or handoff**, or **b) another source** (a tokens file, Figma variables, a reference site or app): read `<skill>/../kickstart-design/references/design-import.md`.
- **c) None.** Ask two or three questions, one per message, skipping what the design step answered: the tone (three words, and who uses it), references they like and why, what to avoid. Then:
  - if `frontend-design` is available, invoke it and take its direction;
  - otherwise propose one yourself: a one-sentence direction, a 4-6 color palette, one or two type families with a scale, a spacing scale.

  Show it and get a yes.

## 2. Tokens

Settle the values for `design/tokens.json` (W3C DTCG) with the structure of `tokens.example.json`. Its values are placeholders, never output.

- **Groups:** `color.palette` (primitives); semantic `color.ink`, `color.surface`, `color.action`, `color.edge`; `spacing`, `radius`, `size`; `font` (`family`, `size` with `$extensions.lineHeight`, `weight`); `shadow` (DTCG object); `motion`.
- **Roles every base component needs:**
  - `action.primary`, plus `action.primary-active` for hover on pointer platforms and pressed on touch
  - `action.danger` and `action.focus`
  - `ink.on-action`, `ink.on-danger` and `ink.danger`
  - `size.touch-target`, `size.border` and `size.focus-ring`

  Derive them from the palette, and check text-on-fill contrast in both modes.
- **Aliases:** semantic tokens alias primitives, and dark values (`$extensions.modes.dark`) are aliases too.
- **Names:** spacing as steps (`1x`, `2x`, `4x`), roles by meaning (`action.primary`, not `blue`). A font family and a font weight never share a name.

In step 4:
- Write `tokens.json`.
- Get `design/build_tokens.py` from `kickstart_files.py files --ui`. Never read or retype the script; `--help` shows its usage.
- Run the platform's build command and wire the output in as the platform file says. After a scaffold, also replace the demo styles.
- Load the fonts.
- Add a `tokens` script if the project has a task runner.
- Put the build and check commands in `CLAUDE.md` and in the `settings` allow-list.

## 3. Components

The six in `components-spec.md`, in the platform's idiom and location. With a component library, follow "Component libraries" in `platforms/other.md`. For UI code, invoke `frontend-design` when available.

## 4. Docs

- `docs/DESIGN.md` from its template: the one-sentence direction, token roles (names, not values), layout and motion, and a concrete "Avoid" list.
- The inventory, `<components dir>/README.md`, from `components-README.md`; use `components/README.md` when the platform has no folder of its own.
- The UI block in `CLAUDE.md` (in `_base/CLAUDE.md`), with real paths.

## 5. Enforcement

Add the lint warning from the platform file to the linter the project has. With no linter, put the `check` command in the lint step. Never install a linter without a yes.

## Files and confirmation

List everything this step adds or changes in the step 3 format, as `create` and `exists`/`edit` lines: the tokens, the generated output, the six components, the inventory, `DESIGN.md`, and the CSS entry, `package.json` and lint config edits. Get a yes before step 4.

## Checks (step 4)

The token build exits 0. `check` exits 0 on the UI source. The platform wiring is in place. Every `font.family` is loaded (on Apple platforms, every weight too). The project builds, and lints and type-checks when the dependencies are installed.
