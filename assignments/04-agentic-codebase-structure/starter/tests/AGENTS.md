# Testing Instructions — Scoped Guidance for `tests/`

These rules apply when writing, modifying, or reviewing tests in `tests/`.

## Core Principles

1. **Test Through Public API Only:**
   - Exercise endpoints exclusively via FastAPI's `TestClient(app)`.
   - Never import internal helper functions to verify internal state directly; verify through HTTP requests and responses.

2. **Symmetric Success & Failure Coverage:**
   - Every route and feature must have tests for happy paths (e.g., 200 OK, 307 Temporary Redirect).
   - Test explicit failure conditions and boundaries (e.g., 400 Bad Request, 404 Not Found, 409 Conflict).

3. **Execution Independence:**
   - Tests must run independently and in any order.
   - Do not rely on hardcoded shared alias names across test runs if `links.db` persists; generate unique aliases per test (e.g., using `uuid` or distinct suffixes) or test with temporary isolated databases.
   - The entire test suite must pass cleanly when executed repeatedly (`pytest` run twice in succession).

4. **Behavioral Assertions:**
   - Assert on status codes, headers (e.g., `Location` on redirects), and response JSON bodies.
   - Do not assert on private database row IDs or implementation trivia.
