# AGENTS.md — Link Shortener

## What this is
A tiny FastAPI + SQLite service that turns long URLs into short codes.
- `POST /shorten` with `{"url": "https://..."}` → `{"code": "b", "short_url": "/b"}`
- `GET /{code}` → 307 redirect to the stored URL, or 404 for an unknown code

## Where things are
- `main.py` — the whole app: DB setup (`get_db`, `init_db`), base62 `encode`, request models, routes
- `tests/` — pytest suite (see `tests/AGENTS.md` for test rules)
- `docs/TASKS.md` — the feature backlog; implement only the task you were asked for
- `links.db` — local SQLite file created at startup; never commit it
- `.agents/skills/implement-feature/` — the workflow to follow when adding a feature

## Commands (run from this folder)
```bash
pip install -r requirements.txt
pytest                         # all tests must pass before and after a change
uvicorn main:app --reload      # http://localhost:8000, docs at /docs
```

## Product boundaries
In scope: creating short links, redirecting, and the small features listed in `docs/TASKS.md`.
Out of scope — do not add without being asked:
- user accounts, auth, or an admin UI
- a different database, an ORM, migrations, or background jobs
- new third-party dependencies (stick to what is in `requirements.txt`)
- splitting `main.py` into packages or other architecture changes

## Conventions
- Keep it one small file: new endpoints and helpers go in `main.py`.
- Use parameterized SQL (`?` placeholders), never string formatting.
- Use `HTTPException` with the right status code and a short `detail` message.
- Schema changes go in `init_db()` and must not break existing rows.

## Change workflow
1. **Understand** — read the task, `main.py`, and the related tests.
2. **Test** — add a failing behavioral test for the new behavior first.
3. **Implement** — make the smallest change in `main.py` that passes it.
4. **Verify** — run `pytest`; all old and new tests must pass. Summarize what changed.
