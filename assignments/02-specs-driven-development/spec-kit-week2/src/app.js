/**
 * Main application coordinator for Quote of the Day.
 */

import { getRandomQuote } from "./quotes.js";
import { createStorageAdapter } from "./storage.js";

/**
 * Initializes and binds the Quote of the Day application.
 */
export function initApp() {
  const quoteTextEl = document.getElementById("quote-text");
  const quoteAuthorEl = document.getElementById("quote-author");
  const btnNewQuote = document.getElementById("btn-new-quote");
  const btnFavorite = document.getElementById("btn-favorite");
  const favoriteLabel = document.getElementById("favorite-label");

  if (!quoteTextEl || !quoteAuthorEl || !btnNewQuote || !btnFavorite) {
    console.error("Required DOM elements missing for Quote of the Day");
    return;
  }

  // Initialize storage adapter with browser localStorage
  const storage = createStorageAdapter();

  /** @type {import('./quotes.js').Quote | null} */
  let currentQuote = null;

  /**
   * Updates the visual and accessibility state of the favorite button.
   * @param {boolean} isFav
   */
  function updateFavoriteState(isFav) {
    btnFavorite.setAttribute("aria-pressed", isFav ? "true" : "false");
    if (isFav) {
      btnFavorite.classList.add("is-favorite");
      if (favoriteLabel) {
        favoriteLabel.textContent = "Favorited";
      }
    } else {
      btnFavorite.classList.remove("is-favorite");
      if (favoriteLabel) {
        favoriteLabel.textContent = "Favorite";
      }
    }
  }

  /**
   * Renders a given quote into the DOM and synchronizes favorite state.
   * @param {import('./quotes.js').Quote} quote
   */
  function renderQuote(quote) {
    currentQuote = quote;
    quoteTextEl.textContent = quote.text;
    quoteAuthorEl.textContent = quote.author;

    const isFav = storage.isFavorite(quote.id);
    updateFavoriteState(isFav);
  }

  /**
   * Selects and displays a new quote.
   */
  function handleNewQuote() {
    try {
      const nextQuote = getRandomQuote(currentQuote ? currentQuote.id : null);
      renderQuote(nextQuote);
    } catch (err) {
      console.error("Failed to load new quote:", err);
    }
  }

  /**
   * Toggles the favorite status for the current quote.
   */
  function handleToggleFavorite() {
    if (!currentQuote) {
      return;
    }
    const newStatus = storage.toggleFavorite(currentQuote.id);
    updateFavoriteState(newStatus);
  }

  // Attach event listeners
  btnNewQuote.addEventListener("click", handleNewQuote);
  btnFavorite.addEventListener("click", handleToggleFavorite);

  // Initial render
  handleNewQuote();
}

// Auto-initialize when loaded in browser
if (typeof document !== "undefined") {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initApp);
  } else {
    initApp();
  }
}

