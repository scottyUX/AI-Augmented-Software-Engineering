import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { getAllQuotes, getRandomQuote } from "../../src/quotes.js";
import { createStorageAdapter, STORAGE_KEY } from "../../src/storage.js";

const __dirname = dirname(fileURLToPath(import.meta.url));

test("index.html contains all required semantic contract elements", () => {
  const htmlPath = resolve(__dirname, "../../index.html");
  const html = readFileSync(htmlPath, "utf-8");

  assert.ok(html.includes('id="quote-card"'), "Missing #quote-card");
  assert.ok(html.includes('id="quote-text"'), "Missing #quote-text");
  assert.ok(html.includes('id="quote-author"'), "Missing #quote-author");
  assert.ok(html.includes('id="btn-new-quote"'), "Missing #btn-new-quote");
  assert.ok(html.includes('id="btn-favorite"'), "Missing #btn-favorite");
  assert.ok(html.includes('aria-live="polite"'), "Missing aria-live on quote container");
  assert.ok(html.includes('aria-pressed="false"'), "Missing initial aria-pressed attribute");
  assert.ok(html.includes('src="src/app.js"'), "Missing app.js module link");
  assert.ok(html.includes('href="style.css"'), "Missing style.css link");
});

test("End-to-End Simulation: Quote rotation, favoriting, and reload persistence", () => {
  // Simulate browser storage
  const mockStorageStore = {};
  const mockStorage = {
    getItem(k) { return mockStorageStore[k] || null; },
    setItem(k, v) { mockStorageStore[k] = String(v); },
    removeItem(k) { delete mockStorageStore[k]; }
  };

  // Session 1: User visits page
  const storage1 = createStorageAdapter(mockStorage);
  const q1 = getRandomQuote();
  assert.ok(q1 && q1.id && q1.text && q1.author);
  assert.equal(storage1.isFavorite(q1.id), false, "Initial quote should not be favorited");

  // User favorites current quote
  const favState = storage1.toggleFavorite(q1.id);
  assert.equal(favState, true);
  assert.equal(storage1.isFavorite(q1.id), true);

  // User clicks "New quote"
  const q2 = getRandomQuote(q1.id);
  assert.notEqual(q2.id, q1.id, "Quote rotation must not immediately repeat same quote");

  // Session 2: User reloads page
  const storage2 = createStorageAdapter(mockStorage);
  assert.equal(storage2.isFavorite(q1.id), true, "Favorited quote must persist across reloads");
  assert.deepEqual(storage2.getFavorites(), [q1.id]);
});

