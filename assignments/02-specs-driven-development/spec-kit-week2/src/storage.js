/**
 * Storage adapter for Quote of the Day favorites.
 * Handles persistence, schema validation, and fallback mechanisms.
 */

export const STORAGE_KEY = "qotd_favorites_v1";

/**
 * Creates an in-memory storage fallback.
 * @returns {Storage}
 */
function createMemoryStorage() {
  const memoryStore = new Map();
  return {
    getItem(key) {
      return memoryStore.has(key) ? memoryStore.get(key) : null;
    },
    setItem(key, value) {
      memoryStore.set(key, String(value));
    },
    removeItem(key) {
      memoryStore.delete(key);
    },
    clear() {
      memoryStore.clear();
    }
  };
}

/**
 * Sanitizes raw data retrieved from storage into a valid set of quote IDs.
 * @param {string | null} raw
 * @returns {Set<string>}
 */
function parseAndSanitize(raw) {
  if (!raw || typeof raw !== "string") {
    return new Set();
  }

  try {
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) {
      return new Set();
    }

    const validIds = parsed.filter(
      item => typeof item === "string" && item.trim().length > 0
    );
    return new Set(validIds);
  } catch {
    return new Set();
  }
}

/**
 * Creates a storage adapter instance.
 * @param {Storage} [storageBackend] - Optional storage implementation (defaults to window.localStorage in browser)
 */
export function createStorageAdapter(storageBackend) {
  let backend = storageBackend;

  if (!backend && typeof window !== "undefined" && window.localStorage) {
    try {
      backend = window.localStorage;
    } catch {
      backend = createMemoryStorage();
    }
  }

  if (!backend) {
    backend = createMemoryStorage();
  }

  let inMemoryFavorites = new Set();

  // Initial load
  try {
    const raw = backend.getItem(STORAGE_KEY);
    inMemoryFavorites = parseAndSanitize(raw);
  } catch {
    inMemoryFavorites = new Set();
  }

  /**
   * Persists the current in-memory favorites set to the storage backend.
   */
  function persist() {
    try {
      const data = JSON.stringify([...inMemoryFavorites]);
      backend.setItem(STORAGE_KEY, data);
    } catch (err) {
      // Gracefully continue using in-memory state on quota or security errors
      console.warn("Storage write failed; keeping state in-memory:", err);
    }
  }

  return {
    /**
     * Returns an array of all currently favorited quote IDs.
     * @returns {string[]}
     */
    getFavorites() {
      return [...inMemoryFavorites];
    },

    /**
     * Checks whether a specific quote is marked as favorite.
     * @param {string} quoteId
     * @returns {boolean}
     */
    isFavorite(quoteId) {
      if (!quoteId || typeof quoteId !== "string") {
        return false;
      }
      return inMemoryFavorites.has(quoteId);
    },

    /**
     * Toggles the favorite status of a quote.
     * @param {string} quoteId
     * @returns {boolean} The new favorite status (true if favorited, false if unfavorited)
     */
    toggleFavorite(quoteId) {
      if (!quoteId || typeof quoteId !== "string") {
        return false;
      }

      const isFav = inMemoryFavorites.has(quoteId);
      if (isFav) {
        inMemoryFavorites.delete(quoteId);
      } else {
        inMemoryFavorites.add(quoteId);
      }

      persist();
      return !isFav;
    },

    /**
     * Clears all stored favorites.
     */
    clearFavorites() {
      inMemoryFavorites.clear();
      try {
        backend.removeItem(STORAGE_KEY);
      } catch {
        // Ignore removal errors
      }
    }
  };
}

