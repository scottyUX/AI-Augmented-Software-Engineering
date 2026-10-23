# Starter — Link Shortener

A tiny FastAPI + SQLite service that you will make easier for a coding agent to understand and modify. The application already works; you will add repository guidance, one scoped instruction, one reusable workflow, and complete one feature.

## Setup

```bash
pip install -r requirements.txt
pytest                       # 3 tests should pass
uvicorn main:app --reload    # http://localhost:8000  (docs at /docs)
```

## Try it

```bash
curl -X POST localhost:8000/shorten -H 'Content-Type: application/json' \
  -d '{"url":"https://example.com"}'
# -> {"code":"c","short_url":"/c"}  then GET localhost:8000/<code> redirects
```

> **Windows (PowerShell):** `curl` is an alias for `Invoke-WebRequest` there, so the
> command above fails. Use this instead (works in PowerShell 5.1 and 7):
> ```powershell
> Invoke-RestMethod -Method Post -Uri http://localhost:8000/shorten `
>   -ContentType 'application/json' -Body '{"url":"https://example.com"}'
> ```

> **Why isn't my code `c`?** Codes are the base62 row id, and the tests and the server
> share the same `links.db`. Each `pytest` run and each `/shorten` call adds rows, so your
> code depends on what's already in the database. Delete `links.db` to start from
> scratch (it is gitignored).

## Files

- `main.py` — the app (`POST /shorten`, `GET /{code}`)
- `test_main.py` — the existing pytest suite
- `docs/TASKS.md` — choose one feature to implement

Start by running the existing tests, then read all three files before adding agent guidance.
