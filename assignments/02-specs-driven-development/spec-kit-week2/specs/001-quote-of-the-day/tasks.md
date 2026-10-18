# Tasks: Quote of the Day

**Input**: Design artifacts from `specs/001-quote-of-the-day/`  
**Branch**: `001-quote-of-the-day`  
**Feature Directory**: `specs/001-quote-of-the-day`  

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, directory structure, and foundational UI markup

- [X] T001 Create project directories for source code and tests in `src/` and `tests/unit/`
- [X] T002 [P] Create HTML entrypoint with semantic structure (`#quote-card`, `#quote-text`, `#quote-author`, `#btn-new-quote`, `#btn-favorite`, `#favorite-icon`, `aria-live="polite"`, `aria-pressed="false"`) and ES module linkage in `index.html`
- [X] T003 [P] Create modern responsive styles, card layout, button states, focus rings, and favorite active styling in `style.css`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core quote catalog and domain definitions required across all user stories

**⚠️ CRITICAL**: Must be completed before user story implementation begins.

- [X] T004 Create quote catalog data array in `src/quotes.js` containing at least 8 curated quotes, enforcing verbatim constraints: "`id` must be unique non-empty string", "`text` must not be empty or whitespace-only", and "`author` must not be empty or whitespace-only"
- [X] T005 [P] Implement domain query functions `getAllQuotes()` and `getQuoteById(id)` in `src/quotes.js` per `specs/001-quote-of-the-day/contracts/quotes-contract.md`

**Checkpoint**: Core quote data layer available; user story implementation can begin.

---

## Phase 3: User Story 1 - View and Discover Quotes (Priority: P1) 🎯 MVP

**Goal**: Deliver a functioning Quote of the Day page where visitors view an inspiring quote and author on load, and can click "New quote" to display a different quote without immediate repetition.

**Independent Test**: Load `index.html` to confirm quote text and author appear; click "New quote" to confirm the quote updates to a different quote. Run `node --test tests/unit/quotes.test.js`.

### Tests for User Story 1 🧪
> **NOTE: Write these tests FIRST, ensure they fail before implementing T007**

- [X] T006 [P] [US1] Create unit tests in `tests/unit/quotes.test.js` validating that `getAllQuotes()` returns the full catalog conforming to schema, `getRandomQuote()` returns a valid quote, and `getRandomQuote(excludeId)` never returns `excludeId` when catalog length > 1

### Implementation for User Story 1

- [X] T007 [US1] Implement pure `getRandomQuote(excludeId = null)` function in `src/quotes.js` per `specs/001-quote-of-the-day/contracts/quotes-contract.md`
- [X] T008 [US1] Implement initial quote display and "New quote" button click event listener in `src/app.js` to render active quote into `#quote-text` and `#quote-author` per `specs/001-quote-of-the-day/contracts/ui-contract.md`

**Checkpoint**: User Story 1 complete and independently testable as a standalone MVP!

---

## Phase 4: User Story 2 - Favorite and Unfavorite Quotes (Priority: P2)

**Goal**: Allow users to toggle the favorite state of the active quote with immediate visual feedback (`aria-pressed` and icon style change) and synchronize favorite state during quote rotation.

**Independent Test**: View a quote, click Favorite to toggle active state (`aria-pressed="true"`), click again to unfavorite (`aria-pressed="false"`), and cycle quotes to verify the favorite indicator matches the active quote.

### Tests for User Story 2 🧪
> **NOTE: Write these tests FIRST, ensure they fail before implementing T010**

- [X] T009 [P] [US2] Create unit tests in `tests/unit/storage.test.js` verifying `toggleFavorite(id)`, `isFavorite(id)`, and state transitions between Favorited and Unfavorited using an in-memory storage mock

### Implementation for User Story 2

- [X] T010 [US2] Implement `createStorageAdapter` factory in `src/storage.js` with in-memory state tracking, `isFavorite(quoteId)`, and `toggleFavorite(quoteId)` methods per `specs/001-quote-of-the-day/contracts/storage-contract.md`
- [X] T011 [US2] Connect favorite button click handler and state synchronization in `src/app.js` to toggle favorite state on `#btn-favorite`, update `aria-pressed`, and update favorite icon when switching quotes

**Checkpoint**: User Story 2 functional; favorite state toggles interactively and syncs across quote changes.

---

## Phase 5: User Story 3 - Persist Favorites Across Sessions (Priority: P3)

**Goal**: Persist favorited quote IDs under key `qotd_favorites_v1` in `localStorage`, maintaining favorites across page reloads and recovering gracefully from corrupt or restricted storage.

**Independent Test**: Favorite a quote, reload the page, cycle quotes, and verify the quote remains favorited. Corrupt storage in DevTools and verify the app recovers without crashing.

### Tests for User Story 3 🧪
> **NOTE: Write these tests FIRST, ensure they fail before implementing T013**

- [X] T012 [P] [US3] Add unit tests in `tests/unit/storage.test.js` verifying `localStorage` serialization, schema sanitization (filtering non-string items), fallback when `localStorage` throws `SecurityError` or `QuotaExceededError`, and recovery from malformed JSON

### Implementation for User Story 3

- [X] T013 [US3] Implement `localStorage` read/write serialization, schema sanitization, and error recovery (`try/catch` with in-memory fallback) in `src/storage.js` for key `qotd_favorites_v1`
- [X] T014 [US3] Integrate persistent storage adapter initialization on page load in `src/app.js` to hydrate saved favorites before initial quote render

**Checkpoint**: All three user stories operational; favorites persist across reloads and handle storage failures defensively.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Verification, accessibility, and documentation validation

- [X] T015 [P] Add keyboard accessibility styling, focus rings, hover transitions, and responsive layout polish in `style.css`
- [X] T016 Run full automated test suite via `node --test tests/unit/*.test.js` and execute end-to-end scenarios per `specs/001-quote-of-the-day/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately; no dependencies.
- **Foundational (Phase 2)**: Depends on Setup (Phase 1) - blocks User Story 1.
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2). Delivers standalone MVP.
- **User Story 2 (Phase 4)**: Depends on User Story 1 completion for UI integration.
- **User Story 3 (Phase 5)**: Extends storage adapter from User Story 2 with durable persistence.
- **Polish (Phase 6)**: Executes after all user stories are implemented.

### Parallel Opportunities

- `T002` (HTML shell) and `T003` (CSS styles) can execute in parallel.
- `T005` (Domain query functions) can execute in parallel once `T004` data model exists.
- `T006` (US1 tests) can run in parallel with UI/CSS setup.
- `T009` (US2 storage mock tests) can run in parallel with US1 UI wiring.
- `T012` (US3 persistence tests) can run in parallel before storage serialization implementation.

---

## Parallel Example: User Story 1

```bash
# Launch test creation and initial structure in parallel:
Task T006: "Create unit tests in tests/unit/quotes.test.js"
Task T002: "Create HTML entrypoint in index.html"
Task T003: "Create modern responsive styles in style.css"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)
1. Complete Phase 1 (Setup) and Phase 2 (Foundational).
2. Write tests for US1 in `tests/unit/quotes.test.js` (T006).
3. Implement `src/quotes.js` (T007) and `src/app.js` (T008).
4. **Validate MVP**: Load `index.html` to confirm quotes display and rotate on click.

### Incremental Delivery
1. Add User Story 2: Implement favorite button and active state toggle in memory.
2. Add User Story 3: Implement durable `localStorage` persistence with defensive fallback.
3. Polish & Validate: Run `node --test tests/unit/*.test.js` and verify end-to-end scenarios.

