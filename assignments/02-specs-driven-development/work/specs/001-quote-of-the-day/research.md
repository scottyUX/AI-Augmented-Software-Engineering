# Research & Technical Decisions: Quote of the Day

**Feature**: `001-quote-of-the-day`
**Date**: 2026-10-17
**Status**: Completed (Updated for Deterministic Daily Quote Selection)

## 1. Architecture & Modularity

### Decision
Use standard native HTML5, modern CSS3 (Custom Properties, Flexbox, CSS Grid), and native browser ES6 modules (`<script type="module">`). Separate code cleanly into:
- `data/`: Built-in quote collection.
- `services/`: Pure business logic (`QuoteService`, `StorageService`).
- `ui/`: DOM controllers and view rendering (`QuoteView`, `FavoritesView`).
- `app.js`: Root orchestrator binding UI events to services.

### Rationale
- **Zero Build Overhead**: Runs immediately by opening `index.html` or serving via any static web server (such as `npx serve` or Python `http.server`).
- **High Testability**: Pure business logic modules in `services/` have no direct DOM dependencies, enabling fast, isolated unit testing under standard automated test runners.
- **Maintainability & Modularity**: Adheres to the Single Responsibility Principle and Constitution Principle I/III (clean architecture, low cognitive load).

### Alternatives Considered
- **Monolithic Single File**: Putting all HTML, CSS, and JS in a single `index.html`. Rejected because it creates tight coupling, prevents isolated unit testing, and violates Constitution Principle I.
- **Frontend Frameworks (React/Vue/Svelte)**: Rejected per explicit user constraint ("Use plain HTML/CSS/JavaScript, no backend").

---

## 2. Persistence & Storage Strategy

### Decision
Use browser `window.localStorage` to store user favorites, wrapped within a dedicated `StorageService` that provides graceful degradation to in-memory storage if `localStorage` is disabled, inaccessible (e.g. strict privacy modes, incognito restrictions), or full.

### Rationale
- **User Requirement**: Explicitly requested `localStorage`.
- **Key Schema**: Store under the namespaced key `qod_favorites_v1`.
- **Fault Tolerance**: Wrapping access in `try / catch` blocks catches `SecurityError` and `QuotaExceededError`. When storage fails, the service falls back to in-memory state and triggers a non-intrusive UI notification (satisfying FR-013/FR-014).

### Alternatives Considered
- **IndexedDB**: Asynchronous and capable of larger datasets, but adds unnecessary complexity and asynchronous ceremony for storing a small list of quote IDs.
- **Cookies**: Inefficient and transmitted with every HTTP request; unnecessary for client-only offline state.
- **In-Memory Only**: Fails the requirement for persistence across reloads.

---

## 3. Deterministic Daily Quote Selection Algorithm

### Decision
Implement `QuoteService.getDailyQuote(date = new Date())` which deterministically extracts the local calendar date (`YYYY-MM-DD`) and computes a stable integer hash index:
```javascript
function getLocalDateKey(date) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}

function hashString(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) - hash) + str.charCodeAt(i);
    hash |= 0;
  }
  return Math.abs(hash);
}

// In QuoteService:
getDailyQuote(date = new Date()) {
  const key = getLocalDateKey(date);
  const hash = hashString(key);
  const index = hash % this._quotes.length;
  return this._quotes[index];
}
```

### Rationale
- **Deterministic & Idempotent**: For any visit on the same local calendar date (regardless of time of day or page reloads), `getLocalDateKey(date)` evaluates to the exact same string, yielding the identical quote.
- **Pure Function & Testable**: Accepting an optional `date` parameter enables deterministic unit testing for any date (e.g. testing leap days, year boundaries, consecutive days) without mocking global timers.
- **Decoupled from Server**: Requires zero external clock or network synchronization, operating seamlessly offline.

### Alternatives Considered
- **Day of Year Calculation (`dayOfYear % length`)**: Day of year repeats identically across non-leap years and doesn't salt year differences evenly. A 32-bit string hash of `"YYYY-MM-DD"` creates better dispersion year over year.
- **Caching in `localStorage`**: Caching the daily quote in storage creates stale cache issues if the user changes timezone, and requires extra storage synchronization. A pure deterministic mathematical function is stateless, instantaneous, and immune to cache invalidation bugs.

---

## 4. Quote Selection & Consecutive Repeat Prevention

### Decision
Implement `QuoteService.getRandomQuote(excludeId)` which selects a quote from the curated collection. If the collection contains 2 or more items and a quote is currently active (such as the daily quote or a previously clicked quote), the service excludes the currently active quote, guaranteeing that the next quote is never identical to the current quote.

### Rationale
- Satisfies FR-006 and Acceptance Scenario 2 of User Story 2.
- Handles edge cases cleanly: if collection size is 1, returns the single quote without crashing or infinite looping.

### Alternatives Considered
- **Random selection without exclusion**: Can result in the same quote being selected twice consecutively, producing poor user feedback when clicking "New quote".
- **Full Fisher-Yates Deck Shuffling**: Shuffles the whole array in advance. Slightly more complex state to track; tracking `excludeId` is cleaner and stateless.

---

## 5. Favorites Data Representation

### Decision
Store an array of lightweight record objects containing `quoteId` and `favoritedAt` ISO timestamp:
```json
[
  { "quoteId": "quote-001", "favoritedAt": "2026-10-17T02:15:00.000Z" }
]
```
At runtime, maintain a `Set<string>` of active favorite IDs for $O(1)$ lookup when rendering the active quote's favorite toggle state.

### Rationale
- Avoids duplicating quote text in storage; if quotes are enriched or formatted, storage data remains valid.
- Storing `favoritedAt` enables chronological sorting of favorites in the favorites list.

---

## 6. Accessibility & Responsive UX

### Decision
- **Semantic HTML**: `<main>`, `<article class="quote-card">`, `<blockquote>`, `<cite>`, and accessible `<button>` controls.
- **Screen Reader Announcements**: Use `aria-live="polite"` on the quote container so assistive technologies announce new quotes upon clicking "New quote".
- **Accessible Toggle**: Use `aria-pressed="true|false"` and descriptive `aria-label` (e.g., "Add quote to favorites" / "Remove quote from favorites").
- **Responsive Typography**: Fluid typography using CSS `clamp()` and modern system font stacks for fast load times and clean reading across all viewports from 320px to 4K displays.

---

## 7. Testing Strategy

### Decision
- **Unit Tests**: Test `QuoteService.getDailyQuote()` with multiple specific dates (asserting deterministic stability and date-to-date variation) and `QuoteService.getRandomQuote(excludeId)` using Node's built-in `node:test` and `node:assert`.
- **Integration Tests**: Verify that `initApp` renders the deterministic daily quote upon page load and syncs favorite state.
- **Manual Verification**: Follow `quickstart.md` scenarios for same-day reloads and "New quote" clicks.
