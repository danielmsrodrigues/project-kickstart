<!-- Not an output file. Read only the platform you are building for. Paths are defaults; an existing project's layout wins. Commands run from the repo root. -->

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

### Lint rule for hardcoded values

Add it to the linter the project already has, as a **warning**, exempting token and generated files. With no linter for these files, put `python3 design/build_tokens.py check <dirs>` in the lint step instead of installing one. Never install a linter without the user's yes.

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
