import test from "node:test";
import assert from "node:assert/strict";
import { getAllQuotes, getQuoteById, getRandomQuote } from "../../src/quotes.js";

test("getAllQuotes returns at least 8 quotes with valid schema", () => {
  const quotes = getAllQuotes();
  assert.ok(quotes.length >= 8, `Expected at least 8 quotes, found ${quotes.length}`);

  const ids = new Set();
  for (const q of quotes) {
    assert.equal(typeof q.id, "string", "id must be string");
    assert.ok(q.id.trim().length > 0, "id must not be empty or whitespace");
    assert.ok(!ids.has(q.id), `Duplicate id found: ${q.id}`);
    ids.add(q.id);

    assert.equal(typeof q.text, "string", "text must be string");
    assert.ok(q.text.trim().length > 0, "text must not be empty or whitespace");

    assert.equal(typeof q.author, "string", "author must be string");
    assert.ok(q.author.trim().length > 0, "author must not be empty or whitespace");
  }
});

test("getQuoteById retrieves matching quote or null", () => {
  const quote = getQuoteById("q1");
  assert.ok(quote !== null, "Expected quote for id 'q1'");
  assert.equal(quote.id, "q1");

  assert.equal(getQuoteById("non-existent-id"), null);
  assert.equal(getQuoteById(""), null);
  assert.equal(getQuoteById(null), null);
});

test("getRandomQuote returns a valid quote from catalog", () => {
  const quotes = getAllQuotes();
  const validIds = new Set(quotes.map(q => q.id));

  for (let i = 0; i < 20; i++) {
    const q = getRandomQuote();
    assert.ok(validIds.has(q.id), `Selected unknown quote id: ${q.id}`);
  }
});

test("getRandomQuote(excludeId) avoids returning excluded ID", () => {
  const targetId = "q1";
  for (let i = 0; i < 50; i++) {
    const q = getRandomQuote(targetId);
    assert.notEqual(q.id, targetId, "getRandomQuote returned the excluded quote ID");
  }
});

