# Week 4 — Structuring a Repo for Agents

I used VS Code Copilot and chose the **Custom alias** task from `docs/TASKS.md`.
The original test suite passed three tests before changes. My plan was to accept an
optional alias in `POST /shorten`, persist it as the short code, return 409 if that
code is already taken, and leave generated codes unchanged. I added public-API tests
first; both failed against the original implementation, then passed after the change.
The final suite passes all five tests.

## Repository guidance

`AGENTS.md` is at the starter repository root. It gives an unfamiliar agent a short
description of the service, points to `main.py`, `test_main.py`, `docs/TASKS.md`, and
`requirements.txt`, and lists the commands to install, run, and test the app. It also
sets product boundaries and a small understand-test-implement-verify workflow. This
context should be broadly available because it applies to almost any change in this
small service: knowing its entry points, commands, and intended scope prevents wasted
exploration and unrelated architectural work.

The scoped instruction is
`.github/instructions/tests.instructions.md`, with `applyTo: "test_main.py"`.
Because the current test file is at the starter root, this pattern targets the actual
tests rather than an unused `tests/` directory. It asks for public-route behavior,
success and failure coverage, order-independent tests, and assertions against observable
results. It should not load for ordinary application edits because those test-specific
details are only relevant while changing `test_main.py`. VS Code Copilot discovers the
instruction from `.github/instructions/` and applies its frontmatter pattern.

## Reusable workflow and feature

`.github/skills/implement-shortener-feature/SKILL.md` encodes the repeatable feature
procedure: read the task and guidance, inspect related code and tests, state expected
behavior and affected files, add and run a failing behavioral test, make the smallest
implementation, run the full pytest suite, and report results and risks. Copilot
discovers project skills under `.github/skills/`; its description supports automatic
matching, and the skill can also be explicitly invoked as
`/implement-shortener-feature`.

The implementation inserts a supplied alias directly and relies on SQLite's unique
constraint to detect a collision, returning HTTP 409. This avoids a separate
check-then-insert race. Tests exercise alias creation and redirect, and duplicate-alias
conflict; generated unique test aliases avoid dependence on prior test runs. The
original three tests continue to pass.

## Stages and reflection

During Plan, inspecting the schema showed that `code` is already unique, so using that
constraint is safer than checking availability before insertion. During Implement, I
added both behavioral tests before changing the route, confirmed the expected failures,
then implemented the optional request field and conflict response. During Review, a
separate read-only review returned **ACCEPT**: the feature, tests, and guidance matched
the assignment, with no actionable findings.

I learned that agent readiness is about putting each instruction at the right level.
Repository navigation belongs in always-available context; test conventions belong
with test-file matching; a feature procedure belongs in an on-demand skill. This keeps
guidance useful without loading every detail into every task, while the tests and
workflow make the behavior and verification steps explicit.
