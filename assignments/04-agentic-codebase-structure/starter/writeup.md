# Week 4 Write-up — Structuring a Repo for Agents: The Link Shortener

**Agent:** Antigravity / Gemini CLI · **Task:** Task 1 — Custom Alias · **Verification:** 8 tests pass, verified twice consecutively

---

### 1. `AGENTS.md` Repository Guidance

`AGENTS.md` provides essential baseline context: system overview, file directory layout, run and test commands, strict product boundaries (no frontend UI, no external databases or auth, and reserved route protection for `/docs`, `/redoc`, `/openapi.json`, and `/shorten`), and the 4-step workflow (understand → test → implement → verify). Broad availability at the repository root ensures any unfamiliar agent immediately understands system limits, architectural patterns, and execution environment before reading any subfolder.

### 2. Scoped Instruction

`tests/AGENTS.md` contains scoped testing principles: exercising endpoints solely via `TestClient(app)`, testing both success and failure cases symmetrically, asserting against public HTTP behaviors rather than private SQLite states, and guaranteeing execution independence across consecutive runs (e.g., using dynamic UUIDs to prevent collisions in persistent `links.db`). This instruction loads just-in-time when the agent navigates into or edits files within `tests/`, avoiding unnecessary token consumption during non-testing tasks.

### 3. Reusable Workflow

The `.agents/skills/implement-feature/SKILL.md` workflow encodes a 7-step test-driven procedure: (1) read task and boundaries, (2) inspect existing code and tests, (3) declare expected contracts and affected files before modifying code, (4) write failing behavioral tests, (5) apply the minimal necessary code change, (6) run `pytest` twice consecutively to ensure idempotency, and (7) summarize modifications and assess risks. This enforces discipline and prevents uncontrolled codebase refactoring.

### 4. Agent Discovery Mechanisms

In modern agentic systems (such as Antigravity and Gemini CLI), root `AGENTS.md` is loaded automatically into the top-level system context at session start. Scoped guidance in `tests/AGENTS.md` is discovered hierarchically when an agent reads or touches any path under `tests/` via just-in-time context injection. The reusable workflow in `.agents/skills/implement-feature/SKILL.md` conforms to the Agent Skills standard, discovered by the agent's skill manager and invoked during implementation.

### 5. Planning and Review Insights

During planning and review, the agent caught critical boundary conditions that naive implementations overlook:
- **Collision Avoidance:** A custom alias might match a future generated base62 code (e.g., `encode(2)`), which would cause subsequent automatic shortenings to crash with HTTP 500 SQLite integrity errors; the plan introduced an advance loop for auto-generated codes.
- **Route Shadowing & Validation Ordering:** Review flagged that reserved paths (like `openapi.json` containing `.`) must be rejected with 409 before regex checking (400), and regex must use `\Z` instead of `$` to prevent trailing newlines.

### 6. Structuring Repositories for Coding Agents

Structuring repositories for AI agents is fundamentally an exercise in context scoping and guardrail placement. Global context must stay small and boundary-focused; cramming all subsystem instructions into root files floods context windows and degrades adherence. Hierarchical scoped instructions ensure agents absorb domain-specific constraints (such as testing standards) exactly when relevant. Combined with explicit three-stage handoffs (Plan → Implement → Review) and standardized workflows, clear repo structure shifts agents from unreliable code-generators to disciplined software engineers.
