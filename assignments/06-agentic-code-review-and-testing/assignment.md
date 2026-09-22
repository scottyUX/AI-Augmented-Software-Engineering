# Week 6 — AI Code Review & Testing: The Habit Tracker

## Overview
This week combines the two halves of trustworthy agentic development: **deterministic
guardrails** (tests, lint, types) and **LLM-based review**. You'll implement features
on a small codebase, back them with tests, open pull requests, and run an **AI code
reviewer ([Graphite](https://graphite.dev/) Diamond)** — then compare the AI's review
to your own manual, line-by-line review.

**New domain:** a **habit tracker** API (not the reference's notes app).

## Learning goals
- Set up deterministic guardrails as a first line of defense.
- Practice agent-driven implementation with disciplined human review.
- Compare human vs. AI code review and develop heuristics for trusting AI reviews.

---

## Get started with Graphite
1. Sign up: https://app.graphite.dev/signup (claim the free trial; students can use
   the education program afterward).
2. Install the Graphite CLI / GitHub app so Diamond can review your PRs.

## The starter app (build a minimal one)
Create `habit-tracker/` — a small API (FastAPI or Express + SQLite) with `habits` and
`check-ins`, minimal tests, and a linter/formatter configured. Add a `docs/TASKS.md`
with **four** tasks, e.g.:
1. `GET /habits/{id}/streak` — compute the current daily streak.
2. Input validation + proper error responses on `POST /habits`.
3. A weekly-summary endpoint (check-ins per habit for the last 7 days).
4. Pagination on `GET /habits`.

## Part I — Guardrails first
Before implementing tasks, make the guardrails real:
- A test command that fails the build on any failing test.
- Lint + format configured (black+ruff or eslint+prettier).
- (Recommended) type checking (mypy or TypeScript).
Document the commands in the README.

## Part II — Implement, review, compare
For **each** of the four tasks:
1. Create a separate branch.
2. Implement it with your AI coding tool using a **one-shot prompt**; then add/update tests.
3. **Manually review** the diff line-by-line. Note issues (correctness, performance,
   security, naming, test gaps, API shape, UX, docs) and fix them.
4. Open a **PR** including: problem description + approach, testing performed (commands
   + results), and notable tradeoffs/limitations.
5. Run **Graphite Diamond** to generate an AI review on the PR.

## Deliverables
Push `habit-tracker/` and a `writeup.md` containing:
- **Four PRs**, one per task, each with a clear description, commit links, and visible
  Graphite Diamond AI comments.
- Your guardrail setup (commands + what they catch).
- A reflection:
  - The kinds of comments you typically made in **your** manual reviews.
  - **Your** comments vs. **Graphite's** for each PR — where the AI was better/worse,
    with specific examples.
  - Your comfort trusting AI reviews going forward, and heuristics for when to rely on them.

## Evaluation (100 pts)
- 20 per task (×4 = 80): correctness/completeness, code quality + tests, depth of your
  manual review notes, and the Diamond AI review present.
- 20 — Reflection: insightful human-vs-AI comparison and honest calibration.
