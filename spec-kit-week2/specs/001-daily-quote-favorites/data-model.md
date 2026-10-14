# Data Model: Daily Quote Favorites

## Quote

A built-in collection entry shown to the visitor.

| Field | Type | Rules |
|---|---|---|
| `id` | string | Stable and unique within the collection; used to identify favorites. |
| `text` | string | Required and non-empty. |
| `attribution` | string or absent | Optional author or source; omit when unavailable. |

The collection is fixed for the page version and contains at least two distinct quote entries. A quote's ID must remain stable when its text and attribution have not changed.

## Favorite

A visitor's saved reference to a built-in quote.

| Field | Type | Rules |
|---|---|---|
| `quoteId` | string | Must match an ID in the built-in quote collection. A quote can occur at most once. |

Favorites are private to the current browser and device. They are represented in persistent storage as a JSON array of quote ID strings under `daily-quote-favorites:v1`.

## Runtime State
- `favoritesPanelExpanded`: in-memory presentation state, initially expanded on each page load; changing it does not alter or persist favorite data.
- `toastMessage`: at most one temporary success message for the latest favorite add or removal; it is not persisted.

- `currentQuoteId`: ID of the one quote currently displayed; selected on page load and changed by the New quote action.
- `favoriteQuoteIds`: unique IDs of favorites that also exist in the built-in collection.
- `storageStatus`: normal, restored-data warning, or save failure; warnings do not block quote selection.

## State Transitions and Validation
- Collapsing or expanding the favorites column changes presentation only and leaves `favoriteQuoteIds` unchanged.
- A successful add or removal shows a toast for no more than five seconds. A newer successful action replaces the current message and restarts its dismissal period; a failed action does not show a success toast.

- Initial load selects one quote from the built-in collection. When there are multiple entries, the next selection excludes the currently displayed ID.
- Activating the favorite control adds the current ID if absent or removes it if present. The saved state and UI state change only after persistence succeeds.
- Loading favorites accepts only an array of known string IDs, removes duplicates, and rejects malformed data. A read error or malformed value yields an empty in-memory favorite list and a visible non-blocking warning.
- Saving serializes the unique favorite IDs. If storage is unavailable or the write fails, preserve the prior in-memory list and show a non-blocking error.
- With a one-entry quote collection, requesting a new quote leaves the current ID unchanged.
