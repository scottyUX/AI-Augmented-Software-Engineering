# Stage 1: Planning Session — Custom Alias (Task 1)

## Context & Objectives
Inspect Task 1 from `docs/TASKS.md`:
> "Custom alias — allow `POST /shorten` to accept an optional `alias`; use it as the code if it is available, otherwise return 409."

Repository boundaries from `AGENTS.md` and testing rules from `tests/AGENTS.md` apply.

## Code & System Inspection
1. `main.py`:
   - `ShortenRequest` only accepts `url: str`.
   - `POST /shorten` inserts into SQLite `links` table, fetches `row_id`, computes base62 `encode(row_id)`, and updates the row.
   - `GET /{code}` fetches the redirect URL for the given code.
   - Reserved paths in FastAPI: `/docs`, `/redoc`, `/openapi.json`, and `/shorten`.
2. `tests/test_main.py`:
   - Contains 3 baseline tests verifying shortening, redirection, invalid URL rejection (400), and nonexistent code (404).

## Proposed Plan
1. **Request Schema**:
   Extend `ShortenRequest` to include `alias: str | None = None`.

2. **Validation & Boundaries**:
   - URL validation must remain intact (must start with `http://` or `https://`).
   - If `alias` is supplied:
     - Check against reserved paths (`docs`, `redoc`, `openapi.json`, `shorten`). If matched, reject with HTTP 409 Conflict to avoid shadowing FastAPI application routes.
     - Validate length and character format: 1 to 32 alphanumeric characters, hyphens, or underscores (`^[a-zA-Z0-9_-]{1,32}\Z`). Reject invalid format with HTTP 400 Bad Request.
     - Check for code collisions in `links` table. If already in use, return HTTP 409 Conflict.
     - Use parameterized SQL insertion with SQLite `UNIQUE` constraint safety.

3. **Collision Avoidance for Auto-Generated Codes**:
   When no alias is provided, auto-generate code via `encode(candidate_id)`. If an earlier custom alias claimed that code, retry/advance `candidate_id` so that auto-generation never fails with a 500 error.

4. **Testing Plan (`tests/test_main.py`)**:
   - Success path: shortening with a custom alias and following redirect.
   - Conflict path: attempting to reuse an existing alias returns HTTP 409.
   - Reserved path: attempting to use reserved names returns HTTP 409.
   - Format validation: invalid characters, spaces, or excessive lengths return HTTP 400.
   - Collision safety: auto-generation cleanly skips taken alias codes.
   - Independence: use dynamic UUID-based aliases so tests do not pollute persistent SQLite state.
