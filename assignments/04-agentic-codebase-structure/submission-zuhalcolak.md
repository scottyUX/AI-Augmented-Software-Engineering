# Week 4 Submission (Structuring a Repo for Agents) — Zuhal Çolak

**Repository:** https://github.com/zuhalcolak/week4-agentic-codebase-structure

Implemented **Task 1: Custom Alias** using an agent-ready architecture with three distinct lifecycle stages (Plan, Implement, Review).

### Deliverables Included:
- **Root `AGENTS.md`**: Concise repository guidance (<40 lines) covering system overview, file directory layout, run/test commands, product boundaries, and change workflow.
- **Scoped Instruction (`tests/AGENTS.md`)**: Testing rules requiring public API execution (`TestClient`), symmetric success/failure coverage, execution independence, and behavioral assertions.
- **Reusable Workflow (`.agents/skills/implement-feature/SKILL.md`)**: Standardized 7-step test-driven feature development procedure conforming to the Agent Skills standard.
- **Feature Implementation & Tests**: Implemented custom alias with validation and collision avoidance in `main.py`; 8 tests in `tests/test_main.py` covering success paths, conflict handling (409), reserved routes (409), invalid characters (400), and auto-generation collision avoidance.
- **Lifecycle Sessions**: Documented in `docs/sessions/` (`01-plan.md`, `02-implement.md`, `03-review.md`).
- **`writeup.md`**: Answers all six required reflection and tool-mapping questions.

### Test Results
- All 8 tests passed consecutively (`pytest`):
  - `test_shorten_and_redirect`: PASS
  - `test_rejects_bad_url`: PASS
  - `test_unknown_code_404`: PASS
  - `test_custom_alias_success`: PASS
  - `test_custom_alias_conflict_409`: PASS
  - `test_custom_alias_reserved_name_409`: PASS
  - `test_custom_alias_invalid_characters_400`: PASS
  - `test_auto_generated_code_avoids_alias_collision`: PASS
