# Quickstart & Validation Guide: Quote of the Day

**Feature**: Quote of the Day (`001-quote-of-the-day`)  
**Date**: 2026-10-15  
**Status**: Completed  

---

## Prerequisites

- **Node.js**: v18+ (verified with current environment Node v24) for running automated tests.
- **Web Browser**: Any modern browser (Chrome, Edge, Firefox, Safari).
- **Optional Static Server**: Python 3 (`python -m http.server`) or Node http-server. Opening `index.html` directly in the browser also works since assets are self-contained.

---

## 1. Automated Test Execution

Run the zero-dependency test suite via Node.js built-in test runner:

```bash
node --test tests/unit/*.test.js
```

### Expected Output
- All tests pass (quotes catalog integrity, non-repeating random selection, storage serialization, error handling, in-memory fallback, and favorite toggling).
- Exit code `0`.

---

## 2. Launching the Application

### Option A: Local HTTP Server (Recommended)
```bash
python -m http.server 8000
```
Open `http://localhost:8000` in your browser.

### Option B: Direct File Open
Open `index.html` directly in your browser.

---

## 3. End-to-End Validation Scenarios

### Scenario 1: Initial Render & Quote Rotation
1. Open the page.
2. **Verify**: A quote text and author attribution appear immediately.
3. Click the **"New quote"** button.
4. **Verify**: A new quote appears without delay, different from the initial quote.

### Scenario 2: Favoriting a Quote
1. On the currently displayed quote, click the **Favorite** button.
2. **Verify**: The favorite button icon highlights (filled heart/star), and `aria-pressed="true"`.
3. Click the **"New quote"** button until an unfavorited quote is displayed.
4. **Verify**: The favorite button reflects an unfavorited state (outline, `aria-pressed="false"`).

### Scenario 3: Reload Persistence
1. Mark the currently visible quote as favorite.
2. Note the quote text and author.
3. Refresh the page in the browser (`Ctrl+R` / `Cmd+R`).
4. Click **"New quote"** until the favorited quote reappears.
5. **Verify**: The quote is still marked as favorite with the filled icon and `aria-pressed="true"`.

### Scenario 4: Storage Error Resilience
1. In the browser Developer Tools Console (`F12`), corrupt the storage:
   ```javascript
   localStorage.setItem('qotd_favorites_v1', '{corrupt json]');
   ```
2. Refresh the page.
3. **Verify**: The application loads normally without unhandled exceptions or blank screen; favorites reset gracefully.

