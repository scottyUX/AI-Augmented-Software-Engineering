# AGENTS.md — Link Shortener Service

## Overview
This repository contains a lightweight HTTP Link Shortener service built with **FastAPI** and **SQLite**.
It accepts long URLs (`http://` or `https://`), stores them in a local SQLite database (`links.db`), generates a compact Base62 short code (or uses a custom alias), and redirects clients (`307 Temporary Redirect`) when they request `GET /{code}`.

## Key File Locations
- `main.py` — FastAPI application entry point, SQLite database helpers (`get_db`, `init_db`), Base62 encoder, and HTTP route handlers (`POST /shorten`, `GET /{code}`).
- `test_main.py` — Primary `pytest` test suite exercising the HTTP endpoints via FastAPI's `TestClient`.
- `tests/AGENTS.md` — Scoped testing rules and guidelines for writing and maintaining tests.
- `docs/TASKS.md` — Product backlog of small, self-contained feature tasks (custom aliases, click counters, link expiry).
- `requirements.txt` — Python runtime and testing dependencies (`fastapi`, `uvicorn`, `pytest`, `httpx`).

## Installation, Running, and Testing
Run all commands from the project root directory (`assignments/05-agentic-codebase-structure/starter`):

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the test suite
pytest

# 3. Start the development server (http://localhost:8000, OpenAPI docs at /docs)
uvicorn main:app --reload
```

## Product Boundaries
### What Belongs in This Service
- Creating shortened links (`POST /shorten`) with URL validation (`http://` or `https://`).
- Resolving short codes (`GET /{code}`) with `307` HTTP redirects.
- Core link lifecycle features specified in `docs/TASKS.md` (custom aliases, click counting/stats, and link expiration).
- Lightweight, self-contained SQLite persistence using Python's built-in `sqlite3` module.

### What Does NOT Belong in This Service
- User accounts, authentication, OAuth, or role-based access control.
- Frontend UI frameworks, HTML templates, CSS/JS build pipelines, or static asset serving.
- External database servers (PostgreSQL, Redis), ORMs, or background job queues.
- Third-party analytics trackers, billing, or external network calls during request handling.

## Change Workflow
Every code change or new feature MUST follow this four-step loop:
1. **Understand** — Read the task in `docs/TASKS.md` and inspect `main.py` and `test_main.py` to understand existing behavior and schema constraints.
2. **Test** — Write a clear, failing test in `test_main.py` (or `tests/`) covering both happy-path and error responses via the public HTTP API.
3. **Implement** — Make the smallest, cleanest change in `main.py` necessary to satisfy the requirement without breaking existing functionality.
4. **Verify** — Run `pytest` to confirm 100% of new and existing tests pass, and review the diff for simplicity, edge cases, and adherence to product boundaries.

## Guardrails & Conventions
- **Never** delete or weaken existing tests in `test_main.py` to make a change pass.
- **Always** use parameterized SQL queries (`?` placeholders) to prevent SQL injection.
- **Always** close database connections using `with closing(get_db()) as conn:`.
- Keep the service dependency-free beyond `requirements.txt`.

