# Week 4 Writeup - Structuring a Repo for Agents: The Link Shortener

**Student:** Zuhal Çolak  
**Agent:** Antigravity / Gemini CLI  
**Task:** Task 1 — Custom Alias  
**Validation:** 8/8 tests passed consecutively  

---

### 1. Root `AGENTS.md` Information and Broad Availability
In `AGENTS.md`, I included high-level architectural context: system overview, file directory layout, run/test commands, strict product boundaries (no frontend UI, no external databases or auth), reserved system routes (`docs`, `redoc`, `openapi.json`, `shorten`), and a concise 4-step workflow (understand → test → implement → verify). This information must be broadly available at the repository root because every agent session needs an immediate, unified mental model of the service's boundaries, execution commands, and architectural limits before touching any file. Keeping it under 40 lines prevents context bloat while orienting unfamiliar agents instantly.

### 2. Scoped Instruction and Activation Context
I scoped testing instructions into `tests/AGENTS.md`. It mandates exercising endpoints solely through FastAPI's public `TestClient(app)`, requiring symmetric coverage (success and failure/edge cases), enforcing test independence across runs (using dynamic UUIDs and temporary test databases via `tmp_path`), and asserting on HTTP behaviors rather than private SQLite states. This instruction loads just-in-time only when an agent navigates into, edits, or inspects the `tests/` directory. It should not be loaded during non-testing tasks (such as refactoring data models or updating documentation) to conserve context window tokens and avoid irrelevant instruction noise.

### 3. Reusable Workflow Procedure
The reusable workflow in `.agents/skills/implement-feature/SKILL.md` encodes a disciplined 7-step test-driven procedure: (1) review task requirements and boundaries, (2) inspect relevant code and schemas, (3) declare the API contract and affected files prior to coding, (4) write failing behavioral tests, (5) implement the minimal code change, (6) verify by running `pytest` twice consecutively to ensure idempotency and test independence, and (7) summarize modifications and assess remaining operational risks.

### 4. Agent Discovery and Invocation Mechanisms
In Antigravity and Gemini CLI, the agent automatically reads root `AGENTS.md` at session startup to establish repository-level context. When the agent accesses or modifies files under `tests/`, the hierarchical rule system discovers `tests/AGENTS.md` via path-based matching and injects it into context. Reusable workflows conforming to the Agent Skills standard (`.agents/skills/<skill-name>/SKILL.md`) are automatically registered in the agent's skill catalog and invoked directly during feature implementation.

### 5. Planning and Review Improvements
During the three-stage lifecycle (Plan → Implement → Review), the agent identified two critical edge cases:
- **Auto-Generation Collision:** If a customer creates a custom alias that coincides with a future base62 encoded ID (e.g., alias `"b"` matching row 2), subsequent automatic shortenings would crash with an unhandled SQLite UNIQUE constraint error (`500`). The plan introduced an auto-generation collision loop that skips occupied codes.
- **Route Shadowing & Regex Security:** During review, the agent flagged that reserved routes must be blocked with `409 Conflict` before format validation, and regex matching must use `\Z` instead of `$` to prevent trailing newline injection.

### 6. Lessons Learned on Structuring Agentic Codebases
Structuring a repository for coding agents is fundamentally an exercise in context scoping and guardrail placement. Global context must remain concise and boundary-focused; cramming every operational detail into the root floods the context window and dilutes adherence. Scoping guidelines to subdirectories ensures instructions appear only when relevant. Pairing modular guidance with standardized workflows and structured lifecycle handoffs (Plan, Implement, Review) transforms LLMs from unpredictable code generators into reliable, disciplined pair programmers.
