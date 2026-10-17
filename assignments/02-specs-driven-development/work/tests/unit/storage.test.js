import { test, describe, beforeEach } from "node:test";
import assert from "node:assert/strict";
import { StorageService } from "../../src/js/services/storage.js";

/**
 * Mock localStorage implementation for Node test environment
 */
class MockLocalStorage {
  constructor() {
    this.store = new Map();
    this.failOnSet = false;
    this.failOnGet = false;
  }

  getItem(key) {
    if (this.failOnGet) {
      throw new Error("SecurityError: localStorage is disabled");
    }
    return this.store.get(key) || null;
  }

  setItem(key, value) {
    if (this.failOnSet) {
      throw new Error("QuotaExceededError: storage full");
    }
    this.store.set(key, String(value));
  }

  removeItem(key) {
    this.store.delete(key);
  }

  clear() {
    this.store.clear();
  }
}

describe("StorageService", () => {
  let mockStorage;
  let storageService;

  beforeEach(() => {
    mockStorage = new MockLocalStorage();
    storageService = new StorageService(mockStorage);
  });

  test("should report isPersistent as true when mockStorage is working", () => {
    assert.equal(storageService.isPersistent(), true);
  });

  test("should return empty array when no favorites are saved", () => {
    assert.deepEqual(storageService.getFavorites(), []);
  });

  test("should add a favorite and persist it", () => {
    const success = storageService.addFavorite("quote-001");
    assert.equal(success, true);
    assert.equal(storageService.isFavorite("quote-001"), true);
    assert.equal(storageService.isFavorite("quote-002"), false);

    const favorites = storageService.getFavorites();
    assert.equal(favorites.length, 1);
    assert.equal(favorites[0].quoteId, "quote-001");
    assert.ok(favorites[0].favoritedAt);
  });

  test("should not add duplicate favorites", () => {
    storageService.addFavorite("quote-001");
    storageService.addFavorite("quote-001");

    const favorites = storageService.getFavorites();
    assert.equal(favorites.length, 1);
  });

  test("should remove a favorite", () => {
    storageService.addFavorite("quote-001");
    storageService.addFavorite("quote-002");

    assert.equal(storageService.isFavorite("quote-001"), true);
    const removed = storageService.removeFavorite("quote-001");
    assert.equal(removed, true);
    assert.equal(storageService.isFavorite("quote-001"), false);
    assert.equal(storageService.isFavorite("quote-002"), true);

    const favorites = storageService.getFavorites();
    assert.equal(favorites.length, 1);
    assert.equal(favorites[0].quoteId, "quote-002");
  });

  test("should handle corrupted JSON gracefully and return empty array", () => {
    mockStorage.setItem("qod_favorites_v1", "{ malformed_json :::");

    const favorites = storageService.getFavorites();
    assert.deepEqual(favorites, []);
    assert.equal(storageService.isFavorite("quote-001"), false);
  });

  test("should fall back to in-memory store if localStorage throws SecurityError", () => {
    const failingStorage = {
      getItem() { throw new Error("SecurityError: blocked"); },
      setItem() { throw new Error("SecurityError: blocked"); },
      removeItem() { throw new Error("SecurityError: blocked"); }
    };

    const fallbackService = new StorageService(failingStorage);
    assert.equal(fallbackService.isPersistent(), false);

    // Can still add and read in-memory
    const added = fallbackService.addFavorite("quote-005");
    assert.equal(added, true);
    assert.equal(fallbackService.isFavorite("quote-005"), true);
    assert.equal(fallbackService.getFavorites().length, 1);
  });
});
