# Interface Contract: Quotes Domain API

**Module**: `src/quotes.js`  
**Target Consumer**: `src/app.js`, unit test suites  

---

## Functions

### `getAllQuotes()`
Returns an array of all curated quote objects available in the built-in catalog.

- **Parameters**: None
- **Returns**: `Array<{ id: string, text: string, author: string }>`
- **Preconditions**: None
- **Postconditions**: Returns an immutable or cloned array of at least 8 quote items. Each item conforms to the `Quote` entity schema.

---

### `getQuoteById(id)`
Retrieves a single quote matching the specified unique ID.

- **Parameters**:
  - `id` (`string`): The unique identifier of the quote.
- **Returns**: `{ id: string, text: string, author: string } | null`
- **Behavior**: Returns the matching quote object, or `null` if no quote with `id` exists.

---

### `getRandomQuote(excludeId = null)`
Selects a random quote from the catalog, avoiding `excludeId` when the catalog contains multiple items.

- **Parameters**:
  - `excludeId` (`string | null`, optional): The ID of the currently displayed quote to exclude from selection. Default is `null`.
- **Returns**: `{ id: string, text: string, author: string }`
- **Behavior**:
  - If `excludeId` is provided and the catalog contains 2 or more quotes, the returned quote's `id` MUST NOT equal `excludeId`.
  - If the catalog has only 1 item, returns that item.
  - If the catalog is empty (error case), throws an `Error("Quote catalog cannot be empty")`.

