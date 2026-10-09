# Starter — Link Shortener

A tiny FastAPI + SQLite service you'll make *agent-native*. You don't build the app —
you add `AGENTS.md`, a hook, a reusable workflow, and use subagents on one task.

## Setup
```bash
pip install -r requirements.txt
pytest                      # 3 tests should pass
uvicorn main:app --reload   # http://localhost:8000  (docs at /docs)
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
- `test_main.py` — pytest suite
- `docs/TASKS.md` — pick one task for the subagent exercise
