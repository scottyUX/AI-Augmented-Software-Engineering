# Week 2 — Spec-Driven Development Writeup

**Agent:** Google Antigravity (Gemini 3.8 Flash) · **Spec Kit:** specify-cli 1.2.1 (`--integration agy`)

## Prompts given to each skill

**Round 1**
- `/speckit-constitution Create principles focused on code quality, testing, and maintainability.`
- `/speckit-specify A quote-of-the-day page: one random quote from a built-in list, a "New quote" button, and favoriting that persists across reloads.`
- `/speckit-plan Use plain HTML/CSS/JavaScript, no backend; persist favorites in localStorage.`
- `/speckit-tasks`
- `/speckit-implement`
- `/speckit-converge` → **Converged**

**Round 2 (after refining the spec)**
- Spec refinement: `Refine specs/001-quote-of-the-day/spec.md only (do not change code yet): The quote shown on page load must stay the same for the whole calendar day, based on the user's local date, so reloading the page shows the same quote of the day. The "New quote" button still shows a random quote, but never the same quote that is currently displayed.`
- `/speckit-plan Update the plan for the refined spec: choose the daily quote deterministically from the user's local date; keep plain HTML/CSS/JavaScript and localStorage.`
- `/speckit-tasks`
- `/speckit-implement`
- `/speckit-converge` → **Converged**

## Spec refinement: before / after

- **Before:** The original spec only said "one random quote". The page showed a different quote on every reload, so it was not really a *quote of the day*.
- **What I changed:** I refined the spec (not the code) to require that the quote on page load is chosen from the user's local date and stays the same all day, and that "New quote" never repeats the quote currently shown.
- **After:** Reloading the page now shows the same quote all day, and "New quote" still gives a different random quote. Commit: `docs: refine spec - quote stays the same all day`, followed by `feat: daily quote stays the same all day`.

## Convergence outcome

Both rounds ended with `/speckit-converge` reporting **Converged**: the implementation satisfied the spec, plan, and tasks, and no new tasks were appended.

## What I learned

For a page this small, writing a constitution, plan, and task list felt like overhead, and approving many agent commands slowed me down. But it paid off when I noticed the reload problem: I only had to fix one sentence-level gap in the spec, and the agent updated the plan, tasks, and code to match without me touching the code. The spec made the bug easy to describe because the mistake was in the requirements, not in the implementation. Next time I would think harder about edge cases like "what happens on reload" before running /speckit-specify.