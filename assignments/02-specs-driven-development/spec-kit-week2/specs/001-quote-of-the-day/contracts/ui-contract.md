# Interface Contract: UI Presentation & DOM Elements

**Files**: `index.html`, `src/app.js`  
**Target Consumer**: Browser DOM, End-to-End verification  

---

## DOM Element Registry

| Element Selector / ID | Tag | Purpose | Required Attributes / ARIA |
|---|---|---|---|
| `#quote-card` | `<article>` | Container for the displayed quote | `class="quote-card"`, `aria-live="polite"` |
| `#quote-text` | `<blockquote>` | Text body of the active quote | Rendered inside `#quote-card` |
| `#quote-author` | `<cite>` | Author attribution of active quote | Rendered inside `#quote-card` |
| `#btn-new-quote` | `<button>` | Button to request a new quote | `id="btn-new-quote"`, `type="button"` |
| `#btn-favorite` | `<button>` | Button to toggle favorite status | `id="btn-favorite"`, `type="button"`, `aria-pressed="false|true"` |
| `#favorite-icon` | `<span>` / `svg` | Visual indicator inside favorite button | Displays filled/active vs. outline/inactive state |

---

## User Interaction Events

### Click on `#btn-new-quote`
1. Calls `getRandomQuote(currentQuoteId)` to obtain next quote.
2. Updates `#quote-text` textContent with `nextQuote.text`.
3. Updates `#quote-author` textContent with `nextQuote.author`.
4. Checks `storage.isFavorite(nextQuote.id)`.
5. Updates `#btn-favorite` attribute `aria-pressed` to `"true"` or `"false"` and updates visual icon accordingly.
6. Updates internal `currentQuoteId` pointer.

### Click on `#btn-favorite`
1. Calls `storage.toggleFavorite(currentQuoteId)`.
2. Receives new boolean state `isFav`.
3. Updates `#btn-favorite` attribute `aria-pressed` to `String(isFav)`.
4. Toggles active/filled styling class on `#btn-favorite` (e.g. `is-favorite`).

