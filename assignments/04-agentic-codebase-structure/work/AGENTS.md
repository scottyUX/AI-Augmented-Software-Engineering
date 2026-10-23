# AGENTS.md — Link Shortener

## What this is
A tiny URL shortener: FastAPI + SQLite, one app file. `POST /shorten` stores a URL and
returns a base62 code; `GET /{code}` redirects (307) to it; `GET /stats/{code}` reports
the visit count.

## Map
| Path | Purpose |
|---|---|
| `main.py` | Whole app: DB setup (`init_db`), `encode`, routes |
| `test_main.py` | Original smoke tests — keep them passing, don't rewrite them |
| `tests/` | New behavioral tests (see `tests/AGENTS.md` for test rules) |
| `docs/TASKS.md` | Feature backlog |
| `links.db` | Local SQLite file, created at import time — never commit it |
| `.agents/skills/implement-feature/` | Reusable workflow for adding a feature |

## Commands
```bash
pip install -r requirements.txt
pytest -q                     # must be green before and after every change
uvicorn main:app --reload     # http://localhost:8000/docs
```

## Product boundaries
In scope: shortening `http(s)` URLs, redirecting, and the small features in `docs/TASKS.md`.
Out of scope — do not add without asking: user accounts/auth, a web UI, analytics
beyond a simple counter, external services, new frameworks, an ORM, or a second database.

## Conventions
- Keep everything in `main.py` unless it grows past ~200 lines.
- Use parameterized SQL (`?` placeholders) only. Never build SQL with f-strings.
- Schema changes must also work on an existing `links.db` (use a guarded `ALTER TABLE`).
- Errors use `HTTPException` with a clear `detail`; status codes: 400 bad input,
  404 unknown code, 409 conflict, 410 gone.
- Don't add dependencies to `requirements.txt` without asking.

## Change workflow
1. **Understand** — read the task, `main.py`, and the related tests. State the expected
   behavior and the files you will touch.
2. **Test** — write a failing behavioral test first (success + at least one failure case).
3. **Implement** — the smallest change that makes it pass. No unrelated refactors.
4. **Verify** — run `pytest -q`; all old and new tests pass. Summarize what changed and any risks.
