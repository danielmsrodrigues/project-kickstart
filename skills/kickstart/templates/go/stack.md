# Stack: Go

Defaults only. `Makefile`/`justfile` targets and CI win.

## Commands

| Purpose | Default |
|---------|---------|
| Install | `go mod download` |
| Build | `go build ./...` |
| Test | `go test ./...` |
| Single test | `go test ./<pkg> -run '^TestName$'` |
| Lint | `go vet ./...` (plus `golangci-lint run` if configured) |
| Format check | `gofmt -l .` |
| Run | `go run ./cmd/<name>` |

## Scaffold (empty repo)

`go mod init <module path>` (e.g. `github.com/<owner>/<repo>`; ask for it if unknown), then `cmd/<name>/main.go` by hand. It does not run git. (Not exercised by this skill's tests: Go was unavailable on the test machine.)


## Conventions

- `cmd/<name>/` for binaries, `internal/` for code not meant for import, `pkg/` only for real public libraries.
- `gofmt` is the style; no other formatting rules.
- Errors are returned, wrapped with `fmt.Errorf("...: %w", err)`; no panics in library code.
- Table-driven tests in `*_test.go` next to the code.
- Short package names, lowercase, no underscores.

## Don'ts

- Don't commit built binaries.
- Don't add a dependency for what the standard library already does.

## Permissions

Allow `go build/test/vet`, `gofmt -l` and `go mod tidy`.
