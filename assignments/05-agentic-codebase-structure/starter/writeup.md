# Week 4 Writeup — Structuring a Repo for Agents: The Link Shortener

## 1. Root Context (`AGENTS.md`)
In the root `AGENTS.md` (53 lines), I documented five essential pillars for the FastAPI + SQLite Link Shortener: a brief overview of the URL shortening and Base62 redirection flow, exact locations of core files (`main.py`, `test_main.py`, `tests/AGENTS.md`, `docs/TASKS.md`, `requirements.txt`), copy-pasteable commands for setup (`pip install -r requirements.txt`), testing (`pytest`), and local execution (`uvicorn main:app --reload`), explicit product boundaries, and the mandatory `understand -> test -> implement -> verify` workflow. Defining what does *not* belong in the service (no authentication, ORMs, external databases, or frontend build pipelines) prevents the agent from over-engineering or introducing unrequested dependencies, while keeping the file under 60 lines preserves context window efficiency.

## 2. Scoped Instructions (`tests/AGENTS.md`)
Rather than overloading the root instructions with detailed testing rules, I placed directory-scoped guidelines in `tests/AGENTS.md`. This file enforces four testing rules: (1) interacting strictly through the public HTTP API via FastAPI's `TestClient(app)` rather than calling internal helpers like `encode()` or `get_db()`, (2) covering both happy paths (`200`, `307`) and error states (`400`, `404`, `409`, `410`), (3) maintaining test independence by using unique `uuid4`-based aliases so tests can run in any order against `links.db`, and (4) asserting observable HTTP behavior rather than internal SQLite details. Scoping these rules keeps non-test tasks lightweight while ensuring rigorous test quality whenever test files are touched.

## 3. Reusable Workflow (`SKILL.md`)
I created `.agents/skills/implement-feature/SKILL.md` (also mirrored at `SKILL.md`) to codify a repeatable 7-step Test-Driven Development (TDD) loop whenever a new feature is requested:
1. Read the target task from `docs/TASKS.md`.
2. Inspect `main.py`, `test_main.py`, and `AGENTS.md`.
3. Write down the expected API contract and edge cases before editing files.
4. Add a failing test first (**Red**) and verify failure with `pytest`.
5. Implement the smallest possible code change in `main.py` (**Green**).
6. Run `pytest` to confirm a 100% pass rate.
7. Summarize code changes, test coverage, and architectural risks.

Packaging this sequence as a reusable skill eliminates prompt repetition and prevents the agent from jumping straight into code edits before establishing a failing test.

## 4. Tool Discovery & Agent Feature Mapping
Each repository artifact maps directly to a core capability in **Antigravity**:
- **Root `AGENTS.md`** → Workspace-level persistent rules automatically read to establish project architecture, commands, and guardrails.
- **`tests/AGENTS.md`** → Path-scoped instructions loaded via progressive disclosure when working on tests.
- **`.agents/skills/implement-feature/SKILL.md`** → Reusable Agent Skill (`SKILL.md` with YAML frontmatter) that standardizes multi-step feature execution.
- **Three-Stage Execution (`Plan -> Implement -> Review`)** → Role-separated agent phases separating read-only design from code mutation and post-implementation critique.

## 5. Planning, Implementation & Review Insights (Task 1: Custom Alias)
We applied the three-stage workflow to **Task 1 (Custom Alias)** from `docs/TASKS.md`:
- **Phase 1 (Plan):** Without modifying any files, the planner specified adding `alias: str | None = None` to `ShortenRequest` and leveraging SQLite's `UNIQUE` constraint on `links.code` to detect duplicate aliases.
- **Phase 2 (Implement):** Following the TDD skill, we first added `test_custom_alias_success` and `test_custom_alias_conflict_returns_409` to `test_main.py` and verified they failed (`2 failed, 3 passed`). We then added a minimal 14-line branch in `shorten()` in `main.py` that inserts `(req.alias, req.url)` and catches `sqlite3.IntegrityError` to raise `HTTPException(status_code=409, detail="alias already in use")`. Re-running `pytest` resulted in **5/5 passing tests (100%)**.
- **Phase 3 (Review):** The reviewer rated the change **ACCEPT**, confirming adherence to parameterized SQL queries, connection closing (`with closing(get_db())`), and public-API test independence, while noting a subtle edge case: if a user registers a short Base62 custom alias (e.g., `"e"`) before `row_id` reaches that count, a future auto-generated `encode(row_id)` could collide with it.

## 6. Key Lessons on Structuring a Repo for Agents
Structuring a repository for coding agents requires treating context as a scarce, hierarchical resource. Concise root instructions (`AGENTS.md`) with explicit product non-goals stop agents from hallucinating extra infrastructure, while scoped rules (`tests/AGENTS.md`) and reusable skills (`SKILL.md`) deliver specialized constraints right when needed. Finally, combining a strict Red-Green `pytest` verification loop with separated Plan, Implement, and Review phases transforms an agent from an unpredictable code generator into a disciplined engineering partner.

