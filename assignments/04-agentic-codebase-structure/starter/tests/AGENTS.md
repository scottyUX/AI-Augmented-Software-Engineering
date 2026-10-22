# Test Instructions (`tests/AGENTS.md`)

## Test Standards for `test_main.py`
When creating or modifying `test_main.py`, adhere to the following rules:
- **Test Client:** Use the public FastAPI API via `TestClient`.
- **Test Coverage:** Cover both success and failure cases comprehensively.
- **Independence:** Keep tests independent of execution order.
- **Behavioral Assertions:** Assert observable behavior rather than internal implementation details.
