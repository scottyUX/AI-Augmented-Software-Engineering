# Implementation Plan: Daily Quote Favorites

**Branch**: `001-daily-quote-favorites` | **Date**: 2026-10-14 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-daily-quote-favorites/spec.md`

## Summary

Build a single-page quote experience using plain HTML, CSS, and JavaScript modules.
The page selects from a small built-in collection, lets visitors request another
quote, and saves favorite quote IDs in browser `localStorage`. Visitors can collapse
the favorites column without changing saved data. Successful add/remove actions show
a temporary, non-blocking toast. These UI states use vanilla JavaScript and CSS
transitions, respecting the `prefers-reduced-motion` preference. There is no backend, account,
or runtime dependency. Automated tests use Node's built-in test runner for quote
selection and favorite-data handling; end-to-end behavior is verified in a browser.

## Technical Context

**Language/Version**: Browser-native JavaScript (ES modules), HTML, and CSS

**Primary Dependencies**: None at runtime; browser APIs only

**Storage**: `localStorage` under a versioned, feature-specific key

**Testing**: Node.js built-in `node:test` for state helpers; browser acceptance checks

**Target Platform**: Modern browsers with ES module, DOM, and `localStorage` support

**Project Type**: Static web application

**Performance Goals**: Quote selection and favorite interactions update immediately without network requests

**Constraints**: Plain HTML/CSS/JavaScript; no backend; favorites persist in `localStorage`; handle unavailable or invalid saved data without disabling quote browsing; collapse and toast interactions use CSS transitions and native DOM events only

**Scale/Scope**: One page, a small fixed quote collection, one active quote, and a small per-browser favorites collection

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Clear, Correct Implementation**: Pass. Keep quote/state logic named and separate from DOM rendering; make UI states explicit.
- **Behavior-Focused Testing**: Pass. Cover selection, favorite validation, persistence, failure paths, collapse state, toast lifecycle, and keyboard/browser flows.
- **Simple, Maintainable Design**: Pass. Use native browser APIs and Node's built-in test runner; add no runtime packages, framework, or backend.
- **Accessible and Resilient Interaction**: Pass. Use native buttons, keyboard operation, announced quote/status updates, expanded-state semantics, reduced-motion support, and fallback behavior for storage errors.
- **Traceable Scope and Decisions**: Pass. The design maps directly to the reviewed requirements and introduces no account, server, or unrelated feature.

## Project Structure

### Documentation (this feature)

```text
specs/001-daily-quote-favorites/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── page-and-persistence.md
├── checklists/
│   └── requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
index.html
styles.css
src/
├── app.mjs
└── quote-state.mjs
tests/
└── quote-state.test.mjs
```

**Structure Decision**: Keep the static page entry point and stylesheet at the
repository root. Put the browser UI module and pure quote/favorite state helpers in
`src/`; keep the collapsible panel and toast lifecycle in the page module, with
transitions in `styles.css`. Exercise pure helpers with Node's built-in test runner.
No backend, UI library, animation dependency, build tooling, or package manifest is
needed.

The drawer toggle's chevron points toward the action: right when the desktop drawer
is collapsed and left when it is expanded; down when the narrow-screen drawer is
collapsed and up when it is expanded. The favorites content remains mounted while
animating in an inner clipping wrapper. Transition the outer content wrapper's CSS
grid row from `0fr` to `1fr` with opacity, and animate desktop grid columns in CSS.
On wide viewports, collapse the content before resizing the column; on expansion,
resize the column before revealing the content so text does not reflow mid-animation.
On narrow viewports, animate the bottom drawer content without a fixed panel height.
JavaScript changes state classes and ARIA attributes only; it MUST NOT measure
content height, write inline heights, or switch the transitioning content to
`display: none`.

## Complexity Tracking

No constitution violations or additional architectural complexity require justification.
