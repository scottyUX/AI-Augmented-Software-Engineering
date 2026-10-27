# Week 2 Submission: Riza Arslan

**Project repository:** https://github.com/xXx0001-crybto/spec-kit-week2

**Writeup:** https://github.com/xXx0001-crybto/spec-kit-week2/blob/main/writeup.md

**Project:** Quote of the Day, built with spec-driven development using GitHub Spec Kit
(v1.2.3) and Claude Code.

## What's in the repo

- Spec artifacts committed one stage at a time: constitution, spec, refined spec, plan
  (with research, data model, UI/module contracts and quickstart) and tasks (31)
- The page (`index.html`, `styles.css`, `src/`): a random quote from a built-in list, a
  "New quote" button, and favorites saved in localStorage
- Tests: 46 passing, 100% line coverage

## Spec refinement

The first spec let users favorite quotes but gave them no way to see them. I refined the
spec (before any code) to add a "Favorites" list with a remove button per entry and a
"No favorites yet" empty state (FR-011 to FR-015). That change flowed into the contracts,
the `favorites-store.js` API (`list`, `add`, `remove`) and a whole new task phase
(T023–T026).

## Convergence

Converged on the first implement → converge round, with no findings; 31/31 tasks complete.
CI was recorded as a deferral (the plan postpones it until a repository host is chosen).
