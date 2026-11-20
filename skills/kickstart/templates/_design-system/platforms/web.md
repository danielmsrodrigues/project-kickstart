<!-- Not an output file. Read only the platform you are building for. Paths are defaults; an existing project's layout wins. Commands run from the repo root. -->

## Web (React, Vue, Svelte, Astro, plain HTML)

Detect: `react`, `vue`, `svelte`, `astro`, `next`, `nuxt`, `@angular/core` or `solid-js` in `package.json`, or an `index.html`.

| What | Default |
|------|---------|
| Build tokens | `python3 design/build_tokens.py build design/tokens.json --css src/styles/tokens.css` |
| With Tailwind v4 | add `--tailwind v4` |
| With Tailwind v3 | add `--tailwind v3 --tailwind-out tailwind.tokens.cjs`, then spread it into `theme.extend` (or `theme`, to drop the defaults) in `tailwind.config` |
| Wire it up | Import the tokens file once in the app's CSS entry (`src/index.css`, `app/globals.css`, ...). With Tailwind v4 the import goes right after `@import "tailwindcss";`. |
| Fonts | Load every family named in `font.family` (self-hosted `@font-face` in the CSS entry, or the framework's font loader). A token naming a font that is never loaded silently falls back. |
| Components | `src/components/ui/`, styled with the project's approach (Tailwind utilities, CSS modules) reading the tokens |
| Check | `python3 design/build_tokens.py check src` |

**Tailwind v4 notes** (what the generator does, and what it can't):
- Semantic tokens become utilities: `bg-action-primary`, `text-ink-muted`, `border-edge-default`, `p-4x`, `rounded-control`, `shadow-raised`, `text-md` (with its paired line height), `font-display`, `font-strong`.
- Tailwind's default color palette is cleared (`--color-*: initial`), so `bg-red-500` produces nothing. Its spacing, sizing and other defaults stay, because layout utilities (`w-full`, `grid-cols-2`) need them.
- `color.palette.*` primitives get no utilities; use the semantic tokens.
- Spacing names that match Tailwind's container sizes (`xs`, `sm`, `md`, ...) are refused, because `max-w-md` would pick them up. Use step names (`1x`, `2x`, `4x`).
- No duration namespace exists: use `duration-(--motion-fast)`.
- `size.*` tokens have no namespace either: use `min-h-(--size-touch-target)`, `max-w-(--size-content-max)`.
- Tailwind inlines shadow values into its utilities, so a dark-mode shadow value does not apply through `shadow-*`. If shadows must change per theme, apply `box-shadow: var(--shadow-raised)` in component CSS.

### Lint rule for hardcoded values

Add it to the linter the project already has, as a **warning**, exempting token and generated files. With no linter for these files, put `python3 design/build_tokens.py check <dirs>` in the lint step instead of installing one. Never install a linter without the user's yes.

With create-vite's default Oxlint (React templates without `--eslint`), use the `check` command: the ESLint selectors below don't apply.

**ESLint (flat config): JS/TS/JSX, inline styles, React Native style objects, Tailwind arbitrary values**

```js
// eslint.config.js: add this object to the exported array (inside defineConfig([...]) in
// create-vite and create-next-app configs). Tested with ESLint 9 and 10.
// If the project already sets no-restricted-syntax for these files, merge the selectors
// into that rule: a second entry for the same rule replaces the first.
const HEX = "#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})";
const TOKEN_MSG = "Hardcoded value. Use a design token (design/tokens.json)."; // name the real token source if it is not design/tokens.json
export const designTokenRules = {
  files: ["src/**/*.{js,jsx,ts,tsx}"],
  ignores: ["src/theme/**"],
  rules: {
    "no-restricted-syntax": ["warn",
      { selector: `Literal[value=/^${HEX}$/]`, message: TOKEN_MSG },
      { selector: `TemplateElement[value.raw=/^${HEX}$/]`, message: TOKEN_MSG },
      { selector: "Literal[value=/(^|\\s)[\\w:-]+-\\[(#|-?\\d)/]", message: TOKEN_MSG },
      { selector: "Literal[value=/^(rgb|hsl)a?\\(/]", message: TOKEN_MSG },
    ],
  },
};
```

**Stylelint: CSS, SCSS, `.razor.css`** (only if Stylelint is already set up, or the user approves adding it)

```json
{
  "rules": {
    "color-no-hex": [true, { "severity": "warning" }],
    "color-named": ["never", { "severity": "warning" }],
    "function-disallowed-list": [["rgb", "rgba", "hsl", "hsla"], { "severity": "warning" }]
  },
  "overrides": [
    { "files": ["**/tokens*.css"], "rules": { "color-no-hex": null, "color-named": null, "function-disallowed-list": null } }
  ]
}
```
