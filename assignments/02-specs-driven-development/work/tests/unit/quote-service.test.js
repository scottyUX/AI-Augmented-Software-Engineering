import { test, describe } from "node:test";
import assert from "node:assert/strict";
import { QuoteService } from "../../src/js/services/quote-service.js";

const sampleQuotes = [
  { id: "quote-1", text: "Quote One", author: "Author One", category: "Test" },
  { id: "quote-2", text: "Quote Two", author: "Author Two", category: "Test" },
  { id: "quote-3", text: "Quote Three", author: "Author Three", category: "Test" }
];

describe("QuoteService", () => {
  test("should throw TypeError if quotes array is empty or invalid", () => {
    assert.throws(() => new QuoteService([]), /TypeError/);
    assert.throws(() => new QuoteService(null), /TypeError/);
  });

  test("should return all quotes with getAllQuotes()", () => {
    const service = new QuoteService(sampleQuotes);
    const all = service.getAllQuotes();
    assert.equal(all.length, 3);
    assert.deepEqual(all, sampleQuotes);
  });

  test("should find quote by id with getQuoteById()", () => {
    const service = new QuoteService(sampleQuotes);
    const found = service.getQuoteById("quote-2");
    assert.ok(found);
    assert.equal(found.id, "quote-2");
    assert.equal(found.text, "Quote Two");

    const notFound = service.getQuoteById("non-existent");
    assert.equal(notFound, undefined);
  });

  test("should return a random quote from the collection", () => {
    const service = new QuoteService(sampleQuotes);
    const randomQuote = service.getRandomQuote();
    assert.ok(randomQuote);
    assert.ok(["quote-1", "quote-2", "quote-3"].includes(randomQuote.id));
  });

  test("should handle single quote collection gracefully", () => {
    const singleQuote = [{ id: "single", text: "Only One", author: "Solo" }];
    const service = new QuoteService(singleQuote);

    const quote = service.getRandomQuote("single");
    assert.ok(quote);
    assert.equal(quote.id, "single");
  });

  test("should never return excludeId when collection size >= 2", () => {
    const service = new QuoteService(sampleQuotes);

    // Test multiple iterations to ensure randomness never selects excludeId
    for (let i = 0; i < 50; i++) {
      const quote = service.getRandomQuote("quote-1");
      assert.notEqual(quote.id, "quote-1", `Iteration ${i} returned excluded ID quote-1`);
      assert.ok(["quote-2", "quote-3"].includes(quote.id));
    }
  });

  // Daily Quote Tests (US1)
  test("should return the identical daily quote for the same local calendar date across different times", () => {
    const service = new QuoteService(sampleQuotes);

    // Morning, noon, night on 2026-10-17
    const morning = new Date(2026, 9, 17, 8, 30, 0);
    const noon = new Date(2026, 9, 17, 12, 0, 0);
    const night = new Date(2026, 9, 17, 23, 59, 59);

    const quoteMorning = service.getDailyQuote(morning);
    const quoteNoon = service.getDailyQuote(noon);
    const quoteNight = service.getDailyQuote(night);

    assert.ok(quoteMorning);
    assert.equal(quoteMorning.id, quoteNoon.id, "Morning and noon quotes must match");
    assert.equal(quoteNoon.id, quoteNight.id, "Noon and night quotes must match");
  });

  test("should return a valid daily quote by default when no date is passed", () => {
    const service = new QuoteService(sampleQuotes);
    const todayQuote = service.getDailyQuote();
    assert.ok(todayQuote);
    assert.ok(["quote-1", "quote-2", "quote-3"].includes(todayQuote.id));
  });

  test("should deterministically select quotes across different dates", () => {
    const service = new QuoteService(sampleQuotes);
    const date1 = new Date(2026, 9, 17);
    const date2 = new Date(2026, 9, 18);

    const quoteDay1 = service.getDailyQuote(date1);
    const quoteDay2 = service.getDailyQuote(date2);

    assert.ok(quoteDay1);
    assert.ok(quoteDay2);
    // Verifying calling date1 again yields the same quoteDay1
    assert.equal(service.getDailyQuote(date1).id, quoteDay1.id);
  });
});
