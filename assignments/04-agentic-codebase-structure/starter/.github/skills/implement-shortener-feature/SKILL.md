---
name: implement-shortener-feature
description: "Use when implementing a feature from docs/TASKS.md in this FastAPI link shortener; guides plan, behavioral testing, implementation, verification, and summary."
argument-hint: "Feature task from docs/TASKS.md"
---

# Implement a link-shortener feature

Use this workflow for one selected task from `docs/TASKS.md`.

1. Read the selected task and `AGENTS.md`.
2. Inspect the related route, persistence code, and `test_main.py`.
3. Before editing, state the expected behavior and the files likely to change.
4. Add an independent behavioral test through the FastAPI public API. Run it first and
   confirm it fails for the expected reason.
5. Implement the smallest change that satisfies the task and preserves existing
   behavior.
6. Run the full suite with `python -m pytest -q`; report the result explicitly.
7. Review the diff for scope and unintended changes. Summarize the behavior, tests, and
   any remaining risks.
