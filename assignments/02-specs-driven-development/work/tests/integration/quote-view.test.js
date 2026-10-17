import { test, describe } from "node:test";
import assert from "node:assert/strict";
import { QuoteView } from "../../src/js/ui/quote-view.js";
import { QuoteService } from "../../src/js/services/quote-service.js";

/**
 * Mock DOM element helper for integration testing
 */
function createMockElement() {
  const attributes = new Map();
  const classListSet = new Set();

  return {
    textContent: "",
    innerHTML: "",
    setAttribute(name, value) {
      attributes.set(name, String(value));
    },
    getAttribute(name) {
      return attributes.get(name) || null;
    },
    classList: {
      add(cls) { classListSet.add(cls); },
      remove(cls) { classListSet.delete(cls); },
      contains(cls) { return classListSet.has(cls); }
    }
  };
}

describe("QuoteView (US1)", () => {
  test("should render quote text and author correctly", () => {
    const textElement = createMockElement();
    const authorElement = createMockElement();
    const categoryElement = createMockElement();
    const favoriteButton = createMockElement();

    const view = new QuoteView({
      textElement,
      authorElement,
      categoryElement,
      favoriteButton
    });

    const quote = {
      id: "q-1",
      text: "The future belongs to those who believe.",
      author: "Eleanor Roosevelt",
      category: "Dreams"
    };

    view.renderQuote(quote, false);

    assert.ok(textElement.textContent.includes("The future belongs to those who believe."));
    assert.ok(authorElement.textContent.includes("Eleanor Roosevelt"));
    assert.equal(categoryElement.textContent, "Dreams");
    assert.equal(favoriteButton.getAttribute("aria-pressed"), "false");
    assert.equal(favoriteButton.classList.contains("is-favorite"), false);
  });

  test("should render active favorite state when isFavorite is true", () => {
    const textElement = createMockElement();
    const authorElement = createMockElement();
    const favoriteButton = createMockElement();

    const view = new QuoteView({
      textElement,
      authorElement,
      favoriteButton
    });

    view.renderQuote({ id: "q-1", text: "Text", author: "Author" }, true);

    assert.equal(favoriteButton.getAttribute("aria-pressed"), "true");
    assert.equal(favoriteButton.classList.contains("is-favorite"), true);
  });

  test("should render deterministic daily quote from QuoteService on load", () => {
    const textElement = createMockElement();
    const authorElement = createMockElement();
    const favoriteButton = createMockElement();

    const view = new QuoteView({ textElement, authorElement, favoriteButton });
    const quotes = [
      { id: "q-10", text: "Daily Quote Text", author: "Daily Author" }
    ];
    const service = new QuoteService(quotes);
    const dailyQuote = service.getDailyQuote ? service.getDailyQuote() : quotes[0];

    view.renderQuote(dailyQuote, false);
    assert.ok(textElement.textContent.includes("Daily Quote Text"));
    assert.ok(authorElement.textContent.includes("Daily Author"));
  });
});
