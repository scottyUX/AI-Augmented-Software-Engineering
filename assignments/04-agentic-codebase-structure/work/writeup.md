# Week 4 — Structuring a Repo for Agents: Writeup

**Feature:** Task 2, Click counter. **Tests:** `pytest -q` → **10 passed** (3 original + 7 new).
**Agents:** the artifacts target Google Antigravity (`.agents/`). The plan and review stages
were run with the GitHub Copilot agent in Codespaces; the full log is in [`agent_log.md`](agent_log.md).

## 1. `AGENTS.md`
It has a product summary, a file map, the install/run/test commands, product boundaries
(no auth, UI, ORM or new dependencies), conventions (parameterized SQL, migration-safe schema
changes, status-code meanings) and the four-step change workflow. Every task needs this,
whichever file it touches. At 43 lines it orients the agent without crowding out task context.

## 2. Scoped instruction
`tests/AGENTS.md` sets the testing rules: public API only, success and failure coverage,
independent tests using a fresh temp database (`client` fixture), and assertions on behavior.
`.agents/rules/tests.md` (`trigger: glob`, `globs: tests/**`) loads these rules only when test
files are in play. They are noise when the agent is editing routes or docs.

## 3. Reusable workflow
`.agents/skills/implement-feature/SKILL.md` goes: read the task and guidance → inspect the
code and tests, confirm green → state the behavior, edge cases, files and migration → write
failing tests → smallest implementation → `pytest -q` → summarize the changes and risks.

## 4. Discovery
| Artifact | Antigravity | Copilot (observed) |
|---|---|---|
| `AGENTS.md` | auto-loaded at the workspace root | read when pointed at `work/` (nested, not repo root) |
| test rule | glob rule fires on `tests/**` | found and read `.agents/rules/tests.md` on its own |
| skill | matched by its `description`, or named in the prompt | not used (Copilot looks in its own skill folders) |

## 5. What planning and review caught
**Plan** (on the pre-feature code, no edits allowed). The agent read the guidance, the
code, the tests and the glob rule. It proposed:

- a **guarded `ALTER TABLE`** so existing `links.db` files keep working;
- an **atomic SQL increment**, done only on a successful redirect;
- **`/stats` views and unknown codes don't count**;
- an optional **legacy-schema upgrade test**.

All four are in the final change, each with a test.

**Review** (no edits allowed). The agent diffed against `main` and ran `pytest -q`. Verdict:
**ACCEPT**. It confirmed the counting, the 404s, the migration, and tests that follow the
API-only guidance.

## 6. What I learned
An agent starts each session as a new teammate with no memory, so the repo has to explain
itself. Splitting guidance by when it's needed keeps context small: always-on orientation,
path-scoped test rules, and an on-demand procedure. The planning stage showed it working.
Unprompted, the agent proposed the same migration and test-isolation approach the guidance
asks for, and it found the scoped rule by itself. Separate plan, implement and review stages,
each told not to overstep, made every step easy to verify.
