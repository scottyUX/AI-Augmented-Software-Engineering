# Technical Research & Decisions: Quote of the Day

**Feature**: Quote of the Day (`001-quote-of-the-day`)  
**Date**: 2026-10-15  
**Status**: Completed  

---

## 1. Storage & Persistence Architecture

### Decision
Implement a dedicated `storage.js` adapter module wrapping browser `localStorage` with safe error-handling, schema validation, and in-memory fallback. The storage key used will be `qotd_favorites_v1`, storing a JSON-serialized array of quote IDs (strings).

### Rationale
- **User Requirement**: Fulfills the constraint "persist favorites in localStorage" and "no backend".
- **Constitution Compliance**:
  - *Principle I (Modularity)*: Encapsulates all storage operations away from presentation logic.
  - *Principle IV (Robust Error Handling)*: Protects against private browsing restrictions (`SecurityError`), quota limits, and malformed JSON data by catching exceptions and gracefully falling back to an in-memory Set.
  - *Principle II (Testability)*: The storage adapter can accept a mock storage interface, allowing automated testing in headless environments (like `node:test`) without requiring a browser.

### Alternatives Considered
- **Direct `localStorage` calls inside UI handlers**: Rejected because it creates tight coupling, duplicates error handling, and makes headless automated unit testing difficult.
- **IndexedDB**: Rejected because it adds asynchronous API complexity that is unnecessary for a lightweight list of favorite IDs (violates Principle III / YAGNI).
- **Document Cookies**: Rejected due to size limits, cookie header transmission overhead, and lack of utility without a server.

---

## 2. Quote Catalog & Selection Engine

### Decision
Store a built-in collection of 10 curated quotes in `src/quotes.js`. Provide pure helper functions:
- `getAllQuotes()`: Returns the static catalog.
- `getQuoteById(id)`: Returns the quote matching the given ID or `null`.
- `getRandomQuote(excludeId = null)`: Pure function returning a randomly selected quote from the catalog, guaranteed not to match `excludeId` unless the catalog has only 1 item.

### Rationale
- **Testability**: Pure selection logic is completely decoupled from DOM and browser APIs, making it simple to unit-test with high test coverage.
- **User Experience**: Passing `excludeId` prevents the jarring experience of clicking "New quote" and seeing the exact same quote re-rendered.
- **Offline / Zero Setup**: Embedding the data directly in an ES module allows the application to run immediately when opened locally (via `file://` or local HTTP server) without CORS fetch restrictions.

### Alternatives Considered
- **Fetching quotes from an external REST API**: Rejected because it introduces an external network failure mode, breaks offline capability, and conflicts with the requirement for a "built-in list".
- **External quotes.json loaded via `fetch()`**: Rejected because `fetch()` to local files (`file:///`) is blocked by browser CORS security policies in standard configurations, complicating local development and review.

---

## 3. Architecture & Modular Boundaries

### Decision
Adopt a modular vanilla ES module architecture organized into distinct single-responsibility files:
- `index.html`: Semantic markup and accessible structure.
- `style.css`: Clean, responsive modern CSS (Flexbox/CSS Grid, system font stack, high-contrast states).
- `src/quotes.js`: Quote catalog and pure selection algorithms.
- `src/storage.js`: Persistence layer with defensive JSON parsing and memory fallback.
- `src/app.js`: Application coordinator, DOM rendering, and event binding.

### Rationale
- Fulfills the constraint: "Use plain HTML/CSS/JavaScript, no backend".
- Satisfies Constitution Principle I (Code Quality & Modularity) by enforcing separation of concerns between presentation, state persistence, and domain data.
- Does not require a compiler, bundler, or build pipeline.

### Alternatives Considered
- **Single monolithic HTML file with inline script**: Rejected because it tangles data, storage, and DOM logic, violating modularity and maintainability.
- **Frontend Framework (React, Vue, Svelte)**: Rejected as explicitly out of scope per user requirements; adds unnecessary dependencies and build steps.

---

## 4. Automated Testing Strategy

### Decision
Use the built-in Node.js test runner (`node:test` + `node:assert/strict`) to execute automated unit and contract tests in `tests/`.

### Rationale
- Node.js v24 is already available in the execution environment.
- `node:test` is zero-dependency: requires no `npm install`, `package.json`, or external test framework dependencies.
- Executes tests in sub-second time, enabling continuous test-driven validation.
- Validates pure domain logic (`quotes.test.js`) and persistence edge cases (`storage.test.js` using mock storage).

### Alternatives Considered
- **Jest / Vitest**: Rejected because they require npm package installation, package configuration, and node_modules overhead, violating Principle III (Maintainability & Simplicity).
- **Manual-only testing in browser**: Rejected because Constitution Principle II strictly mandates automated verification for business logic and persistence.

---

## 5. Accessibility & Semantic UI Standards

### Decision
Structure the UI with semantic HTML5 elements:
- `<main>` for primary content landmark.
- `<article class="quote-card" aria-live="polite">` for the quote container so assistive technology announces quote updates.
- `<blockquote>` and `<cite>` for standard quote typography.
- `<button id="btn-favorite" aria-pressed="true|false">` for the favorite toggle, ensuring screen readers announce toggle state.
- Keyboard accessible controls with visible `:focus-visible` styling.

### Rationale
- Meets modern web accessibility standards without adding external UI libraries or dependencies.

