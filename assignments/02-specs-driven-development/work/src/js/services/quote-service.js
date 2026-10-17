/**
 * QuoteService
 *
 * Implements core domain logic for quote collection management,
 * deterministic daily quote selection, and random selection with
 * consecutive repeat prevention.
 *
 * Contract: specs/001-quote-of-the-day/contracts/quote-service.contract.md
 */

export class QuoteService {
  /**
   * @param {Array<{ id: string, text: string, author: string, category?: string }>} quotes
   */
  constructor(quotes) {
    if (!Array.isArray(quotes) || quotes.length === 0) {
      throw new TypeError("QuoteService requires a non-empty array of quotes.");
    }

    this._quotes = [...quotes];
  }

  /**
   * Deterministically returns the Quote of the Day for a given local calendar date.
   * Guarantees that calls with the same local calendar date (YYYY-MM-DD) return
   * the identical quote, regardless of time of day or page reloads.
   *
   * @param {Date} [date=new Date()] - Evaluated against user's local date
   * @returns {{ id: string, text: string, author: string, category?: string }}
   */
  getDailyQuote(date = new Date()) {
    if (this._quotes.length === 1) {
      return this._quotes[0];
    }

    // Extract user's local calendar year, month, and day
    const y = date.getFullYear();
    const m = String(date.getMonth() + 1).padStart(2, "0");
    const d = String(date.getDate()).padStart(2, "0");
    const dateKey = `${y}-${m}-${d}`;

    // 32-bit integer hash on date string
    let hash = 0;
    for (let i = 0; i < dateKey.length; i++) {
      hash = ((hash << 5) - hash) + dateKey.charCodeAt(i);
      hash |= 0;
    }

    const index = Math.abs(hash) % this._quotes.length;
    return this._quotes[index];
  }

  /**
   * Returns a random quote from the collection.
   * If excludeId is provided and collection size >= 2, guarantees the returned
   * quote does not match excludeId.
   *
   * @param {string} [excludeId]
   * @returns {{ id: string, text: string, author: string, category?: string }}
   */
  getRandomQuote(excludeId) {
    if (this._quotes.length === 1) {
      return this._quotes[0];
    }

    if (!excludeId) {
      const index = Math.floor(Math.random() * this._quotes.length);
      return this._quotes[index];
    }

    // Filter available pool excluding the current quote
    const candidates = this._quotes.filter((q) => q.id !== excludeId);
    if (candidates.length === 0) {
      return this._quotes[0];
    }

    const index = Math.floor(Math.random() * candidates.length);
    return candidates[index];
  }

  /**
   * Finds a quote by its unique ID
   * @param {string} id
   * @returns {{ id: string, text: string, author: string, category?: string } | undefined}
   */
  getQuoteById(id) {
    return this._quotes.find((q) => q.id === id);
  }

  /**
   * Returns a copy of all quotes
   * @returns {Array<{ id: string, text: string, author: string, category?: string }>}
   */
  getAllQuotes() {
    return [...this._quotes];
  }
}
