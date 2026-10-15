/**
 * Quotes catalog and domain logic for Quote of the Day.
 */

/**
 * @typedef {Object} Quote
 * @property {string} id - Unique identifier
 * @property {string} text - Quote text content
 * @property {string} author - Author attribution
 */

/**
 * Built-in curated catalog of quotes.
 * Constraints:
 * - id: must be unique non-empty string
 * - text: must not be empty or whitespace-only
 * - author: must not be empty or whitespace-only
 * @type {ReadonlyArray<Quote>}
 */
export const QUOTES = Object.freeze([
  {
    id: "q1",
    text: "Simplicity is prerequisite for reliability.",
    author: "Edsger W. Dijkstra"
  },
  {
    id: "q2",
    text: "Make it work, make it right, make it fast.",
    author: "Kent Beck"
  },
  {
    id: "q3",
    text: "Premature optimization is the root of all evil.",
    author: "Donald Knuth"
  },
  {
    id: "q4",
    text: "The only way to go fast, is to go well.",
    author: "Robert C. Martin"
  },
  {
    id: "q5",
    text: "Any fool can write code that a computer can understand. Good programmers write code that humans can understand.",
    author: "Martin Fowler"
  },
  {
    id: "q6",
    text: "Programs must be written for people to read, and only incidentally for machines to execute.",
    author: "Harold Abelson"
  },
  {
    id: "q7",
    text: "Truth can only be found in one place: the code.",
    author: "Robert C. Martin"
  },
  {
    id: "q8",
    text: "First, solve the problem. Then, write the code.",
    author: "John Johnson"
  },
  {
    id: "q9",
    text: "Code is like humor. When you have to explain it, it’s bad.",
    author: "Cory House"
  },
  {
    id: "q10",
    text: "Experience is the name everyone gives to their mistakes.",
    author: "Oscar Wilde"
  }
]);

/**
 * Returns a list of all quotes in the catalog.
 * @returns {Quote[]}
 */
export function getAllQuotes() {
  return [...QUOTES];
}

/**
 * Retrieves a quote by its unique identifier.
 * @param {string} id
 * @returns {Quote | null}
 */
export function getQuoteById(id) {
  if (!id || typeof id !== "string") {
    return null;
  }
  return QUOTES.find(q => q.id === id) || null;
}

/**
 * Selects a random quote from the catalog, avoiding excludeId if multiple quotes exist.
 * @param {string | null} [excludeId=null]
 * @returns {Quote}
 */
export function getRandomQuote(excludeId = null) {
  if (QUOTES.length === 0) {
    throw new Error("Quote catalog cannot be empty");
  }
  if (QUOTES.length === 1) {
    return QUOTES[0];
  }

  const pool = excludeId
    ? QUOTES.filter(q => q.id !== excludeId)
    : QUOTES;

  const candidates = pool.length > 0 ? pool : QUOTES;
  const randomIndex = Math.floor(Math.random() * candidates.length);
  return candidates[randomIndex];
}

