# Stack: .NET

Defaults only. The solution file, test projects and `global.json` win.

## Commands

| Purpose | Default |
|---------|---------|
| Install | `dotnet restore` |
| Build | `dotnet build` |
| Test | `dotnet test` |
| Single test | `dotnet test --filter "FullyQualifiedName~<TestName>"` |
| Lint / format check | `dotnet format --verify-no-changes` |
| Format | `dotnet format` |
| Run | `dotnet run --project <path/to/Project.csproj>` |

Pass the solution file when there is more than one project at the root.

## Conventions

- `src/` for projects, `tests/` for test projects named `<Project>.Tests`.
- `<Nullable>enable</Nullable>` and `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>` in a shared `Directory.Build.props`.
- PascalCase for types, methods and properties; `_camelCase` for private fields; `I` prefix for interfaces.
- Async methods end in `Async` and take a `CancellationToken` when they do I/O.
- Style rules live in `.editorconfig`; `dotnet format` enforces them.

## Don'ts

- Don't commit `bin/`, `obj/` or user-specific files (`*.user`).
- Don't put secrets in `appsettings.json`; use user secrets or environment variables.

## Permissions

Allow `dotnet restore/build/test/format`. Not `dotnet run` (long-running) or `dotnet nuget push`.
