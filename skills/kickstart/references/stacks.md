# Detecting the stack

## Markers

Look at the repo root first, then one level down (monorepos, `src/`).

| Marker | Template |
|--------|----------|
| `package.json` with `typescript` in dependencies, or `tsconfig.json` | `node-typescript` |
| `package.json` without TypeScript | `node-typescript`, adapted: drop the type-check command and TS ignore rules |
| `pyproject.toml`, `requirements.txt`, `setup.py`, `Pipfile` | `python` |
| `*.sln`, `*.slnx`, `*.csproj`, `*.fsproj`, `global.json` | `dotnet` |
| `Package.swift`, `*.xcodeproj`, `*.xcworkspace` | `swift` |
| `go.mod` | `go` |
| `Cargo.toml` | `rust` |
| Anything else (`pom.xml`, `build.gradle*`, `Gemfile`, `composer.json`, `mix.exs`, `pubspec.yaml`, ...) | `_base`, adapted (see below) |
| No marker | Ask, unless the design settled the stack |

Several markers (for example a Go API plus a TypeScript web app): treat it as a multi-stack repo. Merge the matching templates, put one Commands block per part in `CLAUDE.md`, and name each part's directory.

## Reading the real commands

Template commands are defaults. Replace them with what the repo actually uses:

- **Node:** `package.json` `scripts`; the lockfile picks the package manager (`package-lock.json` npm, `pnpm-lock.yaml` pnpm, `yarn.lock` yarn, `bun.lock`/`bun.lockb` bun).
- **Python:** `uv.lock` means uv, `poetry.lock` Poetry, `Pipfile.lock` Pipenv; `[tool.*]` tables in `pyproject.toml` name the test runner, linter and formatter.
- **.NET:** the solution file name; test projects (`*.Tests.csproj`); `global.json` for the SDK version.
- **Swift:** `Package.swift` means SwiftPM; an Xcode project needs the scheme (`xcodebuild -list`).
- **Go / Rust:** `Makefile` or `justfile` targets, if present, beat the raw tool commands.
- **Any stack:** CI workflow files (`.github/workflows/*`, `.gitlab-ci.yml`) show the commands the project already trusts.

Each template folder has a `stack.md` with the default commands, conventions and permission entries. Read only the one you need.

## Stack without a template

1. Start from `templates/_base/`.
2. Take commands only from the repo (manifest, Makefile, CI). If there are none, write the stack's standard commands and say in the step 3 message that they are unverified.
3. Add the stack's usual build output and dependency folders to `.gitignore`.
4. Allow-list only the build, test and lint commands you wrote in `CLAUDE.md`.
5. After the kickstart, mention that a template for this stack can be contributed (see the repo's CONTRIBUTING.md).
