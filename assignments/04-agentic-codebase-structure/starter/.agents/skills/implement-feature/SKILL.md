---
name: implement-feature
description: Implement one Link Shortener feature using behavioral tests and minimal changes.
---

# Implement Feature — Link Shortener

Use this workflow when implementing a selected feature from `docs/TASKS.md`.

## Procedure

1. Read `AGENTS.md`, `docs/TASKS.md`, and the selected feature requirements.
2. Inspect the relevant application code and existing tests.
3. State the expected behavior, affected files, and planned changes before editing.
4. Add behavioral tests covering successful behavior and at least one failure or edge case. Run them and confirm the new tests fail for the expected reason.
5. Implement the smallest change needed to satisfy the selected task. Preserve existing functionality.
6. Run `python -m pytest -q` from the `starter/` directory. Confirm all existing and new tests pass.
7. Summarize the implemented behavior, modified files, test results, and any remaining risks.

## Constraints

- Follow repository guidance in `AGENTS.md`.
- Apply `tests/AGENTS.md` when editing files in `tests/`.
- Use the existing FastAPI and SQLite architecture.
- Implement only the selected feature.
- Do not introduce unrelated dependencies or refactor unrelated code.