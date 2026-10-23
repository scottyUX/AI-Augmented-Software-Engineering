# Test rules (apply to files under `tests/`)

- **Public API only.** Drive the app through `fastapi.testclient.TestClient` and HTTP
  requests. Don't call internal helpers (`encode`, `get_db`) or query SQLite directly to
  check results — assert on status codes and JSON bodies.
- **Success and failure.** Every feature gets at least one happy-path test and at least one
  failure or edge case (unknown code, bad input, boundary value).
- **Independent.** Each test creates its own data and must pass alone, in any order, and
  when run twice. Use the `client` fixture from `tests/conftest.py`; it gives every test a
  fresh temporary database. Never depend on IDs or codes created by another test.
- **Behavior, not implementation.** Assert what a user of the API observes
  (e.g. `clicks == 2`), not how it is stored (column names, SQL).
- **Redirects.** Use `follow_redirects=False` so the test checks our 307, not the target site.
- **Names** describe behavior: `test_stats_counts_each_redirect`, not `test_stats_2`.
- Run with `pytest -q`. Don't edit `../test_main.py` to make new code pass.
