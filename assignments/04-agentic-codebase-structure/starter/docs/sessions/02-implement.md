# Stage 2: Implementation Session — Reusable Workflow Execution

## Workflow Invocation
Invoked reusable workflow `.agents/skills/implement-feature/SKILL.md`.

## Execution Log

### Steps 1 & 2: Review Guidance & Inspect Existing Assets
- Reviewed `AGENTS.md` boundaries (no new dependencies, protect reserved routes, preserve response shapes).
- Reviewed `tests/AGENTS.md` (exercise through public API `TestClient`, execution independence, behavioral assertions).
- Confirmed `main.py` routes and SQLite schema.

### Step 3: State Expected Behavior & Affected Files
- **Files Modified**: `main.py`, `tests/test_main.py`.
- **Contracts**:
  - `POST /shorten` with `{"url": "...", "alias": "my-alias"}` returns 200 `{"code": "my-alias", "short_url": "/my-alias"}`.
  - Duplicate alias returns 409 Conflict.
  - Reserved alias returns 409 Conflict.
  - Invalid format (spaces, slashes, punctuation, length > 32 or empty) returns 400 Bad Request.
  - Auto-generated requests continue to return 200 without regression.

### Step 4: Add Failing Behavioral Tests
Added 5 new test cases to `tests/test_main.py`:
- `test_custom_alias_success`
- `test_custom_alias_conflict_409`
- `test_custom_alias_reserved_name_409`
- `test_custom_alias_invalid_characters_400`
- `test_auto_generated_code_avoids_alias_collision`

Ran initial pytest verification:
- 3 original tests passed.
- 5 new tests failed as expected (e.g. `AssertionError: assert 200 == 409`).

### Step 5: Implement Minimal Change
- Updated `ShortenRequest` in `main.py` with `alias: str | None = None`.
- Added `RESERVED_CODES` and `ALIAS_PATTERN`.
- Prioritized reserved route rejection (409) and regex validation (400).
- Handled SQLite unique conflicts gracefully via 409 Conflict.
- Added candidate advance loop for auto-generated codes to prevent collisions with user-specified custom aliases.

### Step 6: Verify Suite
- Executed `pytest`: All 8 tests passed in 0.54s.
- Executed second consecutive `pytest`: All 8 tests passed in 0.53s, confirming idempotency and test independence.

### Step 7: Summary & Remaining Risks
- Implementation satisfies all specifications without new external dependencies.
- Parameterized SQL prevents injection vulnerabilities.
- Backward compatibility preserved for all original endpoints.
