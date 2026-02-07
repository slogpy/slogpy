# Tasks: Idiomatic Naming & Dependency Updates

**Input**: Design documents from `/specs/001-idiomatic-naming-deps/`
**Prerequisites**: plan.md (complete), spec.md (complete)

**Tests**: No new tests requested. Existing tests are renamed in-place and re-validated.

**Organization**: Tasks grouped by user story (US1 = naming, US2 = deps, US3 = docs). No tests phase — this is a rename refactor, not new functionality.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story (US1, US2, US3) — omitted for setup/foundational/polish phases

---

## Phase 1: Setup

**Purpose**: No setup needed — existing project, no new structure

_(No tasks — project already initialized and structured)_

---

## Phase 2: Foundational

**Purpose**: No blocking prerequisites — all changes are independent file edits

_(No tasks — no shared infrastructure to build first)_

---

## Phase 3: User Story 1 — Idiomatic Import and Usage (Priority: P1) 🎯 MVP

**Goal**: Replace all `Slog as slog` aliases with direct `Slog` usage across source and test files. Remove all `# noqa: N813` comments.

**Independent Test**: Run `poetry run pytest && poetry run ruff check .` — all tests pass, zero lint violations, zero `as slog` or `# noqa: N813` occurrences.

### Source files

- [ ] T001 [P] [US1] Rename `slog` → `Slog` in slogpy/__main__.py (import, ~40 call sites, remove `# noqa: N813`)
- [ ] T002 [P] [US1] Rename `slog` → `Slog` in slogpy/section.py (import, ~8 method/constant refs, remove `# noqa: N813`)
- [ ] T003 [P] [US1] Rename `slog` → `Slog` in slogpy/progress.py (import, ~3 `_rich_console` refs, remove `# noqa: N813`)

### Test files

- [ ] T004 [P] [US1] Rename `slog` → `Slog` in tests/conftest.py (import, ~4 call sites, remove `# noqa: N813`)
- [ ] T005 [P] [US1] Rename `slog` → `Slog` in tests/test_annoy_console.py (import, all call sites, remove `# noqa: N813`)
- [ ] T006 [P] [US1] Rename `slog` → `Slog` in tests/test_slogpy_console_debug.py (import, all call sites, remove `# noqa: N813`)
- [ ] T007 [P] [US1] Rename `slog` → `Slog` in tests/test_slogpy_file_debug.py (import, all call sites, remove `# noqa: N813`)
- [ ] T008 [P] [US1] Rename `slog` → `Slog` in tests/test_slogpy_file_info.py (import, all call sites, remove `# noqa: N813`)

### Validation

- [ ] T009 [US1] Validate rename: run `poetry run pytest` and `poetry run ruff check .` — all pass, zero `as slog` or `# noqa: N813` in source/test files

**Checkpoint**: All source and test files use `Slog` directly. Tests pass. Ruff clean.

---

## Phase 4: User Story 2 — Broadened Dependency Compatibility (Priority: P2)

**Goal**: Update `pyproject.toml` version constraints for Python, Rich, and pytest. Regenerate lockfile.

**Independent Test**: Run `poetry lock && poetry install && poetry run pytest` — lockfile regenerates cleanly, tests still pass.

- [ ] T010 [US2] Update pyproject.toml: `python = "^3.8"` → `python = ">=3.10"`, `rich = "^13.7.0"` → `rich = ">=12,<15"`, `pytest = "^8.1.1"` → `pytest = ">=8,<10"`
- [ ] T011 [US2] Regenerate lockfile: run `poetry lock` and verify it resolves without errors
- [ ] T012 [US2] Validate deps: run `poetry install && poetry run pytest` — all tests pass with updated constraints

**Checkpoint**: Dependency constraints broadened. Lockfile clean. Tests pass.

---

## Phase 5: User Story 3 — Updated Documentation and Guidance (Priority: P3)

**Goal**: Update all documentation to reflect the new `Slog` naming convention and dependency ranges.

**Independent Test**: Search all markdown files for `Slog as slog`, `^3.8`, `^13.7.0`, `^8.1.1` — zero matches.

- [ ] T013 [P] [US3] Update README.md: replace 3 import lines (`Slog as slog` → `Slog`) and ~20+ `slog.` → `Slog.` in code examples
- [ ] T014 [P] [US3] Update .github/copilot-instructions.md: replace architecture description and import example to use `Slog` directly
- [ ] T015 [P] [US3] Update .specify/memory/constitution.md: clear sync impact report TODOs now that implementation is complete

**Checkpoint**: All documentation consistent with new naming and dependency ranges.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation across all user stories

- [ ] T016 Final validation: run `poetry run ruff check . && poetry run ruff format --check . && poetry run pytest` — all green
- [ ] T017 Verify zero occurrences: `grep -r "as slog" slogpy/ tests/` and `grep -r "noqa: N813" slogpy/ tests/` both return empty

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: N/A — no tasks
- **Phase 2 (Foundational)**: N/A — no tasks
- **Phase 3 (US1 - Naming)**: Can start immediately — no prerequisites
- **Phase 4 (US2 - Deps)**: Can start immediately — independent of US1 (different file: `pyproject.toml`)
- **Phase 5 (US3 - Docs)**: Should follow US1 completion (docs reference the new naming convention)
- **Phase 6 (Polish)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (P1)**: No dependencies — can start immediately
- **US2 (P2)**: No dependencies on US1 — can run in parallel (different files)
- **US3 (P3)**: Depends on US1 completion (docs must reflect the new naming). Can run in parallel with US2.

### Within Each User Story

- US1: All source files (T001-T003) can run in parallel [P]. All test files (T004-T008) can run in parallel [P]. Validation (T009) runs after all renames.
- US2: Sequential — edit pyproject.toml (T010) → lock (T011) → validate (T012)
- US3: All doc files (T013-T015) can run in parallel [P]

### Parallel Opportunities

```text
# Maximum parallelism example:
# Stream A (US1 source):  T001, T002, T003 in parallel
# Stream B (US1 tests):   T004, T005, T006, T007, T008 in parallel (same time as Stream A)
# Stream C (US2):         T010 → T011 → T012 (can run alongside Streams A+B)
#
# After US1 validates (T009):
# Stream D (US3 docs):    T013, T014, T015 in parallel
#
# Final: T016, T017 (sequential)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 3: US1 (T001–T009)
2. **STOP and VALIDATE**: `poetry run pytest && poetry run ruff check .`
3. All source/test files now use idiomatic `Slog` — deliverable on its own

### Incremental Delivery

1. US1 (naming) → Tests pass, ruff clean → Commit
2. US2 (deps) → Lock resolves, tests pass → Commit
3. US3 (docs) → All docs consistent → Commit
4. Polish (T016–T017) → Full validation → Commit

---

## Notes

- All T001–T008 are [P] — different files, no cross-dependencies
- T013–T015 are [P] — different doc files, no cross-dependencies
- No new test files are created; existing tests are renamed in-place
- The `slog.py` file itself is NOT modified (it defines the `Slog` class, not the alias)
- `test_slogpy.py` is NOT modified (it doesn't use the `slog` alias)
- Total: 17 tasks across 3 user stories + 1 polish phase
