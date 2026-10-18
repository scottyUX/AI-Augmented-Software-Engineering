import test from "node:test";
import assert from "node:assert/strict";
import { createStorageAdapter, STORAGE_KEY } from "../../src/storage.js";

/**
 * Creates a mock Web Storage object for testing.
 * @param {Record<string, string>} [initialData={}]
 * @param {Object} [options={}]
 * @param {boolean} [options.throwOnGet=false]
 * @param {boolean} [options.throwOnSet=false]
 */
function createMockStorage(initialData = {}, options = {}) {
  const store = { ...initialData };
  return {
    getItem(key) {
      if (options.throwOnGet) {
        const err = new Error("Access denied");
        err.name = "SecurityError";
        throw err;
      }
      return Object.prototype.hasOwnProperty.call(store, key) ? store[key] : null;
    },
    setItem(key, value) {
      if (options.throwOnSet) {
        const err = new Error("Storage quota exceeded");
        err.name = "QuotaExceededError";
        throw err;
      }
      store[key] = String(value);
    },
    removeItem(key) {
      delete store[key];
    },
    clear() {
      for (const k of Object.keys(store)) {
        delete store[k];
      }
    },
    _getRawStore() {
      return store;
    }
  };
}

test("StorageAdapter initializes with empty favorites when storage is empty", () => {
  const mock = createMockStorage();
  const adapter = createStorageAdapter(mock);

  assert.deepEqual(adapter.getFavorites(), []);
  assert.equal(adapter.isFavorite("q1"), false);
});

test("StorageAdapter toggles favorite state and persists to storage", () => {
  const mock = createMockStorage();
  const adapter = createStorageAdapter(mock);

  // Toggle on
  const res1 = adapter.toggleFavorite("q1");
  assert.equal(res1, true);
  assert.equal(adapter.isFavorite("q1"), true);
  assert.deepEqual(adapter.getFavorites(), ["q1"]);
  assert.equal(mock._getRawStore()[STORAGE_KEY], JSON.stringify(["q1"]));

  // Toggle second quote
  const res2 = adapter.toggleFavorite("q2");
  assert.equal(res2, true);
  assert.equal(adapter.isFavorite("q2"), true);
  assert.deepEqual(adapter.getFavorites(), ["q1", "q2"]);

  // Toggle off q1
  const res3 = adapter.toggleFavorite("q1");
  assert.equal(res3, false);
  assert.equal(adapter.isFavorite("q1"), false);
  assert.deepEqual(adapter.getFavorites(), ["q2"]);
  assert.equal(mock._getRawStore()[STORAGE_KEY], JSON.stringify(["q2"]));
});

test("StorageAdapter clears all favorites", () => {
  const mock = createMockStorage();
  const adapter = createStorageAdapter(mock);

  adapter.toggleFavorite("q1");
  adapter.toggleFavorite("q2");
  assert.equal(adapter.getFavorites().length, 2);

  adapter.clearFavorites();
  assert.deepEqual(adapter.getFavorites(), []);
  assert.equal(adapter.isFavorite("q1"), false);
  assert.equal(adapter.isFavorite("q2"), false);
});

test("StorageAdapter loads existing valid favorites from storage", () => {
  const mock = createMockStorage({
    [STORAGE_KEY]: JSON.stringify(["q3", "q5"])
  });
  const adapter = createStorageAdapter(mock);

  assert.equal(adapter.isFavorite("q3"), true);
  assert.equal(adapter.isFavorite("q5"), true);
  assert.equal(adapter.isFavorite("q1"), false);
  assert.deepEqual(adapter.getFavorites(), ["q3", "q5"]);
});

test("StorageAdapter recovers gracefully from malformed JSON", () => {
  const mock = createMockStorage({
    [STORAGE_KEY]: "{not valid json"
  });
  const adapter = createStorageAdapter(mock);

  assert.deepEqual(adapter.getFavorites(), []);
  assert.equal(adapter.isFavorite("q1"), false);

  // Still allows toggling
  const res = adapter.toggleFavorite("q1");
  assert.equal(res, true);
  assert.equal(adapter.isFavorite("q1"), true);
});

test("StorageAdapter sanitizes non-string elements from stored array", () => {
  const mock = createMockStorage({
    [STORAGE_KEY]: JSON.stringify([123, null, "q2", "", {}, "q7"])
  });
  const adapter = createStorageAdapter(mock);

  assert.deepEqual(adapter.getFavorites(), ["q2", "q7"]);
  assert.equal(adapter.isFavorite("q2"), true);
  assert.equal(adapter.isFavorite("q7"), true);
});

test("StorageAdapter falls back to in-memory store when storage throws SecurityError", () => {
  const mock = createMockStorage({}, { throwOnGet: true, throwOnSet: true });
  const adapter = createStorageAdapter(mock);

  assert.deepEqual(adapter.getFavorites(), []);
  // Should not throw
  const res = adapter.toggleFavorite("q1");
  assert.equal(res, true);
  assert.equal(adapter.isFavorite("q1"), true);
});

test("StorageAdapter handles QuotaExceededError without throwing", () => {
  const mock = createMockStorage({}, { throwOnSet: true });
  const adapter = createStorageAdapter(mock);

  assert.doesNotThrow(() => {
    const res = adapter.toggleFavorite("q1");
    assert.equal(res, true);
    assert.equal(adapter.isFavorite("q1"), true);
  });
});

