/**
 * Application Bootstrap & Event Coordinator
 *
 * Coordinates QuoteService, StorageService, QuoteView, and FavoritesView.
 */

import { quotes } from "./data/quotes.js";
import { QuoteService } from "./services/quote-service.js";
import { StorageService } from "./services/storage.js";
import { QuoteView } from "./ui/quote-view.js";
import { FavoritesView } from "./ui/favorites-view.js";

// Initialize Core Services
export const quoteService = new QuoteService(quotes);
export const storageService = new StorageService();

/**
 * Initializes the application
 */
export function initApp() {
  // DOM Elements
  const container = document.getElementById("quote-container");
  const textElement = document.getElementById("quote-text");
  const authorElement = document.getElementById("quote-author");
  const categoryElement = document.getElementById("quote-category");
  const favoriteButton = document.getElementById("favorite-toggle-btn");
  const storageWarning = document.getElementById("storage-warning");

  const drawerElement = document.getElementById("favorites-drawer");
  const backdropElement = document.getElementById("drawer-backdrop");
  const listElement = document.getElementById("favorites-list");
  const emptyElement = document.getElementById("favorites-empty");
  const countBadgeElement = document.getElementById("favorites-count-badge");
  const toggleFavoritesBtn = document.getElementById("toggle-favorites-btn");
  const closeDrawerBtn = document.getElementById("close-drawer-btn");
  const newQuoteBtn = document.getElementById("new-quote-btn");

  // Show storage warning if operating in in-memory fallback mode
  if (storageWarning && !storageService.isPersistent()) {
    storageWarning.classList.add("is-visible");
  }

  // Initialize Quote View
  const quoteView = new QuoteView({
    container,
    textElement,
    authorElement,
    categoryElement,
    favoriteButton
  });

  // Helper to fetch full quote objects for all stored favorites
  const getResolvedFavorites = () => {
    const records = storageService.getFavorites();
    return records
      .map((rec) => quoteService.getQuoteById(rec.quoteId))
      .filter(Boolean);
  };

  // Initialize Favorites View (User Story 4)
  const favoritesView = new FavoritesView({
    drawerElement,
    backdropElement,
    listElement,
    emptyElement,
    countBadgeElement,
    onRemoveFavorite: (quoteId) => {
      storageService.removeFavorite(quoteId);
      favoritesView.renderFavorites(getResolvedFavorites());

      // If the removed quote is currently on screen, sync its toggle button
      const activeQuote = quoteView.getCurrentQuote();
      if (activeQuote && activeQuote.id === quoteId) {
        quoteView.setFavoriteState(false);
      }
    }
  });

  // Initial favorites render (to populate badge and drawer)
  favoritesView.renderFavorites(getResolvedFavorites());

  // Display initial deterministic Quote of the Day for today (User Story 1)
  const initialQuote = quoteService.getDailyQuote();
  const isFav = storageService.isFavorite(initialQuote.id);
  quoteView.renderQuote(initialQuote, isFav);

  // New quote button handler (User Story 2)
  if (newQuoteBtn) {
    newQuoteBtn.addEventListener("click", () => {
      const currentQuote = quoteView.getCurrentQuote();
      const currentId = currentQuote ? currentQuote.id : undefined;
      const nextQuote = quoteService.getRandomQuote(currentId);
      const isNextFav = storageService.isFavorite(nextQuote.id);
      quoteView.renderQuote(nextQuote, isNextFav);
    });
  }

  // Favorite toggle button handler (User Story 3)
  if (favoriteButton) {
    favoriteButton.addEventListener("click", () => {
      const currentQuote = quoteView.getCurrentQuote();
      if (!currentQuote) return;

      const currentlyFav = storageService.isFavorite(currentQuote.id);
      if (currentlyFav) {
        storageService.removeFavorite(currentQuote.id);
      } else {
        storageService.addFavorite(currentQuote.id);
      }

      const nextFavState = !currentlyFav;
      quoteView.setFavoriteState(nextFavState);
      favoritesView.renderFavorites(getResolvedFavorites());
    });
  }

  // Drawer open / close handlers (User Story 4)
  if (toggleFavoritesBtn) {
    toggleFavoritesBtn.addEventListener("click", () => {
      favoritesView.renderFavorites(getResolvedFavorites());
      favoritesView.open();
      if (toggleFavoritesBtn) toggleFavoritesBtn.setAttribute("aria-expanded", "true");
    });
  }

  const closeDrawer = () => {
    favoritesView.close();
    if (toggleFavoritesBtn) toggleFavoritesBtn.setAttribute("aria-expanded", "false");
  };

  if (closeDrawerBtn) {
    closeDrawerBtn.addEventListener("click", closeDrawer);
  }

  if (backdropElement) {
    backdropElement.addEventListener("click", closeDrawer);
  }

  // Close drawer on Escape key
  if (typeof document !== "undefined") {
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && favoritesView.isOpen()) {
        closeDrawer();
      }
    });
  }

  return { quoteView, favoritesView, quoteService, storageService };
}

// Auto-bootstrap when loaded in browser environment
if (typeof document !== "undefined") {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => initApp());
  } else {
    initApp();
  }
}
