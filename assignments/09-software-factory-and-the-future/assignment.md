# Week 9 — The Software Factory: Generate & Critique

**Estimated time: ~3 hours.**

## Overview
When generating a working app takes minutes, the engineer's job shifts from *writing*
code to *evaluating and integrating* it. You'll generate a full app with an AI app
platform (**[bolt.new](https://bolt.new/)**), then critically evaluate and fix what it
produced.

A ready-to-paste app spec is in [`starter/PROMPT.md`](starter/PROMPT.md).

## Learning goals
- Use an AI app-generation platform end-to-end.
- Critically evaluate generated code (what it got right/wrong).
- Reflect on self-running, self-improving systems and where the SDLC is heading.

---

## The app — Event RSVP
Minimum scope (also in `starter/PROMPT.md`):
- CRUD **events** (title, date, location, capacity).
- Visitors RSVP yes/no; enforce capacity ("Event full" when at capacity).
- Persistent storage, basic validation, a simple functional UI, and local-run instructions.

## What to do
1. **Generate.** Claim your Bolt credits, paste `starter/PROMPT.md` into
   [bolt.new](https://bolt.new/), and iterate prompts until the app meets the scope above.
2. **Export** the generated code into your repo under `event-rsvp/`.
3. **Evaluate & fix.** Run it. Find at least **two** things the generator got wrong or
   left incomplete (a bug, a missing validation, a security/UX gap) and fix them —
   note whether you fixed them by re-prompting Bolt or by hand.

> Scope note: **one** generated version this week (not three). Focus on evaluation, not breadth.

## Deliverables
**Submit the GitHub repository link** containing `event-rsvp/` with:
- The exported source and a `README.md` (prereqs, install, run, env).
- A `writeup.md`:
  - Your final prompt(s) and how many iterations it took.
  - The **two+ issues** you found and how you fixed each.
  - **What you learned:** 3–5 sentences comparing generating vs. building by hand, and —
    if this app had to *improve itself* with minimal human input — what would break first
    and what guardrail you'd add.

## Evaluation (100 pts)
- 30 — Generated app meets the minimum scope and runs.
- 25 — Clear README (prereqs/install/run/env).
- 25 — Two+ real issues found and fixed, with explanation.
- 20 — `writeup.md` with prompts, iterations, and the "what you learned" reflection.

## References
- Bolt intro: https://support.bolt.new/building/intro-bolt
