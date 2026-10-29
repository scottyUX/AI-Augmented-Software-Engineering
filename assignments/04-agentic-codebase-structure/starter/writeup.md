# Assignment 4 — Agentic Codebase Structure

## 1. Repository Guidance

I created a root-level `AGENTS.md` to help coding agents understand the Link Shortener project before making changes. It describes the FastAPI and SQLite architecture, important files, setup commands, and development boundaries. I included a five-step change workflow: Understand, Test, Implement, Verify, and Review. These instructions help agents preserve existing functionality, avoid unnecessary dependencies, and make focused changes.

## 2. Scoped Instructions

I created `tests/AGENTS.md` to provide instructions specifically for the test directory. The file requires behavioral testing through FastAPI's `TestClient`, coverage of successful and failure cases, and independent tests. Its scope is limited to files inside `tests/`, while the root `AGENTS.md` provides general project guidance. The agent inspected both files during implementation and followed the testing rules when adding new tests.

## 3. Reusable Workflow

I created the `implement-feature` skill at `.agents/skills/implement-feature/SKILL.md`. It defines seven steps: read project guidance, inspect relevant code, state the intended changes, write failing behavioral tests, implement the minimum necessary functionality, run the complete test suite, and summarize results and risks.

This workflow can be reused for other tasks in `docs/TASKS.md` without rewriting the implementation instructions each time.

## 4. Skill Discovery and Invocation

Before implementing the feature, I asked Antigravity to discover the available repository skills without modifying any files. The agent located `implement-feature`, inspected its instructions, and explained how to invoke it.

During the IMPLEMENT stage, I explicitly referenced the skill by name and path. This ensured that the agent followed the defined workflow rather than relying only on a general coding request.

## 5. Planning, Implementation, and Review

I selected Task 1, Custom Alias, from `docs/TASKS.md`.

During PLAN, the agent inspected the requirements and existing implementation, identified the affected files, and proposed tests without modifying code.

During IMPLEMENT, the agent first added two behavioral tests. Both failed because custom aliases were not yet supported. It then updated `main.py` to accept an optional alias and return HTTP 409 when an alias was already taken. The existing automatic short-code behavior was preserved. All five tests passed, including on a repeated run.

During REVIEW, a separate agent session inspected the implementation, tests, and Git diff. It returned **ACCEPT**, while identifying potential risks involving alias characters, generated-code collisions, and persistent test data.

## 6. Lessons Learned

This assignment demonstrated how repository instructions, scoped rules, and reusable skills can make AI-assisted development more structured and predictable. Separating PLAN, IMPLEMENT, and REVIEW encouraged clearer reasoning and verification. Writing failing tests before implementation provided concrete evidence that the new behavior was necessary. I also learned that passing tests does not eliminate every risk, making independent code review an important part of the workflow.