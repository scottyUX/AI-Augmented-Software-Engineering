# Week 4 Writeup — Structuring a Repo for Agents

**Agent:** Google Antigravity (Claude Sonnet 4.6 Thinking; Gemini 3.8 Flash hit its daily quota during planning).
**Feature:** Task 1 — Custom alias. **Result:** `pytest` 10 passed (3 original + 7 new); review returned **ACCEPT**.

## 1. What is in `AGENTS.md`, and why is it broadly available?
It explains what the service does (`POST /shorten`, `GET /{code}`), where the important files are, the install/run/test commands, product boundaries (no auth, ORM, new dependencies or refactors), conventions (parameterized SQL, `HTTPException`, schema changes only in `init_db()`), and a four-step change workflow: understand → test → implement → verify. Every task needs this orientation, so it belongs in the always-loaded root file. I kept it to 40 lines so it orients the agent without filling its context.

## 2. Which instruction is scoped, and when does it load?
`tests/AGENTS.md` holds the testing rules: test through the public API with `TestClient`, cover success and failure, keep tests independent (unique `uuid` aliases, no reliance on existing rows in `links.db`), and assert behavior rather than internals. I moved `test_main.py` into `tests/` and added `pytest.ini` (`testpaths = tests`, `pythonpath = .`) so the rule applies to exactly the test files. It is relevant only when the agent reads or edits files under `tests/`. Loading it for every task, such as editing docs or the README, would only add noise.

## 3. What procedure does the reusable workflow encode?
`.agents/skills/implement-feature/SKILL.md` encodes a test-first feature procedure: read the task and both `AGENTS.md` files, inspect the code and run `pytest`, state the expected behavior and affected files, add failing behavioral tests, implement the smallest change, run `pytest` again, and summarize the change and remaining risks.

## 4. How does Antigravity discover or invoke each artifact?
Antigravity loads the root `AGENTS.md` as workspace context when the `work/` folder is opened as the project. It picks up `tests/AGENTS.md` as the nested, directory-scoped instruction when it works in `tests/`. In my session the agent explicitly read it and followed its `uuid` rule. Skills in `.agents/skills/<name>/SKILL.md` follow the Agent Skills standard (the same place Spec Kit installed its `/speckit-*` skills in Week 2). I invoked mine with `/implement-feature`, and the agent answered "I'll follow the implement-feature skill workflow" and went through the steps in order.

## 5. What did planning or review find that improved the result?
Planning, done without edits, flagged three things. An empty alias (`""`) would silently fall back to an auto-generated code, so it should return 400. Aliases containing `/`, `?` or `#` could break routing. And an alias like `"b"` can later collide with a base62 auto-code and cause a 500. From this I added a validation rule (`^[A-Za-z0-9_-]{1,30}$`, otherwise 400) and kept the collision as a documented out-of-scope risk. The review, run in a fresh conversation, returned ACCEPT. Its only minor note was that the 409 test does not assert that the first request succeeded.

## 6. What did I learn?
A small, layered structure works better than one long instruction file: global facts in `AGENTS.md`, area rules next to the code they govern, and procedures as skills. The test-independence rule mattered in practice, because the SQLite file persists between runs and a fixed alias would fail on the second run. Separating plan, implement and review also helped: the read-only plan surfaced edge cases before any code existed, and a fresh reviewer checked the result against the written rules.
