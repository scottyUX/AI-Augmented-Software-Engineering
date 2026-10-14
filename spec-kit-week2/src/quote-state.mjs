export const QUOTES = [
  {
    id: 'fault-in-ourselves',
    text: 'The fault, dear Brutus, is not in our stars, but in ourselves.',
    attribution: 'William Shakespeare, Julius Caesar',
  },
  {
    id: 'what-we-may-be',
    text: 'We know what we are, but know not what we may be.',
    attribution: 'William Shakespeare, Hamlet',
  },
  {
    id: 'soul-of-wit',
    text: 'Brevity is the soul of wit.',
    attribution: 'William Shakespeare, Hamlet',
  },
  {
    id: 'all-the-worlds-a-stage',
    text: "All the world's a stage, and all the men and women merely players.",
    attribution: 'William Shakespeare, As You Like It',
  },
  {
    id: 'nothing-comes-of-nothing',
    text: 'Nothing will come of nothing.',
    attribution: 'William Shakespeare, King Lear',
  },
  {
    id: 'discretion-and-valor',
    text: 'The better part of Valour, is Discretion.',
    attribution: 'William Shakespeare, Henry IV, Part 1',
  },
];

export const FAVORITES_KEY = 'daily-quote-favorites:v1';

export function selectQuote(quotes, currentQuoteId, random = Math.random) {
  if (!Array.isArray(quotes) || quotes.length === 0) {
    throw new Error('At least one quote is required.');
  }

  const alternatives = quotes.length > 1
    ? quotes.filter((quote) => quote.id !== currentQuoteId)
    : quotes;
  const candidates = alternatives.length > 0 ? alternatives : quotes;
  const randomIndex = Math.floor(random() * candidates.length);
  const selectedIndex = Math.max(0, Math.min(randomIndex, candidates.length - 1));

  return candidates[selectedIndex];
}

export function toggleFavorite(favoriteIds, quoteId) {
  const uniqueIds = [...new Set(favoriteIds)];

  return uniqueIds.includes(quoteId)
    ? uniqueIds.filter((id) => id !== quoteId)
    : [...uniqueIds, quoteId];
}

export function persistFavorites(storage, favoriteIds) {
  try {
    storage.setItem(FAVORITES_KEY, JSON.stringify([...new Set(favoriteIds)]));
    return true;
  } catch {
    return false;
  }
}

export function loadFavorites(storage) {
  try {
    const serializedFavorites = storage.getItem(FAVORITES_KEY);
    if (serializedFavorites === null) {
      return { favoriteIds: [], error: false };
    }

    const parsedFavorites = JSON.parse(serializedFavorites);
    if (!Array.isArray(parsedFavorites) || parsedFavorites.some((id) => typeof id !== 'string')) {
      return { favoriteIds: [], error: true };
    }

    const knownIds = new Set(QUOTES.map((quote) => quote.id));
    const favoriteIds = [...new Set(parsedFavorites.filter((id) => knownIds.has(id)))];

    return { favoriteIds, error: false };
  } catch {
    return { favoriteIds: [], error: true };
  }
}
