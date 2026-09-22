# Week 7 — Agent Orchestration: The Recipe Box Sprint

## Overview
One agent is useful; orchestrated agents are a workflow. This week you'll run
**multiple agents concurrently** and implement explicit orchestration patterns using
the **[Warp](https://www.warp.dev/) agentic development environment** — Warp Drive
automations plus multi-agent tabs. You'll also implement a **generator–critic loop**
and one additional pattern from lecture.

**New domain:** a **Recipe Box** app (save recipes, tag them, generate shopping lists)
— not the reference's productivity app.

## Learning goals
- Coordinate multiple agents working concurrently without clobbering each other.
- Implement the **generator–critic loop** and one of: the **goal pattern**, the
  **Ralph loop**, or a **subagent** split.
- Reason about concurrency wins, risks, and coordination strategies.

---

## Learn about Warp
- Warp: https://www.warp.dev/
- Warp University: https://www.warp.dev/university

## The starter app (build a minimal one)
Create `recipe-box/` — a small full-stack app (backend + static frontend + tests) with
recipes and tags. Add a `docs/TASKS.md` with several **independent** tasks so agents
can run in parallel, e.g.: shopping-list generator, tag filtering, ingredient scaling,
import-from-URL, a favorites view, and a test-coverage pass.

## Part I — Warp Drive automation (required: at least one)
Create one or more shareable Warp Drive prompts / rules / MCP integrations for this
repo. Examples: test runner with flaky-retry, docs-sync from the OpenAPI schema, a
refactor harness, or a Git MCP integration so Warp can branch/commit autonomously.

## Part II — Multi-agent, concurrent (required)
Run **separate agents in separate Warp tabs** on independent `TASKS.md` items at the
same time. Use **[git worktrees](https://git-scm.com/docs/git-worktree)** so agents
don't collide. Push the concurrency: how many agents can you keep productive at once?

## Part III — Implement an orchestration pattern (required)
Beyond raw concurrency, implement **at least two** patterns from lecture and document them:
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
Push `recipe-box/` and a `writeup.md` containing:
- Your Warp Drive automation(s): goals, inputs/outputs, steps; share links or exported
  definitions.
- Multi-agent notes: roles, worktree strategy, how many agents ran concurrently, and
  wins/risks/failures observed.
- Your **generator–critic** transcript (with the revision rounds) and your second
  pattern, each explained.
- Autonomy levels used per task (which permissions, why, how you supervised).
- Before vs. after: manual workflow vs. orchestrated workflow.

## Evaluation (100 pts)
- 25 — Warp Drive automation(s) that meaningfully help the repo.
- 30 — Genuine concurrent multi-agent execution via worktrees, with reflection.
- 30 — Two orchestration patterns implemented and evidenced (generator–critic + one).
- 15 — Clear `writeup.md` with transcripts and honest analysis.
