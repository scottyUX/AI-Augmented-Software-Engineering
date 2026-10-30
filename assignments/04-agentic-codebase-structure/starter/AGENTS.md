# Agent Guide

This project is a small FastAPI and SQLite link shortener. `POST /shorten` creates
short codes; `GET /{code}` redirects to the stored destination.

## Important files

- `main.py` — routes, request model, and SQLite persistence.
- `test_main.py` — public-API behavior tests.
- `docs/TASKS.md` — the available feature tasks.
- `requirements.txt` — runtime and test dependencies.

## Setup and verification

- Install: `python -m pip install -r requirements.txt`
- Test: `python -m pytest -q`
- Run: `uvicorn main:app --reload` (API docs at `/docs`)

## Product boundaries

Keep this a small URL-shortening API. Changes to link creation, redirects, and their
direct persistence or tests belong here. Do not add a frontend, accounts, analytics,
external services, or a new architecture unless a task explicitly requires them.

## Change workflow

Understand the selected task and relevant code; run the tests; add a behavioral test
that demonstrates the requested behavior; implement the smallest change; rerun the
complete test suite and summarize results and remaining risks.
