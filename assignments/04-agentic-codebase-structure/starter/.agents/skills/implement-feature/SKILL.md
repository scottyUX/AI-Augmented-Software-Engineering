---
name: implement-feature
description: Standardized 7-step test-driven workflow for adding a feature to the link shortener.
---

# Feature Implementation Workflow

Follow this procedure sequentially whenever implementing a feature or task from `docs/TASKS.md`.

## Step 1: Read Guidance & Boundaries
Review `AGENTS.md` and the selected task description in `docs/TASKS.md`. Confirm that the proposed feature stays within defined product boundaries.

## Step 2: Code Inspection
Inspect `main.py` and `tests/test_main.py` to identify relevant data structures, SQL queries, schemas, and existing tests.

## Step 3: Contract Declaration
Before writing code, explicitly state:
- The exact API contract (request model, HTTP method, path, response codes, headers).
- The files that will be modified or created.

## Step 4: Write Failing Tests
In `tests/test_main.py`, implement behavioral tests asserting:
- Expected success behavior (status 200/307, correct payload/redirect).
- Edge cases and error handling (400 bad input, 409 conflict, etc.).
Run `pytest` to confirm the new tests fail for the expected reasons.

## Step 5: Minimal Implementation
Edit `main.py` with the minimal necessary implementation to satisfy the tests. Avoid unrelated refactoring or speculative features.

## Step 6: Verification
Run `pytest` twice consecutively to ensure:
- All preexisting tests pass.
- All new tests pass.
- No execution order dependencies or persistent state leaks exist.

## Step 7: Summary & Risk Assessment
Document:
- Summary of changes made.
- Validation results.
- Any remaining edge cases or operational risks.
