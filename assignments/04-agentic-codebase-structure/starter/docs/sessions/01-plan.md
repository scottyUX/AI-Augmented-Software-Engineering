# Stage 1: Planning Session — Custom Alias Feature

**Objective:** Inspect Task 1 ("Custom alias") and propose a complete implementation plan without editing any code.

---

## Agent Prompt
> "Please inspect `docs/TASKS.md` Task 1 ('Custom alias'), `main.py`, and `tests/test_main.py`. Do not modify any files. Propose a structured plan covering data model changes, validation rules, collision edge cases, reserved routes, and test strategy."

---

## Agent Proposal & Findings

### 1. Requirements Breakdown
Task 1 states: *"Custom alias — allow `POST /shorten` to accept an optional `alias`; use it as the code if it is available, otherwise return 409."*

### 2. Identified Edge Cases & Architectural Risks
1. **Reserved Route Collisions:** FastAPI serves `/docs`, `/redoc`, and `/openapi.json`, and defines `/shorten`. If a client creates an alias named `docs` or `shorten`, the catch-all redirect route `GET /{code}` would shadow or conflict with built-in service endpoints.
   - *Plan:* Define a `RESERVED_ROUTES` set (`{"docs", "redoc", "openapi.json", "shorten"}`) and reject them with HTTP 409 Conflict.
2. **Auto-Generation Collision:** If a custom alias matches a code that would later be produced by `encode(n)` (e.g. alias `"b"` matches row 2), subsequent automatic shortenings would trigger a SQLite UNIQUE constraint error (`500 Internal Server Error`).
   - *Plan:* The auto-generation sequence must verify whether the computed base62 code is already in use, incrementing to the next available code if a collision occurs.
3. **Alias Input Validation:** An alias must not contain path separators (`/`), query characters (`?`), hashes (`#`), or whitespace.
   - *Plan:* Enforce regex `^[A-Za-z0-9_-]{1,32}\Z`. Invalid formats return HTTP 400 Bad Request.
4. **Execution Independence in Tests:** Hardcoded aliases in tests would collide across test runs because SQLite persists data in `links.db`.
   - *Plan:* Use `uuid.uuid4().hex[:8]` for alias generation in tests, and use `tmp_path` + `monkeypatch` for collision simulation.

### 3. Proposed File Changes
- `main.py`: Update `ShortenRequest` schema, add validation and collision checks in `shorten()`.
- `tests/test_main.py`: Add test cases for success, duplicate conflict (409), reserved names (409), bad characters (400), and auto-generation collision avoidance.

---

## Conclusion
Plan approved. Proceeding to Stage 2 (Implementation).
