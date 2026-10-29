# Test-Specific Agent Instructions

These instructions apply only to files inside the `tests/` directory.

## Testing Guidelines

- Test application behavior through FastAPI's public HTTP endpoints using `TestClient`.
- Cover successful requests and at least one failure or edge case for every new feature.
- Keep tests independent of execution order.
- Assert HTTP status codes, response bodies, and relevant headers.
- Avoid testing private implementation details.
- Preserve existing test coverage.
- Run the complete test suite after making changes.

## Verification

Run tests from the `starter/` directory:

```bash
python -m pytest -q
```

All existing and newly added tests must pass before submitting a change.