# Week 7 — Agent Orchestration: The Recipe Box Sprint

## Overview
One agent is useful; orchestrated agents are a workflow. This week you'll run
**multiple agents concurrently** and implement explicit orchestration patterns from
lecture — the **generator–critic loop** plus one more — on a small app.

**New domain:** a **Recipe Box** app (save recipes, tag them, generate shopping lists).

> **Coding agent — IDE-agnostic.** Use whatever supports running more than one agent at
> once. **Google Antigravity's Agent Manager** (default) can drive multiple agents in
> parallel; other good options include **Warp** (multi-tab agents), or several sessions
> of a CLI agent. Isolate concurrent work with **git worktrees** so agents don't collide.

## Learning goals
- Coordinate multiple agents working concurrently without clobbering each other.
- Implement the **generator–critic loop** and one of: the **goal pattern**, the
  **Ralph loop**, or a **subagent** split.
- Reason about concurrency wins, risks, and coordination strategies.

---

## Learn about orchestration
- **git worktrees** (isolate parallel agents): https://git-scm.com/docs/git-worktree
- Your agent's multi-agent feature (Antigravity Agent Manager, Warp multi-tab, etc.).
- Lecture patterns: generator–critic loop, the goal pattern, the Ralph loop, subagents.

## The starter app (build a minimal one)
Create `recipe-box/` — a small full-stack app (backend + static frontend + tests) with
recipes and tags. Add a `docs/TASKS.md` with several **independent** tasks so agents can
run in parallel, e.g.: shopping-list generator, tag filtering, ingredient scaling,
import-from-URL, a favorites view, and a test-coverage pass.

## Part I — Reusable automation (required: at least one)
Create one or more reusable, shareable automations for this repo using your agent or
terminal — e.g. Antigravity workflows, Warp Drive prompts/rules, saved agent commands,
or a `Makefile` + MCP integration. Examples: a test runner with flaky-retry, docs-sync
from the OpenAPI schema, a refactor harness, or a Git MCP integration so an agent can
branch/commit autonomously.

## Part II — Multi-agent, concurrent (required)
Run **separate agents concurrently** on independent `TASKS.md` items — different
Antigravity agents, Warp tabs, or CLI sessions. Use **git worktrees** so they don't
collide. Push the concurrency: how many agents can you keep productive at once?

## Part III — Implement orchestration patterns (required: 2)
Implement **at least two** patterns from lecture and document them:
1. **Generator–critic loop (required):** one agent generates a solution for a task,
   a second agent critiques it against a rubric, and the generator revises — loop until
   the critic signs off. Show at least two revision rounds.
2. **One more** of your choice:
   - **Goal pattern** — give an agent a high-level goal and let it decompose and drive
     to completion.
   - **Ralph loop** — an agent that repeatedly runs → checks output → fixes until a
     stopping condition is met (e.g., all tests green).
   - **Subagent split** — planner/implementer/reviewer roles on one task.

## Deliverables
**Submit the GitHub repository link** for `recipe-box/`, plus a `writeup.md` containing:
- Your reusable automation(s): goals, inputs/outputs, steps; share links or exported
  definitions, and which tool/feature you used.
- Multi-agent notes: roles, worktree strategy, how many agents ran concurrently, and
  wins/risks/failures observed.
- Your **generator–critic** transcript (with the revision rounds) and your second
  pattern, each explained.
- Autonomy levels used per task (which permissions, why, how you supervised).
- Before vs. after: manual workflow vs. orchestrated workflow.
- **What you learned:** 3–5 sentences on orchestration (and one line per pattern on what
  it did well or badly).

## Evaluation (100 pts)
- 25 — Reusable automation(s) that meaningfully help the repo.
- 30 — Genuine concurrent multi-agent execution via worktrees, with reflection.
- 30 — Two orchestration patterns implemented and evidenced (generator–critic + one).
- 15 — Clear `writeup.md` with transcripts, honest analysis, and the "what you learned"
  reflection.
