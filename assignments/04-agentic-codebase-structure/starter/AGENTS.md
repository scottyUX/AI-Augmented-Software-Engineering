# Agent Guidance (`AGENTS.md`)

## Purpose
Tiny FastAPI + SQLite link shortener service designed for agentic coding workflows.

## Important Files
- `main.py`: FastAPI application (`POST /shorten`, `GET /{code}`).
- `test_main.py`: Pytest test suite using `TestClient`.
- `docs/TASKS.md`: Feature tasks specification.

## Commands
- **Setup:** `pip install -r requirements.txt`
- **Run:** `uvicorn main:app --reload`
- **Test:** `pytest`

## Product Boundaries
- Focused strictly on core URL shortening and redirection.
- Uses local SQLite database (`links.db`).

## Workflow (Understand → Test → Implement → Verify)
1. **Understand:** Read `docs/TASKS.md` and repository guidance.
2. **Test:** Add failing behavioral tests before making changes.
3. **Implement:** Apply the minimal required changes to `main.py`.
4. **Verify:** Run `pytest` to confirm all tests pass successfully.
