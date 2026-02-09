# Plan: Fix release.yaml

**Branch**: `001-idiomatic-naming-deps` (bundled with current work)
**Date**: 2026-02-07
**Target file**: `.github/workflows/release.yaml`

## Summary

The release workflow has 9 issues across security, correctness, and maintenance categories. All fixes target a single file and can be applied in one commit.

## Phase 1 — Trigger & Gates (issues #1, #2, #7)

1. **Replace `on: push` with scoped triggers:**
   - `on: push: tags: ['v*']` for PyPI + GitHub Release + Sigstore jobs
   - `on: workflow_dispatch` for manual trigger (build job only)
2. **Fix the PyPI tag filter:** Change `startsWith(github.ref, 'refs/tags/x')` → `startsWith(github.ref, 'refs/tags/v')` to match semver tags like `v1.0.0`
3. **Add a guard to TestPyPI:** Gate it to tag pushes with `if: startsWith(github.ref, 'refs/tags/v')` so it only publishes when tags are pushed, not on manual workflow_dispatch

## Phase 2 — Build correctness (issue #6)

4. **Install `poetry-dynamic-versioning` in the build step** so the package gets the correct version from the git tag instead of the `0.1.0` placeholder. Two options:
   - **Option A** (recommended): Switch from `python -m build` to `poetry build` with the dynamic versioning plugin installed
   - **Option B**: `pip install poetry-dynamic-versioning[plugin]` before calling `python -m build`, and ensure the build backend hook picks it up

## Phase 3 — Security hardening (issues #4, #5, #9)

5. **Fix shell injection** in the `github-release` job: Replace direct `${{ github.ref_name }}` interpolation with an environment variable:
   ```yaml
   env:
     TAG_NAME: ${{ github.ref_name }}
   run: gh release create "$TAG_NAME" ...
   ```
   Apply to both the `Create GitHub Release` and `Upload artifact signatures` steps.

6. **Pin third-party actions to commit SHAs** instead of mutable tags:
   - `pypa/gh-action-pypi-publish@release/v1` → pin to the full SHA of the current v1 release
   - `sigstore/gh-action-sigstore-python@v1.2.3` → pin to SHA (after upgrading in Phase 4)
   - Add a comment with the human-readable version next to each SHA

7. **Add `persist-credentials: false`** to the `actions/checkout` step in the build job

## Phase 4 — Dependency upgrades (issues #3, #8)

8. **Upgrade deprecated actions:**
   - `actions/setup-python@v4` → `@v5`
   - `actions/upload-artifact@v3` → `@v4`
   - `actions/download-artifact@v3` → `@v4` (in all three jobs that use it)

9. **Upgrade Sigstore action:** `sigstore/gh-action-sigstore-python@v1.2.3` → `@v3.x` (review migration guide for breaking changes in v2 and v3 — input parameter names changed)

10. **Verify the `github-release` job chain** works now that the PyPI gate (issue #2) is fixed — it should naturally unblock since it depends on `publish-to-pypi`

## Phase 5 — Validation

11. **Test the full pipeline** without actually publishing:
    - Push a test tag (e.g., `v0.0.0-rc1`) and verify the build produces a correctly-versioned artifact
    - Verify TestPyPI gate prevents publishing on feature branches
    - Verify PyPI gate only triggers on `v*` tags
    - Delete the test tag and any test releases afterward

## Execution order

| Step | Depends on | Can parallel with |
|------|-----------|-------------------|
| 1–3 (triggers) | — | 5–7 (security) |
| 4 (build) | — | 1–3 |
| 5–7 (security) | — | 1–3 |
| 8–9 (upgrades) | — | 1–7 |
| 10 (chain fix) | 1–3 | 8–9 |
| 11 (validation) | All above | — |

All of steps 1–9 are edits to the same file, so in practice they'll be done as a single commit. Step 11 requires pushing a tag to trigger the workflow.

## Issue Reference

| # | Severity | Issue |
|---|----------|-------|
| 1 | 🔴 Critical | `on: push` with no filter — every push triggers build and TestPyPI publish |
| 2 | 🔴 Critical | PyPI tag filter `refs/tags/x` never matches semver tags — publishing is dead |
| 3 | 🟠 High | `actions/upload-artifact@v3` and `download-artifact@v3` are deprecated (Node 16) |
| 4 | 🔴 Critical | Shell injection via `${{ github.ref_name }}` in `gh release` commands |
| 5 | 🟡 Medium | Third-party actions pinned to mutable tags, not commit SHAs |
| 6 | 🟠 High | `poetry-dynamic-versioning` not installed — built package gets placeholder version |
| 7 | 🟡 Medium | TestPyPI has no conditional guard — publishes on every push |
| 8 | 🟡 Medium | `github-release` job is dead code (depends on never-triggering PyPI job) |
| 9 | 🟡 Medium | Checkout retains credentials unnecessarily |
