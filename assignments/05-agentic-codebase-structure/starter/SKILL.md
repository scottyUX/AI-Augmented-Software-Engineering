---
name: implement-feature
description: Reusable workflow for implementing a new feature or task from docs/TASKS.md using a strict test-first loop.
---

# Reusable Workflow: Implement a New Feature

Use this workflow whenever a new feature or task from `docs/TASKS.md` is requested for the Link Shortener service. Follow every step in sequence without skipping ahead.

## Step 1: Read the Task from `docs/TASKS.md`
- Open `docs/TASKS.md` and read the target task specification carefully.
- Identify the required HTTP endpoints, request fields, response payloads, and status codes (e.g., `200`, `307`, `400`, `404`, `409`, `410`).

## Step 2: Inspect Existing Code
- Read `AGENTS.md`, `tests/AGENTS.md`, `main.py`, and `test_main.py`.
- Understand the current FastAPI routes, Pydantic models (`ShortenRequest`), SQLite table schema (`links`), and existing test setup.

## Step 3: Write Down the Expected Behavior
- Before touching any code, explicitly state:
  - The public API contract (endpoint method, path, request body, response JSON, and status codes).
  - Success scenarios and failure/edge cases.
  - Any schema or state adjustments needed in SQLite (`links` table).

## Step 4: Add a Failing Test First (Red)
- Add new test function(s) in `test_main.py` (following the rules in `tests/AGENTS.md`):
  - Exercise the feature strictly through the public HTTP API (`TestClient(app)`).
  - Cover both success and failure cases.
  - Ensure test independence.
- Run `pytest` and verify that the new test(s) **fail** as expected while existing tests continue to pass.

## Step 5: Implement the Smallest Change (Green)
- Modify `main.py` with the minimal, cleanest code change needed to satisfy the new test(s).
- Respect product boundaries defined in `AGENTS.md` (no extra dependencies, use parameterized SQL queries, close DB connections properly).

## Step 6: Run `pytest` and Verify
- Execute `pytest` from the project root.
- Confirm that **100% of tests pass** (both new and existing tests).
- If any test fails, fix the implementation and re-run `pytest` until green.

## Step 7: Summarize Changes and Risks
- Provide a concise post-implementation summary covering:
  - **Changes Made**: Files and functions/endpoints added or updated.
  - **Test Coverage**: Which success and failure cases are verified by `pytest`.
  - **Risks & Edge Cases**: Any migration considerations (e.g., existing `links.db` schema columns), concurrency nuances, or boundary conditions.

