---
name: implement-feature
description: Guide the implementation of a feature from docs/TASKS.md in the link shortener following test-first methodology and repository boundaries.
---

# Feature Implementation Workflow

Follow this 7-step procedure sequentially when implementing any task from `docs/TASKS.md`.

## Step 1: Read Task & Guidance
- Read the target task specification in `docs/TASKS.md`.
- Review general boundaries in `AGENTS.md` and testing rules in `tests/AGENTS.md`.

## Step 2: Inspect Code & Existing Tests
- Review current routes, models, and database queries in `main.py`.
- Review existing test coverage in `tests/test_main.py`.
- Identify existing contracts that must remain backward-compatible.

## Step 3: State Expected Behavior & Affected Files
Before modifying any files, state:
- Exact HTTP endpoint, method, request schema, and response schemas.
- Success status codes and failure status codes (e.g., 400 for validation errors, 409 for conflicts).
- Edge cases (reserved paths, special characters, duplicates).
- The list of files to be modified or created.

## Step 4: Add Failing Behavioral Tests
- Add new test cases to `tests/test_main.py` covering both success and edge/failure cases.
- Follow `tests/AGENTS.md`: test through `TestClient`, use unique aliases to avoid collision across test runs, and assert on HTTP response behavior.
- Run `pytest` to confirm that the new tests fail specifically due to missing functionality (not syntax or import errors).

## Step 5: Implement Minimal Change
- Update `main.py` with the minimal logic required to pass the new tests.
- Ensure all database queries use parameterized inputs (`?`).
- Maintain backward compatibility for existing routes and callers.
- Avoid introducing new dependencies or refactoring unrelated code.

## Step 6: Verify Test Suite
- Run `pytest` to ensure all tests pass.
- Re-run `pytest` immediately a second time to guarantee tests are idempotent and independent of preexisting database state.

## Step 7: Summarize & Assess Risks
Provide a concise summary:
- Summary of changes by file.
- New test cases and the specific behaviors verified.
- Confirmation of full `pytest` passing.
- Any remaining edge cases, assumptions, or operational risks.
