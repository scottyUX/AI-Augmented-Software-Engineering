# Repository Guidance: Link Shortener

A lightweight FastAPI + SQLite link shortening service that generates short base62 codes or accepts custom aliases, redirecting visitors via HTTP 307.

## Structure
- `main.py`: Core FastAPI service, database initialization, route definitions (`POST /shorten`, `GET /{code}`).
- `links.db`: SQLite database file storing shortened link records (`id`, `code`, `url`).
- `tests/test_main.py`: End-to-end HTTP test suite using FastAPI `TestClient`.
- `tests/AGENTS.md`: Scoped instructions for authoring tests.
- `.agents/skills/`: Reusable agent skills and development workflows.
- `docs/TASKS.md`: Feature roadmap and backlog.

## Development Commands
- Install: `pip install -r requirements.txt`
- Run service: `uvicorn main:app --reload`
- Run test suite: `pytest`
- Format & lint: standard Python style, type annotations on FastAPI endpoints.

## Product Boundaries
- In Scope: URL validation (http/https), custom aliases, base62 ID encoding, 307 redirects, HTTP error codes (400, 404, 409).
- Out of Scope: No frontend UI/templates, no user authentication or multi-tenancy, no external database engines (stay on SQLite), no distributed caches.
- Reserved Routes: Never route or alias system paths (`docs`, `redoc`, `openapi.json`, `shorten`).

## Change Workflow
1. **Understand**: Read target task in `docs/TASKS.md` and inspect affected routes in `main.py`.
2. **Test First**: Add failing behavioral test in `tests/test_main.py` covering both success and edge/failure cases.
3. **Implement**: Apply the minimal clean code change in `main.py` to satisfy requirements.
4. **Verify**: Run `pytest` twice consecutively to guarantee idempotency and test independence.
