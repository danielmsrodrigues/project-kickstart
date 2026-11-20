# Stack: Python

Defaults only. Tools named in `pyproject.toml` and the lockfile win.

## Commands

| Purpose | Default (uv) | Without uv |
|---------|--------------|------------|
| Install | `uv sync` | `python -m venv .venv && pip install -e ".[dev]"` |
| Test | `uv run pytest` | `pytest` |
| Single test | `uv run pytest <path>::<test_name>` | `pytest <path>::<test_name>` |
| Lint | `uv run ruff check .` | `ruff check .` |
| Format | `uv run ruff format .` | `ruff format .` |
| Type-check | `uv run mypy <package>` | `mypy <package>` |
| Run | `uv run <entry-point>` or `uv run python -m <package>` | `python -m <package>` |

Poetry: `poetry install`, `poetry run pytest`, and so on.

## Conventions

- `src/<package>/` layout, tests in `tests/` mirroring the package.
- Type hints on public functions; config for every tool in `pyproject.toml`.
- Modules and functions in snake_case, classes in PascalCase, constants in UPPER_SNAKE_CASE.
- One virtual environment per project in `.venv/`, never committed.

## Don'ts

- Don't install packages into the global interpreter.
- Don't add a `requirements.txt` next to `pyproject.toml` unless a deploy target needs it.

## Permissions

Allow the exact runner prefix used in `CLAUDE.md` (`uv run`, `poetry run`, or none). No `pip install`.
