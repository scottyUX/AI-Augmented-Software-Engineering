import { test, describe } from "node:test";
import assert from "node:assert/strict";
import { QuoteService } from "../../src/js/services/quote-service.js";
import { StorageService } from "../../src/js/services/storage.js";
import { quotes } from "../../src/js/data/quotes.js";

class MockStorage {
  constructor() { this.store = new Map(); }
  getItem(key) { return this.store.get(key) || null; }
  setItem(key, value) { this.store.set(key, String(value)); }
  removeItem(key) { this.store.delete(key); }
  clear() { this.store.clear(); }
}

describe("End-to-End Workflow Verification (Quickstart Scenarios)", () => {
  test("Scenario 1: Daily Quote on Page Load stays identical for whole calendar day", () => {
    const quoteService = new QuoteService(quotes);

    // Simulate same calendar day at different times
    const morning = new Date(2026, 9, 17, 9, 0, 0);
    const evening = new Date(2026, 9, 17, 21, 30, 0);

    const morningQuote = quoteService.getDailyQuote(morning);
    const eveningQuote = quoteService.getDailyQuote(evening);

    assert.ok(morningQuote.id);
    assert.ok(morningQuote.text.length > 0);
    assert.ok(morningQuote.author.length > 0);
    assert.equal(morningQuote.id, eveningQuote.id, "Quote on same calendar day must be identical");
  });

  test("Scenario 2: New Quote Button cycles to random quote and never repeats currently displayed quote", () => {
    const quoteService = new QuoteService(quotes);
    const currentQuote = quoteService.getDailyQuote();

    // Cycling 30 times: each time nextQuote must differ from active quote
    let active = currentQuote;
    for (let i = 0; i < 30; i++) {
      const nextQuote = quoteService.getRandomQuote(active.id);
      assert.notEqual(nextQuote.id, active.id, `Iteration ${i}: next quote must not equal active quote`);
      active = nextQuote;
    }
  });

  test("Scenario 3 & 4: Favoriting, Persistence across reload, and Drawer Removal", () => {
    const mockStorageBackend = new MockStorage();
    let storageService = new StorageService(mockStorageBackend);
    const quoteService = new QuoteService(quotes);

    // Step 1: User favorites quote 1
    const targetQuote = quotes[0];
    storageService.addFavorite(targetQuote.id);
    assert.equal(storageService.isFavorite(targetQuote.id), true);

    // Step 2: Simulate browser page reload by creating a new StorageService instance with same backend
    const reloadedStorage = new StorageService(mockStorageBackend);
    assert.equal(reloadedStorage.isFavorite(targetQuote.id), true, "Favorite must persist across reload");

    // Step 3: View favorites list
    const favRecords = reloadedStorage.getFavorites();
    assert.equal(favRecords.length, 1);
    assert.equal(favRecords[0].quoteId, targetQuote.id);

    // Step 4: Remove favorite
    reloadedStorage.removeFavorite(targetQuote.id);
    assert.equal(reloadedStorage.isFavorite(targetQuote.id), false, "Favorite removed");
    assert.equal(reloadedStorage.getFavorites().length, 0);
  });
});
