# Platforms: where tokens and components go

Not an output file. Paths are defaults; an existing project's layout wins. `build_tokens.py` is copied to `design/build_tokens.py` in the project; the commands below run from the repo root.

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

## SwiftUI

Detect: `import SwiftUI` in sources, `Package.swift` with an app target, or an `*.xcodeproj`.

`<src>` below is `Sources/<Target>` in a Swift package, or the app folder (`<App>/`) in an Xcode project.

| What | Default |
|------|---------|
| Build tokens | `python3 design/build_tokens.py build design/tokens.json --swift <src>/DesignSystem/Theme+Generated.swift` |
| API | `Theme.Colors`, `Theme.Spacing`, `Theme.Radius`, `Theme.Size`, `Theme.Typography`, `Theme.Shadows`, `Theme.Motion`. Names are camelCase from the token path; spacing step `4x` is `Theme.Spacing.x4`. Primitives (`color.palette.*`) are not generated. |
| Colors | Light and dark are dynamic colors that follow the system appearance (UIKit trait collection / AppKit appearance). Increased-contrast variants are not generated; add them by hand if the design calls for them. |
| Type | Always scale with Dynamic Type: `Font.custom(Theme.Typography.familyBody, size: Theme.Typography.sizeMd, relativeTo: .body)`, with `relativeTo` set per role (body, headline, title...). Put the role mapping in one hand-written `Theme+Typography.swift`. `Theme.Typography.size<Name>LineSpacing` is in points, ready for `.lineSpacing(_:)`. |
| Fonts | Only use a custom family when its files are in the repo or the user provides them (check the licence). Each weight token must exist in the family; otherwise the system synthesizes or falls back. Package: put the files in `<src>/Resources/Fonts/`, add `resources: [.process("Resources/Fonts")]` to the target and register them at launch with `CTFontManagerRegisterFontsForURL`. Xcode app: add them to the target and list them under `UIAppFonts`. A family that is not registered falls back to the system font silently, so a quick check in a preview is part of step 4. |
| Shadows | `.themeShadow(Theme.Shadows.raised)`. SwiftUI takes one shadow layer; the generator uses the first and halves the DTCG blur to get SwiftUI's radius. |
| Motion | `Theme.Motion.*` are `TimeInterval` seconds: `.animation(.easeOut(duration: Theme.Motion.fast), value: ...)`. |
| Components | `<src>/DesignSystem/Components/`, as small views, `ButtonStyle`s and `ViewModifier`s reading `Theme.*` |
| Inventory in a package | SwiftPM warns about non-Swift files in a target. Add `exclude: ["DesignSystem/Components/README.md"]` to the target in `Package.swift`. |
| Check | `python3 design/build_tokens.py check <src>` (fails if the path does not exist) |
| Verify iOS without Xcode builds | `swift build` on a Mac compiles the macOS branch only. Type-check the iOS branch with `xcrun --sdk iphonesimulator swiftc -typecheck -target arm64-apple-ios<version>-simulator <files>`, or build the scheme with `xcodebuild` when the project has one. |

A removed or renamed token is a compile error in Swift, which makes sync safer here than on the web.

## .NET Blazor

Detect: `Microsoft.NET.Sdk.Razor`, `Microsoft.AspNetCore.Components`, or `*.razor` files.

| What | Default |
|------|---------|
| Build tokens | `python3 design/build_tokens.py build design/tokens.json --css wwwroot/css/tokens.css` |
| Wire it up | `<link rel="stylesheet" href="css/tokens.css" />` once in the host page (`App.razor` / `index.html` / `_Host.cshtml`), before other stylesheets |
| Fonts | `@font-face` in `wwwroot/css/` |
| Components | `Components/UI/` (`.razor` + `.razor.css` scoped styles reading `var(--…)`) |
| Check | `python3 design/build_tokens.py check Components Pages wwwroot/css --allow "*tokens.css"` |

## React Native / Expo

Detect: `react-native` or `expo` in `package.json`.

| What | Default |
|------|---------|
| Build tokens | `python3 design/build_tokens.py build design/tokens.json --ts src/theme/theme.ts` |
| API | `lightTheme`, `darkTheme` and type `Theme`; pick with `useColorScheme()` inside a theme context |
| Fonts | `expo-font` (`useFonts`) or the native asset setup, with the `font.family` names |
| Components | `src/components/ui/`, `StyleSheet` reading the theme from the context |
| Check | `python3 design/build_tokens.py check src` |

## Other UI stacks

Flutter, Android Compose, desktop toolkits: use the `--ts` or `--css` output as a reference, write the equivalent theme by hand, and say so in DESIGN.md. Contributing a generator is welcome.

## Component libraries

If the project uses a component library (MUI, Chakra, shadcn/ui, Vuetify, MudBlazor, Fluent UI, Syncfusion, Radzen, ...), its components are the base set: don't wrap every one of them.

- Feed the tokens into the library's own theme API (theme object, CSS variables or theme file), generated from or pointing at the token output. Check the library's docs for the current API; don't fork its CSS.
- Write a base component only where the library has no equivalent.
- The inventory lists the library components the project uses, with the variants allowed.

## Enforcement (lint)

Use the linter the project already has, add the rule as a **warning**, and exempt token and generated files. With create-vite's default Oxlint (React templates without `--eslint`), use the `check` command in the lint step instead: the ESLint selectors below don't apply. If the project has no linter for these files, put the `check` command in the lint step (no dependencies) instead of installing one.

**ESLint (flat config): JS/TS/JSX, inline styles, React Native style objects, Tailwind arbitrary values**

```js
// eslint.config.js: add this object to the exported array (inside defineConfig([...]) in
// create-vite and create-next-app configs). Tested with ESLint 9 and 10.
// If the project already sets no-restricted-syntax for these files, merge the selectors
// into that rule: a second entry for the same rule replaces the first.
const HEX = "#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})";
const TOKEN_MSG = "Hardcoded value. Use a design token (design/tokens.json).";
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

**SwiftLint** (`.swiftlint.yml`; only if SwiftLint is already used, or the user approves adding it)

```yaml
excluded:
  - "**/Theme+Generated.swift"
custom_rules:
  hardcoded_color:
    name: "Hardcoded color"
    regex: 'Color\(\s*(\.sRGB\s*,\s*)?(red|hue|white):|#colorLiteral\(|Color\(\s*"|Color\.(red|orange|yellow|green|mint|teal|cyan|blue|indigo|purple|pink|brown|gray|black|white)\b|"#[0-9a-fA-F]{6}'
    message: "Use Theme.Colors instead of a literal or system color."
    severity: warning
  hardcoded_length:
    name: "Hardcoded length"
    regex: '\.padding\(([^)]*[^\w.])?[1-9][0-9]*\s*\)|\.shadow\([^)]*radius:\s*[1-9]|\bspacing:\s*[1-9]|cornerRadius(:|\()\s*[1-9]|\.frame\([^)]*(width|height|minWidth|minHeight|maxWidth|maxHeight):\s*[1-9]|lineWidth:\s*[1-9]|\.lineSpacing\(\s*[1-9]|\bpadding:\s*[1-9]'
    message: "Use Theme.Spacing, Theme.Radius or Theme.Size instead of a number."
    severity: warning
  hardcoded_font:
    name: "Hardcoded font"
    regex: '\bsize:\s*[1-9]|\.font\(\s*\.(largeTitle|title|title2|title3|headline|subheadline|body|callout|footnote|caption|caption2)\b'
    message: "Use the Theme typography roles instead of a literal size or system text style."
    severity: warning
```

**Any stack:** `python3 design/build_tokens.py check <dirs> [--allow GLOB ...]` reports, outside token files and ignoring comments:
- hex, `rgb()`/`hsl()`, and primitives used directly (`--color-palette-*`)
- Tailwind arbitrary values (`p-[13px]`, `bg-[#…]`) and default palette classes
- px/rem literals on spacing, radius, size and type properties in CSS and style objects
- SwiftUI color literals and system colors, number literals in padding/spacing/frame/corner radius/line width/line spacing, literal font sizes and system text styles

It exits 1 when it finds any, and 2 when a path does not exist.
