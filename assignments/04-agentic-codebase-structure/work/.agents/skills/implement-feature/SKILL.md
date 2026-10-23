---
name: implement-feature
description: Implement one feature from docs/TASKS.md in the link shortener test-first. Use when asked to add, build, or implement a task/feature in this repository.
---

# Implement a feature (test-first)

Follow these steps in order. Don't skip ahead.

1. **Read the task and guidance.** Open `docs/TASKS.md` and find the selected task.
   Read `AGENTS.md` and `tests/AGENTS.md`.
2. **Inspect code and tests.** Read `main.py` (routes, `init_db`) and the existing tests
   (`test_main.py`, `tests/`). Run `pytest -q` and confirm it is green before changing anything.
3. **State the plan** in chat before editing:
   - Expected behavior, including every status code and response body.
   - Edge and failure cases.
   - Files you will touch (normally `main.py` and one new `tests/test_<feature>.py`).
   - Schema changes, and how an existing `links.db` is migrated.
4. **Add a failing behavioral test** in `tests/test_<feature>.py` using the `client`
   fixture. Cover success and at least one failure case. Run `pytest -q` and confirm the
   new tests **fail for the right reason** (e.g. 404 because the route doesn't exist yet).
5. **Implement the smallest change** in `main.py` that satisfies the task. Parameterized
   SQL only; no new dependencies; no unrelated refactors.
6. **Run `pytest -q`.** All original and new tests must pass. If something fails, fix the
   code, not the original tests.
7. **Summarize** in chat:
   - What changed (files + one line each).
   - Test results (`N passed`).
   - Remaining risks or follow-ups (concurrency, migration, things deliberately left out).
