# Page and Persistence Contract

## Page
- A native control in the favorites column remains available when the column is collapsed or expanded. It controls the column, exposes its state with `aria-expanded`, and keeps saved quotes unchanged when toggled.
- The favorites column starts expanded on page load. Collapsed state is presentation-only and is not persisted.
- A successful favorite add or removal shows a concise toast in a fixed overlay that does not block controls or shift page content. It is announced politely, disappears within five seconds, and is replaced with a restarted timeout if another successful favorite action occurs.
- Storage failures use the existing non-blocking error status and MUST NOT produce a success toast.
- Collapse and toast transitions use CSS only; reduced-motion preferences suppress or shorten their animation.
- The collapse chevron points right when a wide-screen drawer is collapsed and left when expanded; for the narrow-screen bottom drawer it points down when collapsed and up when expanded.
- During collapse or expansion, favorites remain mounted in an inner clipping wrapper while the outer wrapper's CSS grid row transitions between `1fr` and `0fr` with opacity. On wide screens, collapse content before resizing the column and reverse that order when expanding; on narrow screens, let the bottom drawer auto-size around the animated content. JavaScript MUST NOT measure `scrollHeight`, set inline heights, or hide transitioning content with `display: none`.

- The page presents exactly one quote at a time, including its attribution when available.
- A native **New quote** button requests a different quote from the built-in collection when at least two quotes exist.
- A native favorite toggle applies to the currently displayed quote. Its accessible name and pressed state communicate whether the quote is saved.
- A favorites section lists each saved quote with its attribution when available and a native remove control.
- The empty favorites section has a clear empty-state message.
- Quote changes and non-blocking storage status messages are announced politely to assistive technology. All actions are keyboard operable.

## Persistence

- **Storage key**: `daily-quote-favorites:v1`
- **Serialized value**: JSON array of stable quote ID strings, for example `["morning-light", "small-steps"]`.
- **Read behavior**: Validate the JSON shape, retain only unique IDs present in the built-in quote collection, and treat malformed or inaccessible values as unavailable saved data.
- **Write behavior**: Persist the updated unique ID array before reflecting a favorite toggle as successful.
- **Failure behavior**: Show a non-blocking message when favorites cannot be restored or saved. Quote selection remains available; failed writes do not falsely show a successful favorite change.
- **Scope**: Data is local to the same browser and device. There is no account, network API, or cross-device synchronization.
