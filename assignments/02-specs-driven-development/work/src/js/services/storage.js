/**
 * StorageService
 *
 * Implements persistent storage for favorites using localStorage with
 * automatic detection and in-memory fallback for restricted environments.
 *
 * Contract: specs/001-quote-of-the-day/contracts/storage.contract.md
 */

const STORAGE_KEY = "qod_favorites_v1";

export class StorageService {
  /**
   * @param {Storage} [storageBackend] - Underlying storage engine (defaults to window.localStorage if available)
   */
  constructor(storageBackend) {
    this._memoryFallback = new Map();
    this._isPersistentBackend = false;

    // Resolve backend safely
    let backend = storageBackend;
    if (!backend && typeof window !== "undefined" && window.localStorage) {
      backend = window.localStorage;
    }

    // Probe backend for write/read accessibility
    if (backend) {
      try {
        const testKey = "__qod_probe__";
        backend.setItem(testKey, "1");
        backend.getItem(testKey);
        backend.removeItem(testKey);
        this._backend = backend;
        this._isPersistentBackend = true;
      } catch {
        this._backend = null;
        this._isPersistentBackend = false;
      }
    } else {
      this._backend = null;
      this._isPersistentBackend = false;
    }
  }

  /**
   * Indicates whether storage is backed by durable persistent storage
   * @returns {boolean}
   */
  isPersistent() {
    return this._isPersistentBackend;
  }

  /**
   * Retrieves all saved favorite records
   * @returns {Array<{ quoteId: string, favoritedAt: string }>}
   */
  getFavorites() {
    if (this._isPersistentBackend && this._backend) {
      try {
        const raw = this._backend.getItem(STORAGE_KEY);
        if (!raw) return [];
        const parsed = JSON.parse(raw);
        if (Array.isArray(parsed)) {
          return parsed;
        }
        // If not array, reset corrupted entry
        this._backend.removeItem(STORAGE_KEY);
        return [];
      } catch {
        try {
          this._backend.removeItem(STORAGE_KEY);
        } catch {
          // ignore error removing
        }
        return [];
      }
    }

    // In-memory fallback
    const memData = this._memoryFallback.get(STORAGE_KEY);
    return memData ? [...memData] : [];
  }

  /**
   * Checks if a quote ID is favorited
   * @param {string} quoteId
   * @returns {boolean}
   */
  isFavorite(quoteId) {
    const favorites = this.getFavorites();
    return favorites.some((f) => f.quoteId === quoteId);
  }

  /**
   * Adds a quote ID to favorites
   * @param {string} quoteId
   * @returns {boolean}
   */
  addFavorite(quoteId) {
    if (!quoteId) return false;
    const favorites = this.getFavorites();
    if (favorites.some((f) => f.quoteId === quoteId)) {
      return true; // Already favorite
    }

    const newRecord = {
      quoteId,
      favoritedAt: new Date().toISOString()
    };
    favorites.push(newRecord);

    return this._saveFavorites(favorites);
  }

  /**
   * Removes a quote ID from favorites
   * @param {string} quoteId
   * @returns {boolean}
   */
  removeFavorite(quoteId) {
    if (!quoteId) return false;
    const favorites = this.getFavorites();
    const updated = favorites.filter((f) => f.quoteId !== quoteId);
    return this._saveFavorites(updated);
  }

  /**
   * Persists the favorites array to backend or memory
   * @private
   * @param {Array<{ quoteId: string, favoritedAt: string }>} list
   * @returns {boolean}
   */
  _saveFavorites(list) {
    if (this._isPersistentBackend && this._backend) {
      try {
        this._backend.setItem(STORAGE_KEY, JSON.stringify(list));
        return true;
      } catch {
        // Fall back to memory on write failure
        this._memoryFallback.set(STORAGE_KEY, list);
        return false;
      }
    }

    this._memoryFallback.set(STORAGE_KEY, list);
    return true;
  }
}
