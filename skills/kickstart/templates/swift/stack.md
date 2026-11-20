# Stack: Swift

Defaults only. `Package.swift` or the Xcode project and its schemes win.

## Commands

| Purpose | SwiftPM | Xcode project |
|---------|---------|---------------|
| Resolve | `swift package resolve` | `xcodebuild -resolvePackageDependencies` |
| Build | `swift build` | `xcodebuild -scheme <Scheme> build` |
| Test | `swift test` | `xcodebuild -scheme <Scheme> -destination '<destination>' test` |
| Single test | `swift test --filter <TestCase>/<testName>` | add `-only-testing:<Target>/<TestCase>/<testName>` |
| Lint | `swiftlint lint` (if configured) | same |
| Format check | `swiftformat --lint .` (if configured) | same |
| Run | `swift run <executable>` | run from Xcode |

Find schemes with `xcodebuild -list`. Pick the destination from the project's CI or ask once.

## Conventions

- Types in UpperCamelCase, everything else in lowerCamelCase; one primary type per file, file named after it.
- Prefer value types and `let`; mark classes `final` unless designed for subclassing.
- Swift concurrency (`async`/`await`, actors) for new async code.
- Tests in `Tests/<Target>Tests/` (SwiftPM) or the project's test target.

## Don'ts

- Don't commit `xcuserdata/`, `DerivedData/` or `.build/`.
- Don't edit `*.pbxproj` by hand when Xcode or the package manifest can make the change.

## Permissions

Allow build and test only. Add the `xcodebuild` build/test lines from `CLAUDE.md` with the real scheme.
