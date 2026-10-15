# Interface Contract: Storage Adapter API

**Module**: `src/storage.js`  
**Target Consumer**: `src/app.js`, unit test suites  

---

## Factory: `createStorageAdapter(storageBackend = window.localStorage)`

Creates an isolated storage manager instance. Enables dependency injection of mock storage backends for headless automated testing.

- **Parameters**:
  - `storageBackend` (`StorageLike`, optional): An object providing `getItem(key)` and `setItem(key, value)`. Defaults to `window.localStorage` when running in browser.
- **Returns**: `StorageAdapter` instance.

---

## Methods on `StorageAdapter`

### `getFavorites()`
Retrieves the list of all currently favorited quote IDs.

- **Parameters**: None
- **Returns**: `string[]` (array of quote IDs)
- **Fault Tolerance**:
  - Catches `JSON.parse` syntax errors and returns `[]`.
  - Discards non-string or empty elements.
  - Catches storage permission errors (`SecurityError`) and returns cached in-memory state.

---

### `isFavorite(quoteId)`
Checks whether a given quote is marked as favorite.

- **Parameters**:
  - `quoteId` (`string`): Quote ID to check.
- **Returns**: `boolean` (`true` if favorited, `false` otherwise).

---

### `toggleFavorite(quoteId)`
Toggles the favorite status of the specified quote and persists the new state.

- **Parameters**:
  - `quoteId` (`string`): Quote ID to toggle.
- **Returns**: `boolean` (the new favorite state: `true` if now favorited, `false` if unfavorited).
- **Postconditions**:
  - If previously favorited, `quoteId` is removed from persistence and returns `false`.
  - If previously unfavorited, `quoteId` is added to persistence and returns `true`.
  - Stored value under `qotd_favorites_v1` is updated atomically.

---

### `clearFavorites()`
Removes all favorites from persistence and memory.

- **Parameters**: None
- **Returns**: `void`
- **Postconditions**: Storage key `qotd_favorites_v1` is updated to `[]` or removed.

