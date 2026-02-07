# Feature Specification: Idiomatic Naming & Dependency Updates

**Feature Branch**: `001-idiomatic-naming-deps`  
**Created**: 2026-02-06  
**Status**: Draft  
**Input**: User description: "Adopt idiomatic Pascal case for Slog class usage, bump Python to 3.10, broaden Rich to 12-14, and broaden pytest to 8-9"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Idiomatic Import and Usage (Priority: P1)

A developer using slogpy imports the `Slog` class and calls its methods using standard Python Pascal case naming, without aliasing to a lowercase name. This eliminates the need for `# noqa: N813` comments that suppress linting warnings and aligns with Python naming conventions.

**Why this priority**: This is the primary public-facing change. Every code example, import statement, and downstream consumer is affected. Getting this right first unblocks all other work.

**Independent Test**: Can be fully tested by importing `Slog` directly (without `as slog`) and calling `Slog.info(...)`, `Slog.warn(...)`, etc. — verifying that all existing test assertions still pass with the new calling convention.

**Acceptance Scenarios**:

1. **Given** a Python file that imports `from slogpy.slog import Slog`, **When** the developer calls `Slog.info("message")`, **Then** the message appears on the console and in the log file, identical to the previous `slog.info("message")` behavior.
2. **Given** the slogpy source files (`section.py`, `progress.py`, `__main__.py`), **When** they are updated to use `Slog` directly, **Then** no `# noqa: N813` comments exist in any source file.
3. **Given** a user reading the README, **When** they follow the code examples, **Then** all examples use `Slog.method()` syntax (not `slog.method()`).

---

### User Story 2 - Broadened Dependency Compatibility (Priority: P2)

A developer installs slogpy in an environment that has Python 3.10+, any Rich version from 12.x through 14.x, and any pytest version from 8.x through 9.x. The library installs and functions correctly without dependency conflicts.

**Why this priority**: Broadening compatibility reduces friction for adoption. However, the code changes are mechanical (version constraint edits in `pyproject.toml`) and don't affect runtime behavior, so this is lower priority than the naming change.

**Independent Test**: Can be tested by installing slogpy with boundary versions (Rich 12.0, Rich 14.x, pytest 8.1, pytest 9.x) and verifying the test suite passes in each case.

**Acceptance Scenarios**:

1. **Given** a fresh environment with Python 3.10 and Rich 12.0, **When** slogpy is installed and its tests run, **Then** all tests pass.
2. **Given** a fresh environment with Python 3.13 and Rich 14.x, **When** slogpy is installed and its tests run, **Then** all tests pass.
3. **Given** a project that depends on pytest 9.x, **When** slogpy is added as a dev dependency, **Then** no version conflict occurs.

---

### User Story 3 - Updated Documentation and Guidance (Priority: P3)

A developer or contributor reads the README, copilot-instructions, or constitution and finds all documentation consistent with the new naming convention and dependency ranges.

**Why this priority**: Documentation accuracy matters, but is not a functional requirement — it follows after the code changes are made.

**Independent Test**: Can be verified by searching all markdown files for the old pattern (`Slog as slog`, `^3.8`, `^13.7.0`, `^8.1.1`) and confirming zero matches.

**Acceptance Scenarios**:

1. **Given** the README.md file, **When** a contributor reads the code examples, **Then** all examples show `from slogpy.slog import Slog` and `Slog.method()` calls.
2. **Given** the `.github/copilot-instructions.md` file, **When** a contributor reads the architecture section, **Then** it describes the `Slog` class usage without the lowercase alias.
3. **Given** the `pyproject.toml` file, **When** a contributor inspects dependencies, **Then** Python is `>=3.10`, Rich is `>=12,<15`, and pytest is `>=8,<10`.

---

### Edge Cases

- What happens when a downstream project still uses `from slogpy.slog import Slog as slog`? The import still works — aliasing is a consumer choice. This change only affects slogpy's own code and examples.
- What happens when Rich 12.x lacks an API that slogpy uses? slogpy uses only basic Rich console printing and progress bars, which have been stable since Rich 12.
- What happens when pytest 9's breaking changes affect test collection? slogpy's tests use only basic pytest features (parametrize, capsys, fixtures) which are unchanged between pytest 8 and 9.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: All slogpy source files MUST import `Slog` directly (`from slogpy.slog import Slog`) without aliasing to a lowercase name.
- **FR-002**: All slogpy source files MUST NOT contain `# noqa: N813` comments related to the `Slog` import.
- **FR-003**: All usages of `slog.method()` in slogpy source files MUST be replaced with `Slog.method()`.
- **FR-004**: All usages of `slog.CONSTANT` (e.g., `slog.INFO`, `slog.DEBUG`) in slogpy source files MUST be replaced with `Slog.CONSTANT`.
- **FR-005**: The `pyproject.toml` Python version constraint MUST be changed from `^3.8` to `>=3.10`.
- **FR-006**: The `pyproject.toml` Rich version constraint MUST be changed from `^13.7.0` to `>=12,<15`.
- **FR-007**: The `pyproject.toml` pytest version constraint MUST be changed from `^8.1.1` to `>=8,<10`.
- **FR-008**: All code examples in README.md MUST use the `Slog` (Pascal case) calling convention.
- **FR-009**: The `.github/copilot-instructions.md` MUST be updated to reflect the new import style and dependency ranges.
- **FR-010**: All existing tests MUST continue to pass after the naming and dependency changes.

## Success Criteria *(mandatory)*

1. Zero occurrences of `as slog` aliasing pattern in any slogpy-owned source or test file.
2. Zero occurrences of `# noqa: N813` in any source or test file.
3. All existing tests pass with the updated code (`poetry run pytest` exits 0).
4. All existing tests pass with Ruff linting (`poetry run ruff check .` exits 0 with no N813 suppressions).
5. Library installs and tests pass on Python 3.10 with Rich 12.x.
6. Library installs and tests pass on Python 3.13 with Rich 14.x.
7. No downstream breaking change — consumers who alias `Slog as slog` in their own code are unaffected.

## Assumptions

- Consumers are free to alias `Slog` however they wish in their own projects; this change only governs slogpy's own codebase and documentation.
- Rich versions 12.x through 14.x all support the Rich console and progress bar APIs that slogpy uses (`rich.console.Console`, `rich.progress.Progress`).
- pytest 9.x does not introduce breaking changes to the basic test features slogpy uses (parametrize, fixtures, capsys).
- Python 3.8 and 3.9 are already EOL and dropping support for them is a non-breaking change for the library's target audience.
