# Week 2 Writeup — Spec-Driven Development

## 1. Prompts Used
- **/speckit-constitution**: `Create principles focused on code quality, testing, and maintainability.`
- **/speckit-specify**: `A quote-of-the-day page: one random quote from a built-in list, a "New quote" button, and favoriting that persists across reloads.`
- **/speckit-plan**: `Use plain HTML/CSS/JavaScript, no backend; persist favorites in localStorage.`
- **/speckit-tasks**: `/speckit-tasks`
- **/speckit-implement**: `/speckit-implement`
- **/speckit-converge**: `/speckit-converge`

---

## 2. Spec/Plan Refinement (Before vs. After)

- **Initial State:** 
  The original spec and plan only covered displaying a single random quote, toggling the current quote as a favorite, and persisting that state in `localStorage`. There was no mechanism for users to view, browse, or manage their collection of saved favorites in one place.

- **Refinement:**
  I refined the requirements by prompting `/speckit-specify` to add a small, temporary notification when saving or removing a favorite, and to make the favorites drawer collapsible.I then ran `/speckit-plan` to specify implementing this via plain CSS and DOM updates without backend dependencies.

- **Result:**
  The agent updated `plan.md` and added dedicated sub-tasks to `tasks.md`. Running `/speckit-implement` generated the notifications and sync logic between `localStorage` and the expanded favorites list.
---

## 3. Convergence Outcome
After running the updated loop, `/speckit-converge` reported:
> `✅ Converged — the implementation satisfies the spec, plan, and tasks. No convergence tasks were appended; tasks.md remains unchanged.`

---

## 4. What I Learned (Reflection)
When creating the website with the initial specifications, it was able to create a working product with little involvement. However, when it came to the refinement, it was able to create the notification easily, but struggled with the collapsible favorites drawer, which had issues with the animations despite converging. This taught me that automated convergence works well for functional requirements, but human evaluation is still needed for some of the more subtle visual features.