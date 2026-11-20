<!-- Not an output file. Read only the platform you are building for. Paths are defaults; an existing project's layout wins. Commands run from the repo root. -->

## React Native / Expo

Detect: `react-native` or `expo` in `package.json`.

| What | Default |
|------|---------|
| Build tokens | `python3 design/build_tokens.py build design/tokens.json --ts src/theme/theme.ts` |
| API | `lightTheme`, `darkTheme` and type `Theme`; pick with `useColorScheme()` inside a theme context |
| Fonts | `expo-font` (`useFonts`) or the native asset setup, with the `font.family` names |
| Components | `src/components/ui/`, `StyleSheet` reading the theme from the context |
| Check | `python3 design/build_tokens.py check src` |

### Lint rule for hardcoded values

Add it to the linter the project already has, as a **warning**, exempting token and generated files. With no linter for these files, put `python3 design/build_tokens.py check <dirs>` in the lint step instead of installing one. Never install a linter without the user's yes.

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
