import { test, describe, beforeEach } from "node:test";
import assert from "node:assert/strict";
import { StorageService } from "../../src/js/services/storage.js";
import { QuoteService } from "../../src/js/services/quote-service.js";
import { QuoteView } from "../../src/js/ui/quote-view.js";

class MockStorage {
  constructor() {
    this.store = new Map();
  }
  getItem(key) { return this.store.get(key) || null; }
  setItem(key, value) { this.store.set(key, String(value)); }
  removeItem(key) { this.store.delete(key); }
  clear() { this.store.clear(); }
}

function createMockElement() {
  const attributes = new Map();
  const classListSet = new Set();
  return {
    textContent: "",
    setAttribute(name, value) { attributes.set(name, String(value)); },
    getAttribute(name) { return attributes.get(name) || null; },
    classList: {
      add(cls) { classListSet.add(cls); },
      remove(cls) { classListSet.delete(cls); },
      contains(cls) { return classListSet.has(cls); }
    }
  };
}

describe("Favorite Toggle & Persistence Integration (US3)", () => {
  let storage;
  let quoteService;
  let quoteView;
  let favoriteButton;

  const quotes = [
    { id: "q1", text: "Quote One", author: "Author One" },
    { id: "q2", text: "Quote Two", author: "Author Two" }
  ];

  beforeEach(() => {
    storage = new StorageService(new MockStorage());
    quoteService = new QuoteService(quotes);
    favoriteButton = createMockElement();
    quoteView = new QuoteView({
      textElement: createMockElement(),
      authorElement: createMockElement(),
      favoriteButton
    });
  });

  test("toggle favorite from inactive to active and persist in storage", () => {
    const q1 = quoteService.getQuoteById("q1");
    quoteView.renderQuote(q1, storage.isFavorite(q1.id));

    assert.equal(storage.isFavorite("q1"), false);
    assert.equal(favoriteButton.getAttribute("aria-pressed"), "false");

    // Simulate toggle action
    storage.addFavorite(q1.id);
    quoteView.setFavoriteState(storage.isFavorite(q1.id));

    assert.equal(storage.isFavorite("q1"), true);
    assert.equal(favoriteButton.getAttribute("aria-pressed"), "true");
    assert.equal(favoriteButton.classList.contains("is-favorite"), true);
  });

  test("toggle favorite from active to inactive and remove from storage", () => {
    const q1 = quoteService.getQuoteById("q1");
    storage.addFavorite(q1.id);
    quoteView.renderQuote(q1, storage.isFavorite(q1.id));

    assert.equal(storage.isFavorite("q1"), true);
    assert.equal(favoriteButton.getAttribute("aria-pressed"), "true");

    // Untoggle
    storage.removeFavorite(q1.id);
    quoteView.setFavoriteState(storage.isFavorite(q1.id));

    assert.equal(storage.isFavorite("q1"), false);
    assert.equal(favoriteButton.getAttribute("aria-pressed"), "false");
    assert.equal(favoriteButton.classList.contains("is-favorite"), false);
  });

  test("changing quote reflects that quote's favorite state accurately", () => {
    storage.addFavorite("q2"); // q2 is favorited, q1 is not

    const q1 = quoteService.getQuoteById("q1");
    quoteView.renderQuote(q1, storage.isFavorite(q1.id));
    assert.equal(favoriteButton.getAttribute("aria-pressed"), "false");

    const q2 = quoteService.getQuoteById("q2");
    quoteView.renderQuote(q2, storage.isFavorite(q2.id));
    assert.equal(favoriteButton.getAttribute("aria-pressed"), "true");
  });
});
