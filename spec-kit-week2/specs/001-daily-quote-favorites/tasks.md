# Tasks: Daily Quote Favorites

**Input**: Design documents from `/specs/001-daily-quote-favorites/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/page-and-persistence.md`, and `quickstart.md`

**Tests**: Included because the project constitution and implementation plan require repeatable behavior checks. Use test-first tasks for each story and run browser acceptance checks after implementation.

**Organization**: Tasks are grouped by user story so each increment has a clear goal and independent acceptance criteria.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Parallelizable because it touches a separate file or is an independent validation task with no pending implementation dependency.
- **[Story]**: User story label maps to `spec.md`.
- Every task names the file or validation guide it changes or uses.

## Phase 1: Setup

**Purpose**: Prepare the planned source and test locations. No framework, package manifest, or runtime dependency is required.

- [X] T001 Create the planned `src/` and `tests/` directories for browser modules and Node tests.

---

## Phase 2: Foundational

**Purpose**: Establish the shared page structure and presentation that all stories use.

- [X] T002 [P] Create the semantic page shell, quote region, live status region, native action buttons, and favorites section in `index.html`.
- [X] T003 [P] Add responsive base layout, readable quote styling, and visible keyboard focus states in `styles.css`.

**Checkpoint**: Shared page shell and presentation are ready before story behavior is implemented.

---

## Phase 3: User Story 1 - Discover a Quote (Priority: P1) - MVP

**Goal**: Show exactly one built-in quote and let the visitor request another without an immediate repeat when multiple quotes exist.

**Independent Test**: Open the page, verify one built-in quote appears, then activate **New quote** and verify it changes to a different entry from the collection.

### Tests and implementation for User Story 1

- [X] T004 [US1] Add test-first cases for valid quote entries, selection from the collection, no immediate repeat, and a one-entry collection in `tests/quote-state.test.mjs`; run `node --test tests/quote-state.test.mjs` and confirm the missing behavior fails.
- [X] T005 [US1] Add the built-in quote collection and selection helpers with stable unique IDs, non-empty text, optional attribution, and no-repeat selection in `src/quote-state.mjs`.
- [X] T006 [US1] Render one initial quote and wire the native **New quote** action, including polite announcement of quote changes, in `src/app.mjs`.
- [X] T007 [P] [US1] Run `node --test tests/quote-state.test.mjs` and confirm the quote-selection cases pass.
- [X] T008 [P] [US1] Run the quote-discovery browser acceptance steps in `specs/001-daily-quote-favorites/quickstart.md`.

**Checkpoint**: Story 1 works and can be validated without favorites being implemented.

---

## Phase 4: User Story 2 - Save and Manage Favorites (Priority: P2)

**Goal**: Let the visitor save the current quote, see it in a favorites collection, and remove it without duplicate entries.

**Independent Test**: Save a displayed quote, verify its favorite state and list entry, then remove it and verify it is absent.

### Tests and implementation for User Story 2

- [X] T009 [US2] Add test-first cases for adding, removing, deduplicating, and writing favorite IDs (including a failed write) in `tests/quote-state.test.mjs`; run `node --test tests/quote-state.test.mjs` and confirm the missing behavior fails.
- [X] T010 [US2] Implement favorite toggling, unique-ID serialization, and storage writes using the `daily-quote-favorites:v1` key in `src/quote-state.mjs`.
- [X] T011 [US2] Wire the current quote's accessible favorite toggle, favorites list, removal controls, and non-blocking save-failure status in `src/app.mjs`.
- [X] T012 [P] [US2] Run `node --test tests/quote-state.test.mjs` and confirm the favorite toggle and write cases pass.
- [X] T013 [P] [US2] Run the favorite add, duplicate, and remove browser acceptance steps in `specs/001-daily-quote-favorites/quickstart.md`.

**Checkpoint**: Story 2 works in one session; saved favorites can be managed and are written to browser storage.

---

## Phase 5: User Story 3 - Return to Saved Favorites (Priority: P2)

**Goal**: Restore saved favorites on reload and handle unavailable or invalid saved data without blocking quote browsing.

**Independent Test**: Start with a saved favorite in browser storage, reload the page, and verify it is listed; separately verify malformed or inaccessible storage produces a warning while quote browsing still works.

### Tests and implementation for User Story 3

- [X] T014 [US3] Add test-first cases for restoring valid IDs, rejecting malformed data, ignoring unknown IDs, removing duplicates, and handling read failures in `tests/quote-state.test.mjs`; run `node --test tests/quote-state.test.mjs` and confirm the missing behavior fails.
- [X] T015 [US3] Implement favorite restoration and visible restore-error handling during page initialization in `src/quote-state.mjs` and `src/app.mjs`.
- [X] T016 [P] [US3] Run `node --test tests/quote-state.test.mjs` and confirm restoration and failure cases pass.
- [X] T017 [P] [US3] Run the reload, empty-state, and storage-failure browser acceptance steps in `specs/001-daily-quote-favorites/quickstart.md`.

**Checkpoint**: Story 3 works independently when storage is pre-populated and preserves the empty and failure states.

---

## Phase 6: Polish and Cross-Cutting Validation

**Purpose**: Verify the complete page against accessibility, scope, and acceptance requirements.

- [X] T018 Review and refine keyboard focus, accessible state announcements, and responsive presentation in `index.html`, `styles.css`, and `src/app.mjs`.
- [X] T019 Run the full `node --test` suite and every browser scenario in `specs/001-daily-quote-favorites/quickstart.md`; resolve failures in the referenced source or test files before completion.

---

## Phase 7: User Story 2 Follow-Up - Favorite Notifications (Priority: P2)

**Goal**: Confirm successful favorite additions and removals with one temporary, non-blocking toast; failures must not produce success feedback.

**Independent Test**: Add and remove a favorite, verify the matching toast appears without shifting page content, and verify it disappears within five seconds. Trigger another successful action while it is visible and verify the message is replaced rather than stacked. Simulate a storage write failure and verify no success toast appears.

### Implementation for Favorite Notifications

- [X] T020 [P] [US2] Add a hidden polite status region for favorite notifications in `index.html`.
- [X] T021 [US2] Show add/remove success messages only after persistence succeeds, replace any current message, and restart a maximum five-second dismissal timer in `src/app.mjs`.
- [X] T022 [P] [US2] Style the toast as a fixed, non-blocking overlay with CSS transitions and `prefers-reduced-motion` handling in `styles.css`.
- [X] T023 [US2] Run the toast success, replacement, timing, and storage-failure browser checks in `specs/001-daily-quote-favorites/quickstart.md`.

**Checkpoint**: Successful favorite changes produce one accessible temporary toast; failed writes retain the existing error status and do not claim success.

---

## Phase 8: User Story 4 - Collapse the Favorites Column (Priority: P2)

**Goal**: Let visitors collapse and expand the favorites column without changing saved data, using native controls and CSS transitions.

**Independent Test**: Save a quote, collapse and expand the column using both pointer and keyboard, and verify the quote remains present and the control reports the correct expanded state.

### Implementation for Collapsible Favorites

- [X] T024 [P] [US4] Add a persistent native collapse/expand button and controlled-content relationship with `aria-expanded` and `aria-controls` in `index.html`.
- [X] T025 [US4] Implement session-only expanded state and update the control state without modifying favorites in `src/app.mjs`.
- [X] T026 [P] [US4] Add collapsed-column and content transitions, including mobile layout and `prefers-reduced-motion` behavior, in `styles.css`.
- [X] T027 [US4] Run the keyboard, saved-data-retention, state-announcement, and reduced-motion checks in `specs/001-daily-quote-favorites/quickstart.md`.

**Checkpoint**: The panel can be collapsed and restored without changing persisted favorites, and its state remains accessible.

---

## Phase 9: Final Cross-Cutting Validation

**Purpose**: Verify the original and updated feature requirements together.

- [X] T028 Run `node --test` and all quote, persistence, toast, collapse, keyboard, and reduced-motion scenarios in `specs/001-daily-quote-favorites/quickstart.md`.

## Phase 10: User Story 4 Follow-Up - Drawer Direction and Motion (Priority: P2)

**Goal**: Make the collapse affordance indicate the action at desktop and mobile widths, and ensure the drawer transition remains smooth without height measurement or layout jumps.

**Independent Test**: At wide and narrow viewports, verify collapsed/expanded arrow directions, then toggle repeatedly during animation and confirm content clips smoothly, remains mounted, and preserves favorites.

### Implementation and validation for Drawer Refinement

- [X] T029 [US4] Add responsive chevron transforms in `styles.css`: point right when the wide drawer is collapsed and left when expanded; point down when the narrow drawer is collapsed and up when expanded.
- [X] T030 [US4] Wrap favorites in one clipped child in `index.html`; transition `.favorites-content` from `grid-template-rows: 0fr` to `1fr` in `styles.css`, collapse content before wide-column resizing and reverse that order when expanding, and let the mobile panel auto-size; keep `setFavoritesExpanded` in `src/app.mjs` limited to state classes and ARIA attributes without measured or inline heights.
- [X] T031 [US4] Run the wide/narrow direction and rapid-toggle no-jump/no-flicker checks in `specs/001-daily-quote-favorites/quickstart.md` while verifying saved favorites remain unchanged.
- [X] T032 Run `node --test` and all browser scenarios in `specs/001-daily-quote-favorites/quickstart.md` after the drawer refinement.

**Checkpoint**: Drawer direction communicates the next action at each viewport, and the CSS transition opens/closes smoothly without changing saved data.

## Dependencies and Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; prepare `src/` and `tests/`.
- **Foundational (Phase 2)**: Depends on setup; the semantic page shell and stylesheet can be prepared in parallel.
- **User Story 1 (Phase 3)**: Depends on the foundation; it is the MVP and establishes the active quote behavior.
- **User Story 2 (Phase 4)**: Depends on the displayed quote from Story 1; adds favorite state and persistence writes.
- **User Story 3 (Phase 5)**: Depends on the storage format from Story 2; validate restoration independently by pre-populating storage.
- **Polish (Phase 6)**: Completed for the original feature scope.
- **Favorite Notifications (Phase 7)**: Depends on the existing favorite add/remove behavior in US2.
- **Collapsible Favorites (Phase 8)**: Depends on the existing favorites panel in US2/US3; independent of the toast implementation.
- **Final Validation (Phase 9)**: Depends on Phases 7 and 8.
- **Drawer Refinement (Phase 10)**: Follows the original collapse implementation in Phase 8; arrow styling and transition contract are refined before T031 browser checks.
- **Drawer Regression (T032)**: Depends on all Phase 10 work.

### User Story Dependencies

- **US1 (P1)**: Begins after Phase 2; no dependency on other stories.
- **US2 (P2)**: Uses the current quote established by US1.
- **US3 (P2)**: Restores the favorite format written by US2; its read behavior can be tested independently with pre-populated storage.
- **US2 notifications (P2 follow-up)**: Uses the existing successful add/remove outcomes; storage failures continue to use the existing error status.
- **US4 (P2)**: Uses the existing favorites panel and data; does not depend on notification work.
- **US4 drawer refinement**: Depends on the existing collapsed-state control and state classes from Phase 8.

### Parallel Opportunities

- In Phase 2, T002 and T003 edit separate files and can run in parallel.
- After T006, run T007 and T008 in parallel: one validates state logic and the other validates the rendered browser flow.
- After T011, run T012 and T013 in parallel.
- After T015, run T016 and T017 in parallel.
- In Phase 7, T020 and T022 edit different files and can run in parallel; T023 follows the implementation tasks.
- In Phase 8, T024 and T026 edit different files and can run in parallel; T025 follows T024 and T027 follows all implementation tasks.
- T028 runs only after both UI follow-up stories are complete.
- T029 and T030 both touch the drawer styling/behavior contract and must finish before T031; no parallel execution is recommended for this follow-up.
- Test-first and implementation tasks within each story are intentionally sequential because they exercise the same state module.

### Parallel Examples per User Story

```text
US1 after implementation: T007 (Node tests) || T008 (browser quote flow)
US2 after implementation: T012 (Node tests) || T013 (browser favorite management)
US3 after implementation: T016 (Node tests) || T017 (browser reload and failure flows)
US2 toast follow-up: T020 (toast markup) || T022 (toast CSS); then T021 and T023
US4: T024 (toggle markup) || T026 (collapse CSS); then T025 and T027
US4 drawer refinement: T029 -> T030 -> T031 -> T032
```

## Implementation Strategy

### MVP First

1. Complete setup and foundational page structure.
2. Complete User Story 1 and validate it independently; this is the first usable increment.
3. Add favorite management in User Story 2 and validate add/remove behavior.
4. Add reload restoration and error handling in User Story 3.
5. Complete the follow-up toast and collapsible-column stories.
6. Complete the keyboard, responsive, reduced-motion, and full quickstart checks.
7. Apply and verify the drawer direction and no-layout-jump refinements.

### Incremental Delivery

Each story adds a user-visible capability while preserving the prior story's behavior. Run the relevant Node and browser checks at each checkpoint; do not proceed past a failing checkpoint.
