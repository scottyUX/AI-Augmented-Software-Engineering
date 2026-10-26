# Link Shortener — Agent Guide

A minimal FastAPI + SQLite URL shortener: `POST /shorten` maps an `http(s)` URL to a short code, and `GET /{code}` issues an HTTP 307 redirect to the target URL.

## File Navigation

| Path | Description |
|------|-------------|
| `main.py` | Core FastAPI application, database initialization, and endpoints |
| `tests/` | pytest suite, governed by scoped rules in `tests/AGENTS.md` |
| `docs/TASKS.md` | Task backlog for candidate features |
| `.agents/skills/implement-feature/` | Standardized feature development workflow (`SKILL.md`) |
| `links.db` | Local SQLite database file (gitignored, auto-created at runtime) |

## Setup, Run, and Test

```bash
pip install -r requirements.txt
uvicorn main:app --reload    # Runs server at http://localhost:8000
pytest                       # Runs test suite (defined in tests/)
```

## Product Boundaries

- **In Scope:** Shortening valid `http://` and `https://` URLs, performing fast redirects, and implementing small enhancements from `docs/TASKS.md`.
- **Out of Scope:** User authentication, UI frontend, external database engines, analytics dashboards, or background workers.
- **Route Integrity:** Generated or custom codes must NEVER conflict with or shadow reserved system routes: `/shorten`, `/docs`, `/redoc`, `/openapi.json`.
- **API Stability:** Preserve backward compatibility for existing endpoint responses (`status_code` and JSON schema `{"code": ..., "short_url": ...}`).
- **Data Safety:** Always interact with SQLite using parameterized queries (`?`) and `closing(get_db())`.

## Change Workflow

1. **Understand:** Read the task in `docs/TASKS.md` and check system boundaries.
2. **Test:** Write failing behavioral test cases covering success and failure paths.
3. **Implement:** Apply minimal, focused changes strictly meeting requirements.
4. **Verify:** Run the full `pytest` suite and confirm all tests pass cleanly.
