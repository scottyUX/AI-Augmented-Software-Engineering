---
name: implement-feature
description: Implement one feature from docs/TASKS.md in the link shortener, test-first. Use when asked to add or implement a task or feature in this repository.
---

# Implement a feature (test-first)

Follow these steps in order. Do not skip a step.

1. **Read the task and guidance.** Read the selected task in `docs/TASKS.md`, the root
   `AGENTS.md`, and `tests/AGENTS.md`.
2. **Inspect the code and tests.** Read `main.py` and the existing tests in `tests/`.
   Run `pytest` once to confirm the starting state is green.
3. **State the plan.** Before editing, write down:
   - the expected behavior (inputs, outputs, status codes, edge cases),
   - the files you will change.
4. **Add a failing behavioral test.** Add tests in `tests/` that follow `tests/AGENTS.md`:
   at least one success case and one failure/edge case. Run `pytest` and confirm the
   new tests fail for the right reason.
5. **Implement the smallest change** in `main.py` that makes them pass. Stay inside the
   product boundaries in `AGENTS.md` (no new dependencies, no refactors).
6. **Run `pytest`.** All original and new tests must pass. If not, fix and re-run.
7. **Summarize.** Report what changed (files, endpoints, schema), the test results,
   and any remaining risks or follow-ups.
