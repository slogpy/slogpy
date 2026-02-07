<!--
  Sync Impact Report
  ===================================================================
  Version change: 1.0.0 → 1.1.0 (MINOR — material constraint changes)
  Modified principles:
    - I. Static Singleton API: import example updated to idiomatic
      Pascal case (Slog as slog → Slog directly)
  Modified sections:
    - Technology & Tooling Constraints:
      - Python ≥ 3.8 → ≥ 3.10
      - Rich ^13.7.0 → >=12,<15
  Added sections: N/A
  Removed sections: N/A
  Templates requiring updates:
    - .specify/templates/plan-template.md         ✅ compatible
    - .specify/templates/spec-template.md          ✅ compatible
    - .specify/templates/tasks-template.md         ✅ compatible
    - .specify/templates/checklist-template.md     ✅ compatible
    - .specify/templates/agent-file-template.md    ✅ compatible
  Follow-up TODOs:
    - Update pyproject.toml python & rich constraints
    - Update source, tests, README, copilot-instructions.md
      to use Pascal case Slog (remove `as slog` alias)
    - Remove noqa: N813 comments that suppressed the alias warning
  ===================================================================
-->

# slogpy Constitution

## Core Principles

### I. Static Singleton API

The `Slog` class MUST never be instantiated. All public methods MUST
be `@classmethod` on the single `Slog` class. Consumers import and
use it as a static singleton:

```python
from slogpy.slog import Slog

Slog.info("message")
```

- No factory functions that return `Slog` instances are permitted.
- New functionality MUST be added as `@classmethod` methods on `Slog`.
- Helper modules (e.g., `Section`, `SlogProgress`) MAY be classes but
  MUST integrate with the shared `Slog` console and file handler.

**Rationale**: A single static entry point eliminates configuration
drift and keeps the API surface predictable for script authors.

### II. Dual Output

Every log call MUST write to both a Rich console and a Python
`logging.FileHandler`.

- Console output MUST respect the configured log-level threshold.
- File output MUST capture all levels regardless of threshold.
- Rich markup in messages MUST be stripped (via `strip_style_markup`)
  before writing to the file handler.
- Progress bars (`SlogProgress`) MUST share the `Slog` Rich console
  to prevent display conflicts.

**Rationale**: Script operators need immediate visual feedback while
retaining a complete audit trail in log files.

### III. Ruff Compliance (NON-NEGOTIABLE)

All code MUST pass the Ruff rules defined in `ruff.toml` with zero
violations.

- The rule set in `ruff.toml` is authoritative; rules MUST NOT be
  added, removed, or ignored without explicit maintainer approval.
- `# noqa` exceptions MUST NOT be added without prior discussion and
  documented justification.
- Line length is 120 characters.

**Rationale**: Automated, deterministic linting prevents style
debates and keeps diffs focused on logic.

### IV. Test Discipline

All tests MUST use `pytest` and follow these conventions:

- Console-output tests MUST use `capsys`.
- File-output tests MUST use the `temp_log_file` fixture from
  `conftest.py` (creates a temp directory and initializes slog with a
  temp file path).
- Every test function MUST include a docstring following the
  Given/When/Then pattern.
- New public `Slog` methods MUST have at least one console test and
  one file test before merging.

**Rationale**: Structured, repeatable tests catch regressions early
and document expected behavior for future contributors.

### V. Simplicity & Minimalism

slogpy MUST remain opinionated and simple to use for the common case.

- Features MUST target the majority of logging needs for Python
  scripts and CLI tools; niche use-cases SHOULD be deferred or
  rejected (YAGNI).
- Configuration surface MUST stay small: `initialize()` with
  optional `module`, `tag`, `path`, and `log_level` covers the
  expected setup.
- Dependencies MUST be kept minimal: `rich` for console rendering
  and Python's built-in `logging` for file output.

**Rationale**: The library's value proposition is zero-friction
logging; complexity undermines that promise.

## Technology & Tooling Constraints

- **Language**: Python ≥ 3.10.
- **Dependency management**: Poetry with `poetry-dynamic-versioning`.
- **Versioning**: Published version is derived from git tags via
  `poetry-dynamic-versioning`; `__version__` in `__init__.py` is a
  placeholder and MUST NOT be manually bumped.
- **Console rendering**: Rich (`>=12,<15`).
- **Linting/Formatting**: Ruff (see Principle III).
- **Testing**: pytest (`>=8,<10`), coverage (`^7.5.1`).
- **Custom log levels**: `MINIMAL=0, DEBUG=1, INFO=5, WARN=9,
  ERROR=10, FATAL=99`. These MUST be mapped to Python `logging`
  levels for file output.

## Development Workflow

1. **Branch from `main`** for all feature and fix work.
2. **Write tests first** when adding new `Slog` methods (per
   Principle IV).
3. **Run the full suite** (`poetry run pytest`) before opening a PR.
4. **Run linting** (`poetry run ruff check .`) and formatting
   (`poetry run ruff format .`) before committing.
5. **Commit messages** MUST follow Conventional Commits
   (e.g., `feat:`, `fix:`, `test:`, `docs:`).
6. **PRs MUST pass** all CI checks (tests + ruff) before merge.

## Governance

- This constitution supersedes all ad-hoc practices. Where a
  conflict exists, the constitution is authoritative.
- Amendments require:
  1. A description of the change and its rationale.
  2. An update to the version number following semver rules
     (MAJOR for incompatible governance changes, MINOR for new
     principles or materially expanded guidance, PATCH for
     clarifications and wording fixes).
  3. Updating `Last Amended` date.
  4. Propagation check across `.specify/templates/` to ensure
     consistency.
- All PRs and code reviews MUST verify compliance with these
  principles.
- Runtime development guidance lives in
  `.github/copilot-instructions.md` and MUST remain consistent
  with this constitution.

**Version**: 1.1.0 | **Ratified**: 2026-02-06 | **Last Amended**: 2026-02-06
