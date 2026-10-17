/**
 * QuoteView Component
 *
 * Manages DOM updates for the main quote card, accessible live regions,
 * and favorite toggle states.
 *
 * Contract: specs/001-quote-of-the-day/contracts/ui.contract.md
 */

export class QuoteView {
  /**
   * @param {object} elements
   * @param {HTMLElement} [elements.container]
   * @param {HTMLElement} [elements.textElement]
   * @param {HTMLElement} [elements.authorElement]
   * @param {HTMLElement} [elements.categoryElement]
   * @param {HTMLElement} [elements.favoriteButton]
   */
  constructor({ container, textElement, authorElement, categoryElement, favoriteButton } = {}) {
    this.container = container;
    this.textElement = textElement;
    this.authorElement = authorElement;
    this.categoryElement = categoryElement;
    this.favoriteButton = favoriteButton;
    this._currentQuote = null;
  }

  /**
   * Renders a quote to the DOM
   * @param {{ id: string, text: string, author: string, category?: string }} quote
   * @param {boolean} [isFavorite=false]
   */
  renderQuote(quote, isFavorite = false) {
    if (!quote) return;
    this._currentQuote = quote;

    if (this.textElement) {
      this.textElement.textContent = `“${quote.text}”`;
    }

    if (this.authorElement) {
      this.authorElement.textContent = `— ${quote.author}`;
    }

    if (this.categoryElement) {
      this.categoryElement.textContent = quote.category || "Inspiration";
    }

    this.setFavoriteState(isFavorite);
  }

  /**
   * Updates the visual and accessible state of the favorite toggle button
   * @param {boolean} isFavorite
   */
  setFavoriteState(isFavorite) {
    if (!this.favoriteButton) return;

    if (isFavorite) {
      this.favoriteButton.classList.add("is-favorite");
      this.favoriteButton.setAttribute("aria-pressed", "true");
      this.favoriteButton.setAttribute("aria-label", "Remove quote from favorites");
    } else {
      this.favoriteButton.classList.remove("is-favorite");
      this.favoriteButton.setAttribute("aria-pressed", "false");
      this.favoriteButton.setAttribute("aria-label", "Add quote to favorites");
    }
  }

  /**
   * Returns the currently rendered quote
   * @returns {{ id: string, text: string, author: string, category?: string } | null}
   */
  getCurrentQuote() {
    return this._currentQuote;
  }
}
