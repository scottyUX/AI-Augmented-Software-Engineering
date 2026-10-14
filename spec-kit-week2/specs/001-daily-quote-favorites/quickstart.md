# Quickstart: Daily Quote Favorites

## Prerequisites

- A modern browser with JavaScript modules and `localStorage` enabled.
- Python 3 to serve the static files locally.
- Node.js 18 or newer to run the built-in test suite. Node.js is test-only and is not required at runtime.

## Run the Page

From the repository root, start a static file server:

```powershell
python -m http.server 8000
```

Open `http://localhost:8000` in a browser. This serves static files only; the application has no backend. Use an HTTP origin rather than opening `index.html` directly so browser modules and persistent storage behave consistently.

## Run Automated Tests

From the repository root, run:

```powershell
node --test
```

Expected result: all quote-selection and favorite-data tests pass, including invalid and unavailable storage cases.

## Browser Acceptance Checks

1. Reload the page and verify exactly one quote from the built-in collection is visible.
2. Activate **New quote** several times. Each quote must belong to the collection and must not immediately repeat when the collection has multiple entries.
3. Save the displayed quote. Verify its saved state and its entry in the favorites section.
4. Activate **New quote** until the saved quote appears again. Verify its saved state remains active and no duplicate was added.
5. Reload the page. Verify saved favorites remain listed. Remove one favorite, reload again, and verify it remains absent.
6. With keyboard only, reach and activate **New quote**, the favorite toggle, and a favorite removal control. Verify the current state and status messages are announced accessibly.
7. Clear site data for `localhost:8000` and reload. Verify the page displays a quote and an empty-favorites state.
8. At a wide viewport, activate the favorites-column control with mouse and keyboard. Verify the chevron points right while collapsed and left while expanded, `aria-expanded` updates, and saved quotes remain unchanged.
9. At a narrow viewport, repeat the collapse and expand checks. Verify the bottom drawer chevron points down while collapsed and up while expanded.
10. Toggle the drawer repeatedly during its transition. Verify content remains mounted and clips smoothly without a height jump, flicker, or lost saved entries; verify JavaScript does not measure or assign content height.
11. Add a favorite and remove a favorite. Verify each successful action produces one polite, non-blocking toast that does not shift the page and disappears within five seconds. Trigger another successful action while a toast is visible and verify the message updates without stacking.
12. Simulate a storage write failure. Verify an error status appears, no success toast is shown, and quote browsing remains available.
13. Enable reduced motion in operating-system or browser preferences and repeat the collapse and toast checks. Verify the feature remains usable without relying on animation.

For a storage failure check, block site storage in the browser or use the injected storage failure cases in the automated tests. The page must continue to allow quote browsing and report the favorite persistence failure without claiming it was saved.
