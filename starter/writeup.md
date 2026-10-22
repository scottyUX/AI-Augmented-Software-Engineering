# Week 4 Writeup — Structuring a Repo for Agents

**Name:** Mohammad Poorahmadi

---

### 1. Root Repository Guidance (`AGENTS.md`)
Root `AGENTS.md` contains fundamental repository context: application overview (FastAPI URL shortener), core file map (`main.py`, `test_main.py`, `docs/TASKS.md`), environment setup/execution commands (`pytest`, `uvicorn`), product boundaries, and high-level workflow steps. This information is kept broadly available at the repository root so any task—regardless of scope—has immediate access to build tools, test suites, and core architecture constraints, preventing context hallucination or breaking changes.

### 2. Scoped Instruction (`tests/AGENTS.md`)
The scoped instruction in `tests/AGENTS.md` defines testing-specific guardrails, such as using `TestClient`, enforcing non-redirect assertions (`follow_redirects=False`), and requiring coverage for both success paths and error handling. It loads dynamically whenever the agent opens, edits, or operates on files within the `tests/` directory. Scoping this guidance prevents unnecessary context token bloat during non-testing workflows like documentation edits or API schema adjustments.

### 3. Reusable Workflow (`SKILL.md`)
The `SKILL.md` workflow encodes a 7-step standard operating procedure for feature execution:
1. **Context Gathering:** Read task specs and repo guidance.
2. **Code Inspection:** Examine existing implementation and tests.
3. **Strategy Declaration:** State expected behavior and affected files without editing.
4. **Test-Driven Development:** Write a failing test asserting expected behavior.
5. **Implementation:** Make the minimal code change to satisfy requirements.
6. **Verification:** Execute `pytest` to ensure all tests pass.
7. **Summary:** Document changes and evaluate remaining edge-case risks.

### 4. Discovery & Invocation in Antigravity
The selected agent (Antigravity with Claude Sonnet 4.6) discovers root `AGENTS.md` upon opening the workspace. It dynamically traverses and ingests nested directory instructions (`tests/AGENTS.md`) when accessing test files. The `SKILL.md` reusable procedure is explicitly invoked during Stage 2 prompting ("Follow the exact 7-step workflow defined in SKILL.md"), directing the agent through sequential execution.

### 5. Planning and Review Insights
During Stage 1 planning, the agent identified that the SQLite schema already declared `code TEXT UNIQUE`, allowing custom alias uniqueness to be enforced cleanly via `sqlite3.IntegrityError` without DB migrations. During Stage 3 review, the agent confirmed that making `alias: str | None = None` on `ShortenRequest` preserved full backward compatibility for existing requests without aliases, and verified that edge cases like blank strings were properly rejected with HTTP 400.

### 6. Structuring Repositories for Coding Agents
Structuring a codebase for agents requires layered context management. Broad environment rules belong at the root, domain-specific constraints belong near targeted folders, and multi-step tasks require explicit procedural workflows (`SKILL.md`). Clear operational boundaries and strict TDD guardrails reduce agent hallucinations, enforce repeatable execution, and turn LLMs into reliable engineering collaborators.