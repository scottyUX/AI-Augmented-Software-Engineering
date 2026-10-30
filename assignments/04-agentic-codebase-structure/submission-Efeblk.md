# Week 4 Submission: Efeblk

Repository: https://github.com/Efeblk/week4-link-shortener

- Agent: Codex.
- `AGENTS.md`: purpose, file map, setup/run/test commands, out-of-scope list, change workflow.
- Scoped instruction: `tests/AGENTS.md` (public HTTP API tests through `TestClient`, success and failure cases, independent tests, behaviour not SQLite internals).
- Reusable workflow: `.agents/skills/implement-task/SKILL.md` (7-step feature procedure).
- Feature: task 2, click counter. Redirects count clicks; `GET /stats/{code}` returns the URL and click count, 404 for unknown codes.
- Plan, implement and review stages saved in `docs/stages/`; review returned ACCEPT.
- Tests: 7 pass (3 original, 4 new). Each test uses its own temporary database.
- `writeup.md` answers the six questions.
