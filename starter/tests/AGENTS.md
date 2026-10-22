# Scoped Testing Guidance

When writing or modifying tests in this repository:

1. **Public API Testing:** Test routes strictly through `fastapi.testclient.TestClient`. Do not call internal helper functions (`encode`, `init_db`) directly.
2. **Symmetrical Coverage:** Every endpoint change must include tests for both success cases (2xx) and failure edge cases (4xx status codes).
3. **Test Independence:** Each test must be completely isolated and pass independently regardless of execution order.
4. **Behavioral Assertions:** Assert on HTTP status codes, location headers, and JSON body structure rather than internal database representations.