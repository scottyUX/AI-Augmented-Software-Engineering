# Week 4 Assignment Writeup: Agentic Codebase Structure & Workflow

## Overview
This writeup reflects on transforming a FastAPI and SQLite link shortener into an agent-native repository, establishing concise repository guidance, configuring explicit scoped test instructions, utilizing reusable Gemini CLI skills, and successfully delivering the Custom Alias feature.

## Reflection & Detailed Answers

### 1. Purpose and Value of Repository Guidance (`AGENTS.md`)
Repository guidance acts as the foundational operational contract for coding agents. By keeping `AGENTS.md` concise, we provided essential clarity regarding the FastAPI and SQLite architecture, key files (`main.py`, `test_main.py`), setup and execution commands (`pip install -r requirements.txt`, `pytest`), product boundaries, and the core Understand → Test → Implement → Verify workflow. This concise structure prevents coding agents from wandering into architectural drift or making incorrect assumptions.

### 2. Scoped Testing Instructions for Root-Level Tests
Because existing tests reside in root-level `test_main.py` rather than a dedicated `tests/` subdirectory, automatic directory scoping does not apply. We created `tests/AGENTS.md` containing specific test rules: use the public FastAPI API via `TestClient`, cover success and failure cases, keep tests independent of execution order, and assert observable behavior rather than implementation details. `GEMINI.md` explicitly tells Gemini CLI to read `tests/AGENTS.md` when creating or modifying `test_main.py`. This is an explicit loading rule, not automatic directory scoping.

### 3. Why Test-Specific Guidance Should Not Be Loaded for Unrelated Tasks
Test-specific guidance should not be loaded for unrelated tasks (such as editing application business logic, modifying database schemas, or updating documentation) to prevent context pollution and unnecessary token consumption. Restricting test rules exclusively to test file operations keeps the agent's context window lean and focused strictly on the relevant behavioral constraints for that specific task.

### 4. Discovery Mechanisms in Gemini CLI & Skill Invocation
Gemini CLI discovers project context through convention-based root files like `GEMINI.md`, which links to core repository guidance. Reusable skills are discovered automatically from the `.gemini/skills/` directory structure. The skill is invoked explicitly by calling the `activate_skill` tool with its name (`implement-feature`), loading its specialized instructions and seven-step workflow into the session.

### 5. The PLAN → IMPLEMENT → REVIEW Lifecycle
Adhering to the Research → Strategy/Plan → Execution → Validation → Review lifecycle ensured safe, predictable development. During planning, the agent mapped out database conflict handling and Pydantic validation requirements. Implementation applied minimal necessary changes, and review rigorously audited all test outputs against expectations.

### 6. Custom Alias Feature Implementation & Learnings
For the Custom Alias feature, the agent updated the request model and endpoint in `main.py`, adding success and conflict test cases in `test_main.py`. Running `pytest` produced 5 passing tests and 1 warning, confirming robust behavioral correctness. The final review outcome was ACCEPT. Overall, this assignment demonstrated how agent-ready structures and structured skills enable reliable autonomous software engineering.
