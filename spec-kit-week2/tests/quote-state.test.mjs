import assert from 'node:assert/strict';
import test from 'node:test';

import {
  FAVORITES_KEY,
  QUOTES,
  loadFavorites,
  persistFavorites,
  selectQuote,
  toggleFavorite,
} from '../src/quote-state.mjs';

test('built-in quotes have unique IDs and non-empty text', () => {
  const ids = QUOTES.map((quote) => quote.id);

  assert.ok(ids.length >= 2);
  assert.equal(new Set(ids).size, ids.length);
  assert.ok(QUOTES.every((quote) => quote.text.trim().length > 0));
});

test('selects a quote from the supplied collection', () => {
  const selected = selectQuote(QUOTES, null, () => 0);

  assert.ok(QUOTES.some((quote) => quote.id === selected.id));
});

test('does not immediately repeat the current quote when alternatives exist', () => {
  const currentQuote = QUOTES[0];
  const selected = selectQuote(QUOTES, currentQuote.id, () => 0);

  assert.notEqual(selected.id, currentQuote.id);
});

test('keeps the only quote selected when no alternative exists', () => {
  const onlyQuote = { id: 'only', text: 'One is enough.' };

  assert.equal(selectQuote([onlyQuote], onlyQuote.id, () => 0), onlyQuote);
});

test('adds and removes a favorite without duplicates', () => {
  assert.deepEqual(toggleFavorite([], 'fault-in-ourselves'), ['fault-in-ourselves']);
  assert.deepEqual(
    toggleFavorite(['fault-in-ourselves', 'fault-in-ourselves'], 'fault-in-ourselves'),
    [],
  );
});

test('persists unique favorite IDs using the versioned storage key', () => {
  const stored = new Map();
  const storage = {
    setItem(key, value) {
      stored.set(key, value);
    },
  };

  assert.equal(persistFavorites(storage, ['fault-in-ourselves', 'fault-in-ourselves']), true);
  assert.equal(FAVORITES_KEY, 'daily-quote-favorites:v1');
  assert.equal(stored.get(FAVORITES_KEY), '["fault-in-ourselves"]');
});

test('reports favorite persistence failure without throwing', () => {
  const storage = {
    setItem() {
      throw new Error('Storage is unavailable.');
    },
  };

  assert.equal(persistFavorites(storage, ['fault-in-ourselves']), false);
});

test('restores only known unique favorite IDs', () => {
  const storage = {
    getItem(key) {
      assert.equal(key, FAVORITES_KEY);
      return JSON.stringify([
        'fault-in-ourselves',
        'fault-in-ourselves',
        'unknown-quote',
      ]);
    },
  };

  assert.deepEqual(loadFavorites(storage), {
    favoriteIds: ['fault-in-ourselves'],
    error: false,
  });
});

test('treats missing favorite data as an empty collection without an error', () => {
  assert.deepEqual(loadFavorites({ getItem: () => null }), {
    favoriteIds: [],
    error: false,
  });
});

test('reports malformed favorite data without throwing', () => {
  assert.deepEqual(loadFavorites({ getItem: () => '{invalid json' }), {
    favoriteIds: [],
    error: true,
  });
  assert.deepEqual(loadFavorites({ getItem: () => JSON.stringify({ favorite: 'quote' }) }), {
    favoriteIds: [],
    error: true,
  });
});

test('reports favorite storage read failure without throwing', () => {
  const storage = {
    getItem() {
      throw new Error('Storage is unavailable.');
    },
  };

  assert.deepEqual(loadFavorites(storage), {
    favoriteIds: [],
    error: true,
  });
});
