---
description: "Behavioral testing guidance for the link shortener's root test_main.py."
applyTo: "test_main.py"
---

# Link shortener test guidance

- Exercise the service through its FastAPI public routes with `TestClient`.
- Cover successful behavior and relevant failures or edge cases.
- Assert observable status codes, response data, and headers, not private helpers or
  SQLite implementation details.
- Keep each test independent of test order; use unique aliases or isolated data.
- Run the complete suite with `python -m pytest -q`.
