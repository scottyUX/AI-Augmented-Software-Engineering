# Agent Guide — Link Shortener

## Project Overview

This repository contains a small URL-shortening service built with FastAPI and SQLite. Users can create short links and follow them to their original destinations.

Keep the application lightweight and easy to understand. Do not introduce unnecessary frameworks, services, or architectural complexity.

## Repository Structure

- `main.py` — FastAPI application, SQLite operations, and URL shortening logic.
- `test_main.py` — Existing behavioral tests using FastAPI TestClient.
- `docs/TASKS.md` — Available feature requirements.
- `README.md` — Installation and usage instructions.
- `requirements.txt` — Python dependencies.

## Setup and Commands

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn main:app --reload
```

Run tests:

```bash
python -m pytest -q
```

## Product Boundaries

- Keep the service focused on creating and resolving shortened URLs.
- Use the existing FastAPI and SQLite architecture.
- Preserve existing endpoint behavior unless a selected task requires changes.
- Do not introduce external databases, authentication, or unrelated features.
- Make small, focused changes with meaningful tests.

## Change Workflow

1. **Understand:** Read the selected task and inspect relevant application code.
2. **Test:** Identify expected success and failure behavior; add a failing behavioral test.
3. **Implement:** Make the smallest change necessary to satisfy the task.
4. **Verify:** Run all tests and confirm existing functionality still works.
5. **Review:** Summarize the changes, test results, and remaining risks.