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

One question, four choices, as buttons when you have the question tool. Ask it even when the user said to go ahead without them, unless a source is already in the repo or the conversation.

- **a) Claude Design export or handoff**, or **b) another source** (a tokens file, Figma variables, a reference site or app): read `<skill>/../kickstart-design/references/design-import.md`.
- **d) An existing brand** (a known company, the client's own identity): the look is the brand's, not ours to invent.
  - **Who it's for.** Confirm, in one line, that the project is for the brand or with its permission (client, agency, in-house). If it isn't, say that using a real brand's identity without permission can infringe its trademark, and offer to build in a neutral style instead.
  - **What to ask for:** the brand guidelines, logo files (SVG preferred), official colors, the typefaces and whether the project may use them (license), and any existing app or site to match. Take values exactly from these sources. A value read from a live site is marked as derived.
  - **Never draw or recreate a logo or mark from memory.** Without the files, set the name in plain type and list the logo as missing. A licensed font that isn't provided gets the closest free alternative, named as a stand-in in DESIGN.md.
  - **No visual research and no three directions.** The identity is given. The crafted depth here means only researching interface patterns for the job (`design-research.md`, layer 1) and the signature components.
- **c) None.** Ask two or three questions, one per message, skipping what the design step answered: the tone (three words, and who uses it), references they like and why, what to avoid.

  Then ask the **depth**, once, as buttons. Recommend **Crafted** for a product with screens people will judge by its look:
  - **Crafted**: research references (Dribbble, Behance, Mobbin, modern sites, the product's physical world), draw three directions on a real screen of the app, and design the product's signature components. About twice the cost of this step. Follow `design-research.md`, then continue at the contrast check below.
  - **Quick**: one direction, proposed in text, as follows.
  - if impeccable is installed (or taste-skill, for a marketing or company site), take the direction as `design-skills.md` says;
  - otherwise, if `frontend-design` is available, invoke it and take its direction;
  - otherwise propose one yourself: a one-sentence direction, a 4-6 color palette, one or two type families with a scale, a spacing scale.

  **Check the direction against generic defaults before showing it**, including any direction already written in a spec or the conversation: those are input, not decided. With `frontend-design`, use its list of defaults; with impeccable, its absolute bans in `craft-floor.md`; with taste-skill, on a site, its anti-slop rules. Without it, use the seed list in the "Avoid" section of `templates/_design-system/DESIGN.md`. Common examples are cream with terracotta and a serif display, black with one neon accent, and identical rounded cards with soft grey shadows. If the direction matches one and the user didn't ask for it by name, revise it and say what you changed and why.

  **Then compute contrast; never estimate it.** List every pair the design will actually use: each text color on each background, the text on every filled button, badge and status color (such as a "ready" pill), and borders and focus rings on the backgrounds, in light and dark. Run `python3 <skill>/scripts/build_tokens.py contrast --pairs "FG:BG" ...` (add `:3` for borders and focus rings). Fix every FAIL before showing anything; the user is not expected to catch contrast problems. Show the ratios from the script output, not your own. Then show the direction and get a yes.

## 2. Tokens

Settle the values for `design/tokens.json` (W3C DTCG) with the structure of `tokens.example.json`. Its values are placeholders, never output.

- **Groups:** `color.palette` (primitives); semantic `color.ink`, `color.surface`, `color.action`, `color.edge`; `spacing`, `radius`, `size`; `font` (`family`, `size` with `$extensions.lineHeight`, `weight`); `shadow` (DTCG object); `motion`.
- **Roles every base component needs:**
  - `action.primary`, plus `action.primary-active` for hover on pointer platforms and pressed on touch
  - `action.danger` and `action.focus`
  - `ink.on-action`, `ink.on-danger` and `ink.danger`
  - `size.touch-target`, `size.border` and `size.focus-ring`

  Derive them from the palette.
- **Aliases:** semantic tokens alias primitives, and dark values (`$extensions.modes.dark`) are aliases too.
- **Contrast is declared, then checked by the script.** Every `color.action.*` and `color.status.*` fill gets `"$extensions": {"textOn": "{color.ink.<ink>}"}`, naming the ink used on it. Text that is itself colored (a red error message) is an `ink.*` token, not a status color. Divider-only edges get `"decorative": true`; the rest must reach 3:1. `python3 design/build_tokens.py contrast design/tokens.json` must pass before you show the token set and again after writing it.
- **Motion and shadow:** with Emil Kowalski's skills installed, set them by `emil-design-eng`'s rules (`design-skills.md`).
- **Names:** spacing as steps (`1x`, `2x`, `4x`), roles by meaning (`action.primary`, not `blue`). A font family and a font weight never share a name.

In step 4:
- Write `tokens.json`.
- Get `design/build_tokens.py` from `kickstart_files.py files --ui`. Never read or retype the script; `--help` shows its usage.
- Run the platform's build command and wire the output in as the platform file says. After a scaffold, also replace the demo styles.
- Load the fonts.
- Add a `tokens` script if the project has a task runner.
- Put the build and check commands in `CLAUDE.md` and in the `settings` allow-list.

## 3. Components

The six in `components-spec.md`, in the platform's idiom and location, shown in every variant by the published design system (`references/preview.md`). With a component library, follow "Component libraries" in `platforms/other.md`. For UI code, follow `design-skills.md` (impeccable's craft floor, Emil Kowalski's interaction rules); otherwise invoke `frontend-design` when available.

## 4. Docs

- `docs/DESIGN.md` from its template: the one-sentence direction, token roles (names, not values), layout and motion, and a concrete "Avoid" list.
- The inventory, `<components dir>/README.md`, from `components-README.md`; use `components/README.md` when the platform has no folder of its own.
- `docs/PRODUCT.md` when impeccable is installed (`design-skills.md`).
- The UI block in `CLAUDE.md` (in `_base/CLAUDE.md`), with real paths and the design-skill lines from `design-skills.md`.

## 5. Enforcement

Add the lint warning from the platform file to the linter the project has. With no linter, put the `check` command in the lint step. Never install a linter without a yes.

## Files and confirmation

List everything this step adds or changes in the step 3 format, as `create` and `exists`/`edit` lines: the tokens, the generated output, the six components, the inventory, `design/system/` (the components build for the published design system, web only), `DESIGN.md`, and the CSS entry, `package.json` and lint config edits. Get a yes before step 4.

## Checks (step 4)

The token build exits 0. `contrast design/tokens.json` exits 0. The preview page is generated (and published when possible), as `references/preview.md` says. `check` exits 0 on the UI source. The platform wiring is in place. Every `font.family` is loaded (on Apple platforms, every weight too). The project builds, and lints and type-checks when the dependencies are installed.
