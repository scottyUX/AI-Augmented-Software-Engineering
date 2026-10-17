/**
 * FavoritesView Component
 *
 * Manages rendering of the saved favorites list, empty states,
 * badge counters, and drawer panel open/close interactions.
 *
 * Contract: specs/001-quote-of-the-day/contracts/ui.contract.md
 */

export class FavoritesView {
  /**
   * @param {object} options
   * @param {HTMLElement} [options.drawerElement]
   * @param {HTMLElement} [options.backdropElement]
   * @param {HTMLElement} [options.listElement]
   * @param {HTMLElement} [options.emptyElement]
   * @param {HTMLElement} [options.countBadgeElement]
   * @param {(quoteId: string) => void} [options.onRemoveFavorite]
   */
  constructor({
    drawerElement,
    backdropElement,
    listElement,
    emptyElement,
    countBadgeElement,
    onRemoveFavorite
  } = {}) {
    this.drawerElement = drawerElement;
    this.backdropElement = backdropElement;
    this.listElement = listElement;
    this.emptyElement = emptyElement;
    this.countBadgeElement = countBadgeElement;
    this.onRemoveFavorite = onRemoveFavorite;
    this._isOpen = false;
  }

  /**
   * Opens the favorites drawer
   */
  open() {
    this._isOpen = true;
    if (this.drawerElement) {
      this.drawerElement.classList.add("is-open");
      this.drawerElement.setAttribute("aria-hidden", "false");
    }
    if (this.backdropElement) {
      this.backdropElement.classList.add("is-open");
      this.backdropElement.setAttribute("aria-hidden", "false");
    }
  }

  /**
   * Closes the favorites drawer
   */
  close() {
    this._isOpen = false;
    if (this.drawerElement) {
      this.drawerElement.classList.remove("is-open");
      this.drawerElement.setAttribute("aria-hidden", "true");
    }
    if (this.backdropElement) {
      this.backdropElement.classList.remove("is-open");
      this.backdropElement.setAttribute("aria-hidden", "true");
    }
  }

  /**
   * Checks if drawer is currently open
   * @returns {boolean}
   */
  isOpen() {
    return this._isOpen;
  }

  /**
   * Renders the list of favorite quotes
   * @param {Array<{ id: string, text: string, author: string }>} favoriteQuotes
   */
  renderFavorites(favoriteQuotes = []) {
    const count = favoriteQuotes.length;

    // Update count badge
    if (this.countBadgeElement) {
      if (count > 0) {
        this.countBadgeElement.textContent = String(count);
        this.countBadgeElement.style.display = "inline-block";
      } else {
        this.countBadgeElement.style.display = "none";
      }
    }

    if (!this.listElement || !this.emptyElement) return;

    if (count === 0) {
      this.emptyElement.style.display = "block";
      this.listElement.style.display = "none";
      this.listElement.innerHTML = "";
      return;
    }

    this.emptyElement.style.display = "none";
    this.listElement.style.display = "flex";

    // Build list items safely
    this.listElement.innerHTML = favoriteQuotes
      .map(
        (quote) => `
        <li class="favorite-item" data-id="${this._escapeHtml(quote.id)}">
          <p class="favorite-item-text">“${this._escapeHtml(quote.text)}”</p>
          <div class="favorite-item-footer">
            <span class="favorite-item-author">— ${this._escapeHtml(quote.author)}</span>
            <button class="btn-remove-favorite" type="button" data-id="${this._escapeHtml(quote.id)}" aria-label="Remove quote by ${this._escapeHtml(quote.author)} from favorites">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                <line x1="10" y1="11" x2="10" y2="17"></line>
                <line x1="14" y1="11" x2="14" y2="17"></line>
              </svg>
            </button>
          </div>
        </li>
      `
      )
      .join("");

    // Wire remove buttons
    if (typeof this.listElement.querySelectorAll === "function") {
      const removeButtons = this.listElement.querySelectorAll(".btn-remove-favorite");
      removeButtons.forEach((btn) => {
        btn.addEventListener("click", () => {
          const id = btn.getAttribute("data-id");
          if (id && this.onRemoveFavorite) {
            this.onRemoveFavorite(id);
          }
        });
      });
    }
  }

  /**
   * Helper to escape HTML characters
   * @private
   */
  _escapeHtml(str) {
    if (!str) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }
}
