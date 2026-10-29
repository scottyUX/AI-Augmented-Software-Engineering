# GEMINI.md

For complete repository guidance, architecture, and workflows, please read [AGENTS.md](./AGENTS.md).

## Scoped Testing Instructions (`test_main.py`)
Because existing tests reside in root `test_main.py` rather than a `tests/` subdirectory, subfolder instructions (`tests/AGENTS.md`) do not apply via automatic directory scoping. Whenever creating or modifying root-level `test_main.py`, Gemini CLI must explicitly read and adhere to the test-specific rules in [`tests/AGENTS.md`](./tests/AGENTS.md). Run `pytest` to validate behavioral tests.
