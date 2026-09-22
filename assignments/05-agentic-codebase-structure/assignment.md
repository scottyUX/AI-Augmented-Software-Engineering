# Week 5 — Structuring a Repo for Agents: The Link Shortener

## Overview
A codebase that an agent works in well looks different from one built only for humans.
This week you'll take a small app and make it **agent-native**: encode its rules,
workflows, and guardrails so a coding agent can operate safely and repeatably. You'll
build automations with **Claude Code** — custom slash commands, `CLAUDE.md` guidance,
role-specialized **subagents**, and a **hook** that gates lint/tests.

**New domain:** a **URL shortener** service (not a notes/action-item app).

## Learning goals
- Use skills, rules, and guardrails to shape agent behavior.
- Author `CLAUDE.md` (and try `AGENTS.md` / an `intent.md`) as living context files.
- Wire **hooks** for lint gates and test runs.
- Apply the **planner / implementer / reviewer** subagent pattern.

---

## Learn about Claude Code
- Best practices: https://www.anthropic.com/engineering/claude-code-best-practices
- Subagents: https://docs.anthropic.com/en/docs/claude-code/sub-agents
- Hooks: https://docs.anthropic.com/en/docs/claude-code/hooks

## The starter app (build a minimal one)
Create `link-shortener/` — a small full-stack app you can extend:
- Backend: a tiny API (FastAPI **or** Express) with `POST /shorten` (url → short code)
  and `GET /{code}` (redirect), storage in SQLite or a JSON file.
- A couple of `pytest`/`jest` tests and a formatter/linter (black+ruff, or eslint+prettier).
- A `docs/TASKS.md` listing 4–5 improvement tasks (custom alias, click counter,
  expiry, basic validation, rate limiting).

Keep it deliberately small — it's a playground for the automations, not the deliverable.

## Part I — Make the repo agent-native (build 3+ artifacts, at least one hook)

### A) Custom slash commands (`.claude/commands/*.md`)
Create at least two reusable workflows, e.g.:
- `test.md` — run the test suite, and on green run coverage; summarize failures.
- `new-endpoint.md` — scaffold a route with a **failing test first**, then implement,
  then run lint/format (accepts `$ARGUMENTS`).

### B) `CLAUDE.md` guidance
Author a root `CLAUDE.md` covering: how to run the app, where routes/tests/storage
live, tooling expectations, safe vs. forbidden commands, and a workflow snippet
(e.g. "for a new endpoint: failing test → implement → run hooks"). Optionally add an
`AGENTS.md` and/or an `intent.md` and note how they differ in your writeup.

### C) A hook (required)
Add a hook (`.claude/settings.json`) that runs **lint/format and tests** at a sensible
gate (e.g. before commit or after edits) and **blocks** on failure. Show it catching a
bad change.

### D) Subagents (planner / implementer / reviewer)
Define role-specialized subagents and use them together to complete one `TASKS.md`
item: planner drafts the approach, implementer writes code + tests, reviewer checks
correctness and style before you accept.

## Part II — Use your automations
Complete **at least two** `TASKS.md` items *through* your automations and subagents.

## Deliverables
Push `link-shortener/` with `.claude/` committed, and a `writeup.md`:
- Each automation: purpose, inputs/outputs, and steps.
- Your hook config and a screenshot of it blocking a failing change.
- The subagent roles and a transcript of them completing a task together.
- Before vs. after: the manual workflow vs. the agent-driven one.

## Evaluation (100 pts)
- 40 — Three+ automations built correctly, **including a working hook**.
- 25 — Subagent (planner/implementer/reviewer) pattern used on a real task.
- 20 — Two+ `TASKS.md` items completed via the automations.
- 15 — Clear `writeup.md` with evidence (configs, screenshots, transcripts).
