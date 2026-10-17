# Quote of the Day

A fast, lightweight, and accessible Quote of the Day web application built with plain HTML5, modern CSS3, and vanilla ES6 JavaScript modules. Zero external runtime dependencies, zero build steps, and full offline support.

## Features

- **Deterministic Daily Quote on Load**: Displays a consistent Quote of the Day on initial page visit, staying identical across all reloads on the same calendar day based on the user's local date.
- **On-Demand "New quote" Button**: Smoothly cycles to another quote chosen randomly from the built-in curated library without full-page reloads and guarantees no consecutive repeats.
- **Persistent Favoriting**: Toggle favorites with immediate visual feedback. Favorites are saved in browser `localStorage` and persist across page refreshes and browser restarts.
- **Favorites Drawer**: Dedicated slide-out drawer to view all accumulated favorite quotes, complete with one-click removal and empty state handling.
- **Graceful Storage Degradation**: Automatically falls back to in-memory session storage if `localStorage` is disabled or blocked in strict privacy modes, accompanied by a polite accessibility notification.
- **Accessible (WCAG 2.1 AA)**: Semantic HTML structure, high-contrast color palette ($\ge 4.5:1$), keyboard-operable controls, visible focus indicators, and screen reader announcements via `aria-live="polite"`.

---

## Project Structure

```text
├── src/
│   ├── index.html                   # Semantic HTML5 entry page
│   ├── css/
│   │   ├── styles.css               # Design tokens, reset, and layout grid
│   │   └── components.css           # Quote card, buttons, and drawer styling
│   └── js/
│       ├── app.js                   # Application coordinator & event wiring
│       ├── data/
│       │   └── quotes.js            # Curated library of 26 diverse quotes
│       ├── services/
│       │   ├── quote-service.js     # Pure business logic: random selection & no-repeat
│       │   └── storage.js           # Persistence manager: localStorage + in-memory fallback
│       └── ui/
│           ├── quote-view.js        # Quote card DOM rendering and ARIA state
│           └── favorites-view.js    # Favorites drawer/list DOM rendering & removal
├── tests/
│   ├── unit/
│   │   ├── quote-service.test.js    # Unit tests for selection & no-repeat logic
│   │   ├── storage.test.js          # Unit tests for localStorage serialization & fallbacks
│   │   └── favorites-view.test.js   # Unit tests for favorites drawer UI
│   └── integration/
│       ├── quote-view.test.js       # Integration tests for initial quote rendering
│       ├── favorite-toggle.test.js  # Integration tests for favorite toggling & persistence
│       └── app-workflow.test.js     # End-to-end user scenario tests
├── specs/                           # Spec Kit specifications, plans, and tasks
└── package.json                     # Project manifest and test runner script
```

---

## Running the Application

Because this application uses native web technologies without build steps, you can serve it with any local static HTTP server:

```bash
# Option 1: Using Node.js (via package.json script)
npm.cmd start
# or: node -e "..." (defined in package.json)

# Option 2: Using Python built-in server
python -m http.server 8080 --directory src

# Option 3: Using npx serve
npx serve src -p 8080
```

Once running, navigate to `http://localhost:8080` in your browser.

---

## Running Automated Tests

The automated test suite runs via Node's native test runner (`node:test`):

```bash
# Run all unit and integration tests
npm.cmd test
# or directly:
node --test tests/**/*.test.js
```
