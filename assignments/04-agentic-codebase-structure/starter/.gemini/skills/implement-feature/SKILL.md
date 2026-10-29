---
name: implement-feature
description: Guide the agent through implementing a new feature with structured testing, minimal changes, and verification.
---

# Implement Feature Workflow

Follow these seven steps sequentially when implementing a feature:

1. **Read the selected task and repository guidance:** Review `docs/TASKS.md`, `AGENTS.md`, and project instructions to understand requirements and constraints.
2. **Inspect related code and tests:** Analyze `main.py` and `test_main.py` to understand existing app logic and test setup.
3. **State expected behavior and affected files:** Clearly define the expected inputs, outputs, error conditions (e.g. 409 conflict), and list the files to be modified.
4. **Add a failing behavioral test:** Add a new test case to `test_main.py` and run `pytest` to verify that it fails as expected.
5. **Implement the smallest change:** Apply surgical, minimal code modifications in `main.py` to satisfy the feature requirements.
6. **Run pytest:** Execute `pytest` to confirm all tests pass successfully.
7. **Summarize changes and remaining risks:** Provide a concise summary of the modifications made and highlight any remaining edge cases or risks.
