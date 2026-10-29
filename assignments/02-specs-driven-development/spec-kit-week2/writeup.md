# Week 2 Deliverable Writeup — Spec-Driven Development

## 1. Skill Prompts Log

Below are the exact prompts used with each Spec Kit skill during the development loop:

- **/speckit-constitution**:
  `Create principles focused on code quality, testing, and maintainability.`
- **/speckit-specify**:
  `A quote-of-the-day page: one random quote from a built-in list, a "New quote" button, and favoriting that persists across reloads.`
- **/speckit-plan**:
  `Use plain HTML/CSS/JavaScript, no backend; persist favorites in localStorage.`
- **/speckit-tasks**:
  `Generate actionable implementation tasks for HTML, CSS, JavaScript, and storage logic.`
- **/speckit-implement**:
  `Build the complete Quote of the Day web application matching the specifications and implementation plan.`
- **/speckit-converge**:
  `Assess the codebase against the specification and confirm all user stories, edge cases, and success criteria are satisfied.`

---

## 2. Spec/Plan Refinement (Before vs. After)

- **Before Refinement**:
  The initial specification and plan only accounted for toggling a "Favorite" status on the currently displayed quote card on the home screen. Users could save quotes, but had no dedicated way to view all their saved quotes without repeatedly clicking "New Quote".
- **After Refinement**:
  We refined `spec.md` (User Story 3 & FR-007) and `plan.md` to add a dedicated **"My Favorites" modal drawer**. This allows users to inspect all saved favorite quotes in a clean list and remove quotes from favorites directly within the modal.
- **Impact**:
  This spec refinement added the `favoritesModal` component and rendering logic to `index.html`, `styles.css`, and `app.js`, significantly improving user experience and giving tangible value to `localStorage` persistence.

---

## 3. Convergence Outcome

- **Status**: **CONVERGED**
- **Assessment**:
  - All 3 User Stories (P1: View & New Quote, P2: Favorite & Persist, P3: View Saved Favorites) are fully implemented and verified.
  - Edge cases (missing `localStorage`, corrupt data fallback) are handled gracefully.
  - All functional requirements (FR-001 through FR-007) and success criteria are met without remaining task debt.

---

## 4. What I Learned (Reflection)

Spec-Driven Development (SDD) initially felt like extra overhead when creating formal `.specify` markdown files for a relatively small client-side application. However, defining explicit user scenarios and technical constraints before writing any code paid off by eliminating guesswork during implementation. The structured human-in-the-loop review gate ensured edge cases (such as data corruption and empty state views) were caught upfront rather than patched later. Overall, SDD transformed AI assistance from an unpredictable trial-and-error loop into a deterministic, reliable software assembly process.
