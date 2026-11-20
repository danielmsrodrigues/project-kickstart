# Stack: Rust

Defaults only. Workspace layout, `Makefile`/`justfile` and CI win.

## Commands

| Purpose | Default |
|---------|---------|
| Install | `cargo fetch` |
| Build | `cargo build` |
| Test | `cargo test` |
| Single test | `cargo test <test_name>` |
| Lint | `cargo clippy --all-targets -- -D warnings` |
| Format check | `cargo fmt --check` |
| Run | `cargo run` (workspace: `cargo run -p <crate>`) |

## Conventions

- `rustfmt` and `clippy` are the style; fix warnings rather than allowing them, and justify any `#[allow(...)]`.
- Errors as `Result`; `thiserror` for library errors, `anyhow` for binaries, if the project uses them.
- No `unwrap()`/`expect()` outside tests and `main` setup without a comment saying why it cannot fail.
- Unit tests in a `#[cfg(test)] mod tests` in the same file; integration tests in `tests/`.
- Crates and modules in snake_case, types in UpperCamelCase.

## Don'ts

- Don't add `unsafe` without a `// SAFETY:` comment.
- Don't commit `target/`.

## Permissions

Allow `cargo build/test/check/clippy/fmt`. Not `cargo publish` or `cargo install`.
