# Copilot Instructions for slogpy

## Build, Test, and Lint

This project uses **Poetry** for dependency management and builds with `poetry-dynamic-versioning` (version derived from git tags).

```bash
# Install dependencies
poetry install

# Run all tests
poetry run pytest

# Run a single test file
poetry run pytest tests/test_slogpy_file_info.py

# Run a single test function
poetry run pytest tests/test_slogpy_file_info.py::test_file_timestamp

# Lint
poetry run ruff check .

# Format
poetry run ruff format .
```

## Architecture

slogpy is a logging library built on top of Python's `logging` module and [Rich](https://github.com/Textualize/rich) for console output. The core design:

- **`Slog` class** (`slogpy/slog.py`) — The entire public API is `@classmethod` methods on a single class. There are no instances; consumers import and use it as a static singleton: `from slogpy.slog import Slog as slog`.
- **Dual output** — Every log call writes to both console (via Rich) and file (via Python `logging.FileHandler`). Console output respects a log level threshold; file output captures everything.
- **Custom log levels** — `MINIMAL=0, DEBUG=1, INFO=5, WARN=9, ERROR=10, FATAL=99`. These are mapped to Python `logging` levels for file output.
- **`Section`** (`slogpy/section.py`) — Context manager that emits styled section start/end markers with elapsed time tracking.
- **`SlogProgress`** (`slogpy/progress.py`) — Wraps `rich.progress.Progress` to share slog's Rich console, preventing display conflicts. Factory functions provide common progress bar configurations.
- **`syslogger.py`** — Placeholder module for syslog integration (not yet incorporated).

## Conventions

- **Slog is never instantiated** — all methods are `@classmethod`. Use the class directly: `from slogpy.slog import Slog`, then call `Slog.info(...)`, `Slog.warn(...)`, etc.
- **Ruff**: All ruff rules in `pyproject.toml` are non-negotiable — always follow them. If a rule is exceptionally painful in a specific case, ask before adding a `noqa` exception.
- **Rich markup in messages**: Log messages can contain Rich style markup (e.g., `[yellow]text[/]`). The `strip_style_markup` utility in `util.py` removes markup before writing to file.
- **Test structure**: Tests use `pytest`. Console-output tests use `capsys`; file-output tests use a `temp_log_file` fixture (from `conftest.py`) that creates a temp directory and initializes slog with a temp file path. Tests follow a Given/When/Then docstring pattern.
- **Versioning**: The published version comes from git tags via `poetry-dynamic-versioning`; `__version__` in `__init__.py` is a placeholder.
