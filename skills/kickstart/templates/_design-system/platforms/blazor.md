<!-- Not an output file. Read only the platform you are building for. Paths are defaults; an existing project's layout wins. Commands run from the repo root. -->

## .NET Blazor

Detect: `Microsoft.NET.Sdk.Razor`, `Microsoft.AspNetCore.Components`, or `*.razor` files.

| What | Default |
|------|---------|
| Build tokens | `python3 design/build_tokens.py build design/tokens.json --css wwwroot/css/tokens.css` |
| Wire it up | `<link rel="stylesheet" href="css/tokens.css" />` once in the host page (`App.razor` / `index.html` / `_Host.cshtml`), before other stylesheets |
| Fonts | `@font-face` in `wwwroot/css/` |
| Components | `Components/UI/` (`.razor` + `.razor.css` scoped styles reading `var(--…)`) |
| Check | `python3 design/build_tokens.py check Components Pages wwwroot/css --allow "*tokens.css"` |

### Lint rule for hardcoded values

Add it to the linter the project already has, as a **warning**, exempting token and generated files. With no linter for these files, put `python3 design/build_tokens.py check <dirs>` in the lint step instead of installing one. Never install a linter without the user's yes.

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
