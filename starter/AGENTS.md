# Repository Guidance — Link Shortener

## Application Overview
A minimalist URL shortener service built with FastAPI and SQLite. It converts HTTP/HTTPS URLs into Base62 short codes and handles 307 redirects.

## Important Files
- `main.py` — Complete application logic (FastAPI routes, Base62 encoder, SQLite operations).
- `test_main.py` — Pytest suite using FastAPI's `TestClient`.
- `docs/TASKS.md` — Available feature enhancement tasks.
- `requirements.txt` — Python dependencies (`fastapi`, `uvicorn`, `pydantic`, `pytest`).

## Operations & Verification
- **Install:** `pip install -r requirements.txt`
- **Test:** `pytest` (Run before making changes and after every edit)
- **Run:** `uvicorn main:app --reload` (Docs at `http://localhost:8000/docs`)

## Product Boundaries
- **In Scope:** REST API endpoints, short code generation, HTTP redirects, basic analytics/expiry, SQLite storage.
- **Out of Scope:** Frontend UI templates, user authentication, external caches (Redis), third-party ORMs, complex database migrations.

## Change Workflow
1. **Understand:** Read `main.py` and existing tests to inspect route signatures.
2. **Test First:** Identify required status codes and write/update tests in `test_main.py`.
3. **Implement:** Apply minimal, idiomatic edits to `main.py` matching existing Pydantic/SQLite patterns.
4. **Verify:** Execute `pytest` to ensure all tests pass without warnings or regressions.