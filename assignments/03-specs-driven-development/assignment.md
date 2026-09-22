# Week 3 — Spec-Driven Development with Spec Kit

## Overview
This week you'll build a small application the **spec-driven** way using GitHub's
[**Spec Kit**](https://github.com/github/spec-kit). Instead of vibe-coding, you'll
define **what and why** before **how**: a constitution, a specification, a technical
plan, and a task list — then let your coding agent implement against those artifacts
and iterate until it *converges*.

The point is not the app. The point is the **process**: producing durable spec
artifacts, keeping a human-in-the-loop review gate at each step, and comparing the
result to how you'd normally build.

## Learning goals
- Run the full Spec Kit SDD loop: **constitution → specify → plan → tasks →
  implement → converge**.
- Write specs that are precise enough for an agent to implement without guessing.
- Experience the human review gate between each stage.
- Reflect on when SDD is worth the overhead — and when it isn't.

---

## Prerequisites
- Python **3.11+** and [**uv**](https://github.github.io/spec-kit/install/uv.html).
- A Spec Kit–supported coding agent (Claude Code, Copilot, Cursor, Gemini/Antigravity,
  etc.). Use the one you set up in Week 1.

## Setup
From your terminal, install the Spec Kit CLI and initialize a project. Replace
`copilot` with your agent's [integration key](https://github.github.io/spec-kit/reference/integrations.html):

```bash
uv tool install specify-cli
specify init spec-kit-week3 --integration copilot
cd spec-kit-week3
```

Then **launch your coding agent inside the project directory.** The `/speckit-*`
skills are invoked in the **agent's chat**, one at a time — they are not terminal
commands.

## Part 1 — Pick a feature
Choose a small but non-trivial app that has real data and at least one interesting
rule. Examples:
- A photo organizer with albums grouped by date and a tile preview per album.
- A personal-finance tracker that categorizes transactions and flags overspending.
- A flashcard app with spaced-repetition scheduling.

Pick something you can *specify precisely* — that's the skill being graded.

## Part 2 — Run the SDD loop
Invoke each skill in your agent's chat, and **review the generated artifact before
moving on**:

```text
/speckit-constitution Create principles focused on code quality, testing, and maintainability.
/speckit-specify <one or two sentences describing WHAT and WHY for your feature>
/speckit-plan <your technical choices: language, framework, storage, constraints>
/speckit-tasks
/speckit-implement
/speckit-converge
```

- Repeat **`/speckit-implement` → `/speckit-converge`** until convergence reports
  **Converged**.
- At **each** stage, read the artifact Spec Kit produced under `.specify/` and, when
  something is vague or wrong, **refine the spec/plan** rather than hand-editing the
  code. Capture at least one example where tightening the spec changed the output.

> Optional quality gates: add clarification, checklists, or consistency analysis if
> your agent's Spec Kit integration supports them. Document if you use them.

## Part 3 — Compare against vibe coding
Take **one** feature or bug from your app and implement it the *unstructured* way —
a single free-form prompt to your agent, no spec. Briefly compare the two approaches.

## Deliverables
Push `spec-kit-week3/` to a GitHub repo (add the instructor as a collaborator if
private). It must include:
1. The generated **spec artifacts** in `.specify/` (constitution, spec, plan, tasks,
   convergence report) — committed, not gitignored.
2. The **working application** produced by `/speckit-implement`.
3. A `writeup.md` containing:
   - Your feature idea and the exact prompts you gave each `/speckit-*` skill.
   - One concrete before/after where refining the **spec or plan** (not the code)
     improved the result.
   - The convergence outcome and how many implement→converge rounds it took.
   - **Part 3 comparison:** spec-driven vs. vibe-coded — which was faster, which was
     more correct, and when you'd choose each.
   - 3–4 sentences on where SDD felt like overhead and where it clearly paid off.

## Evaluation (100 pts)
- 30 — Complete, committed spec artifacts for all stages (constitution → converge).
- 25 — Working app that matches its own spec; convergence reached.
- 20 — Evidence of the human review gate: at least one spec/plan refinement that
  measurably changed the output.
- 15 — Thoughtful vibe-coding comparison (Part 3).
- 10 — Clear, complete `writeup.md`.

## Helpful references
- Spec Kit repo: https://github.com/github/spec-kit
- SDD walkthrough / quickstart: https://github.github.io/spec-kit/quickstart.html
- Command reference: https://github.github.io/spec-kit/reference/agentic-sdd.html
- Integration keys (agent-specific invocation): https://github.github.io/spec-kit/reference/integrations.html
