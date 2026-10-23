# Test rules (apply only to files in `tests/`)

- Test through the **public HTTP API** with `TestClient` (`client.post`, `client.get`).
  Do not call private helpers or query `links.db` directly in tests.
- Every feature needs at least one **success** test and one **failure or edge-case** test
  (e.g. 400, 404, 409, 410).
- Tests must be **independent**: no test may rely on another test running first or on
  data already in `links.db`. Create the data a test needs inside that test, and use
  unique values (e.g. `uuid.uuid4().hex[:8]`) for anything that must not collide, such as aliases.
- Assert **behavior**: status codes, JSON fields, and redirect `location` headers —
  not internal details like row ids or exact generated codes.
- Use `follow_redirects=False` when checking redirects.
- One behavior per test, with a descriptive name (`test_alias_already_taken_returns_409`).
