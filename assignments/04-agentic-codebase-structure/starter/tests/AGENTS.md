# Testing Guidance (`tests/`)

Applies exclusively to files located within `tests/`.

## Core Testing Principles
1. **Public API Testing**: Exercise endpoints exclusively through FastAPI's `TestClient(app)`. Never inspect or mock internal helper functions directly.
2. **Symmetric Coverage**: Every new feature or endpoint change must include tests for both valid success paths (200/307) and invalid/failure edge cases (400, 404, 409).
3. **Execution Independence**:
   - Tests must run independently in any order without relying on state from preceding tests.
   - For custom aliases or specific codes, generate dynamic names (e.g. `uuid.uuid4().hex[:8]`) to avoid collision with persistent records in `links.db`.
   - For tests modifying database state directly or testing collision logic, use temporary isolated databases via pytest `tmp_path` and `monkeypatch`.
4. **Behavioral Assertions**: Assert on HTTP status codes, response headers (e.g., `Location` header on redirects), and response JSON schemas. Avoid asserting on private database row IDs.
