# Week 5 — Structuring a Repo for Agents: The Link Shortener

## Overview
A codebase that an agent works in well looks different from one built only for humans.
This week you'll take a small app and make it **agent-native**: encode its rules,
workflows, and guardrails so a coding agent can operate safely and repeatably —
reusable agent commands/workflows, **agent context/rules files**, a **hook** that gates
lint/tests, and role-specialized **subagents**.

**New domain:** a **URL shortener** service (not a notes/action-item app).

> **Coding agent — IDE-agnostic.** Use whichever agent you set up in Week 1
> (**Google Antigravity** by default; Cursor, Copilot, or any other is fine). The
> concepts below — context/rules files, reusable workflows, hooks, subagents — exist in
> every modern agent under different names. Where a file or menu is named, map it to
> your agent's equivalent and note the mapping in your writeup.

## Learning goals
- Use skills, rules, and guardrails to shape agent behavior.
- Author agent **context/rules files** (the cross-tool `AGENTS.md`, plus your agent's
  own format) and an `intent.md`.
- Wire a **hook** for lint gates and test runs.
- Apply the **planner / implementer / reviewer** subagent pattern.

---

## Learn about agent configuration
- **AGENTS.md** — the cross-tool standard many agents (including Antigravity) read for
  repo guidance: https://agents.md/
- Your agent's own docs for **rules/workspace context**, **saved commands/workflows**,
  **hooks**, and **subagents/multiple agents**. Examples:
  - Google Antigravity docs (agent rules, workflows, Agent Manager).
  - Cursor rules (`.cursor/rules`), Claude Code (`CLAUDE.md`, `.claude/`), etc.

## The starter app (build a minimal one)
Create `link-shortener/` — a small full-stack app you can extend:
- Backend: a tiny API (FastAPI **or** Express) with `POST /shorten` (url → short code)
  and `GET /{code}` (redirect), storage in SQLite or a JSON file.
- A couple of `pytest`/`jest` tests and a formatter/linter (black+ruff, or eslint+prettier).
- A `docs/TASKS.md` listing 4–5 improvement tasks (custom alias, click counter,
  expiry, basic validation, rate limiting).

Keep it deliberately small — it's a playground for the automations, not the deliverable.

## Part I — Make the repo agent-native (build 3+ artifacts, at least one hook)

### A) Reusable agent workflows / commands
Create at least two reusable, repeatable workflows for this repo — using your agent's
mechanism for saved commands/workflows (e.g. Antigravity workflows, Cursor/Claude
commands). If your agent has no such feature, capture them as parameterized prompts in
`docs/PLAYBOOKS.md`. Examples:
- **Test runner** — run the suite, and on green run coverage; summarize failures.
- **New endpoint** — scaffold a route with a **failing test first**, then implement,
  then run lint/format.

### B) Agent context / rules files
Author an `AGENTS.md` (and your agent's native rules file, if different) covering: how to
run the app, where routes/tests/storage live, tooling expectations, safe vs. forbidden
commands, and a workflow snippet (e.g. "for a new endpoint: failing test → implement →
run hooks"). Add an `intent.md` describing the project's purpose and constraints, and
note in your writeup how these files differ in role.

### C) A hook (required)
Add a hook that runs **lint/format and tests** at a sensible gate and **blocks** on
failure. Use a **git `pre-commit` hook** (tool-agnostic) or your agent's hook mechanism.
Show it catching a bad change.

### D) Subagents (planner / implementer / reviewer)
Use role-specialized agents to complete one `TASKS.md` item: a **planner** drafts the
approach, an **implementer** writes code + tests, a **reviewer** checks correctness and
style before you accept. Use your agent's subagent/multi-agent feature, or run the three
roles as separate agent sessions.

## Part II — Use your automations
Complete **at least two** `TASKS.md` items *through* your workflows and subagents.

## Deliverables
**Submit the GitHub repository link** for `link-shortener/`, with the agent config
(`AGENTS.md`, `intent.md`, hook, workflows/rules) committed, and a `writeup.md`:
- Each automation: purpose, inputs/outputs, and steps — and which agent feature you
  mapped it to.
- Your hook config and a screenshot of it blocking a failing change.
- The subagent roles and a transcript of them completing a task together.
- Before vs. after: the manual workflow vs. the agent-driven one.
- **What you learned:** 3–5 sentences on what structuring a repo for agents taught you
  (and one line per Part I item on what that specific artifact changed).

## Evaluation (100 pts)
- 40 — Three+ agent-native artifacts built correctly, **including a working hook**.
- 25 — Subagent (planner/implementer/reviewer) pattern used on a real task.
- 20 — Two+ `TASKS.md` items completed via the automations.
- 15 — Clear `writeup.md` with evidence (configs, screenshots, transcripts) and the
  "what you learned" reflection.
