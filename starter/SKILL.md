# Feature Implementation Workflow

This skill defines the standard operating procedure for implementing new features in this repository. Follow these steps sequentially:

1. **Context Gathering:** Read the selected task description in `docs/TASKS.md` and review the repository guidance in `AGENTS.md`.
2. **Code Inspection:** Inspect the existing application logic (`main.py`) and the current test suite (`test_main.py`) to understand the integration points.
3. **Strategy Declaration:** State the expected behavior of the new feature and explicitly list the files that will be affected. Do not edit files in this step.
4. **Test-Driven Development:** Add a failing behavioral test to `test_main.py` that asserts the expected outcome of the new feature.
5. **Implementation:** Implement the smallest possible change in `main.py` that satisfies the task requirements and makes the failing test pass.
6. **Verification:** Run `pytest` via the shell tool to ensure all tests (original and new) pass successfully.
7. **Summary:** Summarize the completed changes and identify any remaining risks or edge cases.