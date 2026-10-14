# Research: Daily Quote Favorites

## Decisions

### Browser-native static application

- **Decision**: Use semantic HTML, CSS, and native JavaScript ES modules, with no runtime dependencies or backend.
- **Rationale**: This directly follows the requested stack and keeps the page small, understandable, and deployable as static files.
- **Alternatives considered**: A frontend framework or a server-rendered application. Both add tooling or services that are unnecessary for one page with a fixed collection and local preferences.

### Persist favorite quote IDs in localStorage

- **Decision**: Store a JSON array of stable quote IDs under a namespaced, versioned key (`daily-quote-favorites:v1`).
- **Rationale**: Favorites must survive reloads in the same browser and device; the built-in quote collection means the page only needs to persist references, not duplicate quote text.
- **Alternatives considered**: Cookies, a server database, and persisting the complete quote records. Cookies are not intended for this client-side preference; a database requires a backend and account model; duplicating quote records increases state and validation work.
- **Failure handling**: Invalid stored data is not trusted. Storage read/write failures produce a non-blocking status and must not prevent quote browsing.

### Separate pure state logic from page rendering

- **Decision**: Put quote selection and favorite parsing/validation in `src/quote-state.mjs`; keep DOM updates and event wiring in `src/app.mjs`.
- **Rationale**: Pure helpers can be exercised without a browser while the page remains a simple native module application.
- **Alternatives considered**: Put all behavior in one script or introduce a state-management package. A small module boundary enables focused tests without a framework or package dependency.

### Use built-in Node tests plus browser acceptance checks

- **Decision**: Use Node's built-in `node:test` for deterministic state logic tests and a real browser for accessibility, display, and reload scenarios.
- **Rationale**: This gives repeatable checks for edge cases without adding a test dependency; browser checks cover behavior that pure unit tests cannot prove.
- **Alternatives considered**: Add a browser automation framework. That is disproportionate for this static page and is not needed to verify the specified flows.

## Resolved Unknowns

### Collapsible panel state

- **Decision**: Use a native button with `aria-expanded` and `aria-controls` to toggle the favorites column's collapsed state. At wide viewports, the right-side drawer uses a right-pointing chevron when collapsed and a left-pointing chevron when expanded. At narrow viewports, the bottom drawer uses down when collapsed and up when expanded.
- **Rationale**: The direction indicates where the drawer will open or the direction it can be closed toward. Collapse is presentation state and must not modify persisted favorites.
- **Motion behavior**: Keep the favorites content mounted in an inner clipping wrapper. Transition the outer wrapper's grid row from `0fr` to `1fr` with opacity. At wide viewports, finish the content transition before changing column width; reverse that order on expansion to avoid reflow while text is visible. At narrow viewports, allow the panel to auto-size around the animated track rather than forcing a fixed height. JavaScript toggles classes and ARIA state only, without reading layout dimensions or writing measured heights. Respect `prefers-reduced-motion`.
- **Alternatives considered**: A UI framework, animation library, JavaScript height measurement, or toggling `display`. These add dependencies, cause forced layout or abrupt visibility changes, or duplicate behavior already handled by CSS.

### Temporary success notifications

- **Decision**: Show at most one fixed-position, polite live-region toast after a successful favorite add or removal. It does not occupy document flow and disappears within five seconds; a newer successful action replaces its message and restarts its dismissal timer.
- **Rationale**: This confirms the result without blocking quote browsing, shifting content, or stacking notices. Failed persistence remains communicated by the existing error status, not a success toast.
- **Alternatives considered**: Modal dialogs, blocking alerts, and stacked notifications. These are more disruptive than the requested feedback.

The requested technology stack, storage mechanism, and no-backend constraint are explicit. The feature has no external service integrations or unresolved technical choices. Node.js is used only to run tests and is not needed by visitors at runtime.
