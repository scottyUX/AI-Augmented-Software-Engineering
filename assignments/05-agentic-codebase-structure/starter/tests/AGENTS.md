# Scoped Agent Instructions — `tests/` Directory

> **Scope**: These instructions apply specifically to test files inside `tests/` (as well as `test_main.py` when working on the test suite). They supplement the root `AGENTS.md`.

## Core Testing Principles

1. **Test Through the Public API Only**
   - Always interact with the application through HTTP endpoints (`POST /shorten`, `GET /{code}`, `GET /stats/{code}`) using FastAPI's `TestClient(app)`.
   - Do **not** call internal helper functions (such as `encode()`, `get_db()`, or `init_db()`) or query SQLite tables directly to assert feature behavior.

2. **Cover Both Success and Failure Cases**
   - Every feature or endpoint must have tests for both the **happy path** (e.g., `200 OK`, `307 Temporary Redirect`) and **error conditions** (e.g., `400 Bad Request` for invalid URLs, `404 Not Found` for unknown codes, `409 Conflict` for duplicate aliases, `410 Gone` for expired links).
   - Assert both the HTTP status code and the relevant response payload or headers (such as `r.json()` fields or `r.headers["location"]`).

3. **Guarantee Test Independence**
   - Tests must be completely self-contained and able to run in any order or in isolation (`pytest -k <test_name>`).
   - Never rely on state, row IDs, or short codes created by a previous test function.
   - When testing custom aliases or state-sensitive routes, use unique aliases per test (or isolate/reset the database state via a fixture) so repeated test runs remain idempotent.

4. **Focus on Observable Behavior, Not Internal Implementation**
   - Assert **what** the service returns (HTTP status codes, JSON structure, redirect behavior), not **how** `main.py` stores or computes values internally.
   - Tests should remain valid even if the internal SQLite schema or encoding logic is refactored, provided the external HTTP contract does not change.

