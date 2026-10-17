# Contract: StorageService

**Path**: `src/js/services/storage.js`
**Interface Type**: Persistence Abstraction Service

## Class: `StorageService`

### `constructor(storageBackend = window.localStorage)`
Initializes the storage manager with a storage implementation. Automatically tests read/write capability; falls back to an internal in-memory map if the backend is disabled or throws `SecurityError`.

---

### `getFavorites(): FavoriteRecord[]`
Retrieves all stored favorites.
- **Behavior**:
  - Reads `qod_favorites_v1` key.
  - Parses JSON; validates array format.
  - If parsing fails or data is corrupted, returns `[]` and resets corrupted key.
- **Returns**: `FavoriteRecord[]` (array of `{ quoteId: string, favoritedAt: string }`)

---

### `isFavorite(quoteId: string): boolean`
Checks whether a specific quote is currently marked as favorite.
- **Parameters**:
  - `quoteId` *(string)*: Unique identifier of quote.
- **Returns**: `boolean`

---

### `addFavorite(quoteId: string): boolean`
Marks a quote as favorite.
- **Parameters**:
  - `quoteId` *(string)*: Identifier to add.
- **Behavior**:
  - If `quoteId` is already present, does not add duplicate.
  - Appends new record `{ quoteId, favoritedAt: new Date().toISOString() }`.
  - Serializes and stores to backend.
- **Returns**: `boolean` (`true` if successfully added/already exists, `false` if storage write failed).

---

### `removeFavorite(quoteId: string): boolean`
Removes a quote from favorites.
- **Parameters**:
  - `quoteId` *(string)*: Identifier to remove.
- **Behavior**:
  - Filters out records with matching `quoteId`.
  - Serializes updated list and stores to backend.
- **Returns**: `boolean` (`true` if successfully removed, `false` if storage write failed).

---

### `isPersistent(): boolean`
Reports whether data is being persisted to durable storage or running in in-memory session mode.
- **Returns**: `boolean` (`true` if backed by functional `localStorage`, `false` if fallback memory).
