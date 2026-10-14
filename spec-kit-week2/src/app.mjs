import {
  QUOTES,
  loadFavorites,
  persistFavorites,
  selectQuote,
  toggleFavorite,
} from './quote-state.mjs';

const quoteText = document.getElementById('quote-text');
const quoteAttribution = document.getElementById('quote-attribution');
const newQuoteButton = document.getElementById('new-quote-button');
const favoriteButton = document.getElementById('favorite-button');
const favoriteButtonLabel = document.getElementById('favorite-button-label');
const favoriteIcon = document.querySelector('.favorite-icon');
const favoritesPanel = document.getElementById('favorites-panel');
const favoritesToggle = document.getElementById('favorites-toggle');
const favoritesContent = document.getElementById('favorites-content');
const pageGrid = document.querySelector('.page-grid');
const favoritesList = document.getElementById('favorites-list');
const emptyState = document.getElementById('empty-state');
const favoriteCount = document.getElementById('favorite-count');
const storageStatus = document.getElementById('storage-status');
const favoriteToast = document.getElementById('favorite-toast');
const favoriteToastMessage = document.getElementById('favorite-toast-message');
const todayDate = document.getElementById('today-date');

let currentQuoteId = null;
let favoriteIds = [];
let toastTimeout = null;
let toastHideTimeout = null;

const TOAST_DURATION_MS = 5000;
const TOAST_TRANSITION_MS = 220;

function renderQuote(quote) {
  quoteText.textContent = quote.text;
  quoteAttribution.textContent = quote.attribution ?? '';
  currentQuoteId = quote.id;
  renderFavoriteButton();
}

function renderFavoriteButton() {
  const isFavorite = favoriteIds.includes(currentQuoteId);

  favoriteButton.setAttribute('aria-pressed', String(isFavorite));
  favoriteButtonLabel.textContent = isFavorite ? 'Remove favorite' : 'Save favorite';
  favoriteIcon.textContent = isFavorite ? '\u2665' : '\u2661';
}

function renderFavorites() {
  favoritesList.replaceChildren();
  emptyState.hidden = favoriteIds.length > 0;
  favoriteCount.textContent = String(favoriteIds.length).padStart(2, '0');
  favoriteCount.setAttribute('aria-label', `${favoriteIds.length} saved quotes`);

  for (const quoteId of favoriteIds) {
    const quote = QUOTES.find((entry) => entry.id === quoteId);
    if (!quote) continue;

    const item = document.createElement('li');
    const text = document.createElement('p');
    const attribution = document.createElement('p');
    const removeButton = document.createElement('button');

    item.className = 'favorite-item';
    text.className = 'favorite-quote';
    text.textContent = quote.text;
    attribution.className = 'favorite-attribution';
    attribution.textContent = quote.attribution ?? '';
    removeButton.className = 'remove-favorite';
    removeButton.type = 'button';
    removeButton.textContent = 'Remove';
    removeButton.setAttribute('aria-label', `Remove favorite: ${quote.text}`);
    removeButton.addEventListener('click', () => changeFavorite(quoteId));

    item.append(text, attribution, removeButton);
    favoritesList.append(item);
  }
}

function showStorageError(message) {
  storageStatus.textContent = message;
  storageStatus.hidden = false;
}

function showFavoriteToast(message) {
  window.clearTimeout(toastTimeout);
  window.clearTimeout(toastHideTimeout);
  favoriteToastMessage.textContent = message;
  favoriteToast.hidden = false;
  requestAnimationFrame(() => favoriteToast.classList.add('is-visible'));

  toastTimeout = window.setTimeout(() => {
    favoriteToast.classList.remove('is-visible');
    toastHideTimeout = window.setTimeout(() => {
      favoriteToast.hidden = true;
    }, TOAST_TRANSITION_MS);
  }, TOAST_DURATION_MS - TOAST_TRANSITION_MS);
}

function setFavoritesExpanded(expanded) {
  favoritesToggle.setAttribute('aria-expanded', String(expanded));
  favoritesToggle.setAttribute('aria-label', `${expanded ? 'Collapse' : 'Expand'} favorites column`);
  favoritesToggle.title = `${expanded ? 'Collapse' : 'Expand'} favorites column`;
  favoritesContent.setAttribute('aria-hidden', String(!expanded));
  favoritesContent.inert = !expanded;
  pageGrid.classList.toggle('is-favorites-collapsed', !expanded);
}

function changeFavorite(quoteId) {
  const wasFavorite = favoriteIds.includes(quoteId);
  const nextFavoriteIds = toggleFavorite(favoriteIds, quoteId);
  let saved = false;

  try {
    saved = persistFavorites(window.localStorage, nextFavoriteIds);
  } catch {
    saved = false;
  }

  if (!saved) {
    showStorageError('Your favorite was not saved. Browser storage may be unavailable.');
    return;
  }

  favoriteIds = nextFavoriteIds;
  storageStatus.textContent = '';
  storageStatus.hidden = true;
  renderFavoriteButton();
  renderFavorites();
  showFavoriteToast(wasFavorite ? 'Removed from favorites.' : 'Added to favorites.');
}

function restoreFavorites() {
  try {
    const result = loadFavorites(window.localStorage);
    favoriteIds = result.favoriteIds;

    if (result.error) {
      showStorageError('Saved favorites could not be restored.');
    }
  } catch {
    favoriteIds = [];
    showStorageError('Saved favorites could not be restored.');
  }
}

function showNewQuote() {
  renderQuote(selectQuote(QUOTES, currentQuoteId));
}

function renderDate() {
  todayDate.textContent = new Intl.DateTimeFormat('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
  }).format(new Date());
}

newQuoteButton.addEventListener('click', showNewQuote);
favoritesToggle.addEventListener('click', () => {
  const isExpanded = favoritesToggle.getAttribute('aria-expanded') === 'true';
  setFavoritesExpanded(!isExpanded);
});
favoriteButton.addEventListener('click', () => {
  if (currentQuoteId) changeFavorite(currentQuoteId);
});
favoriteButton.hidden = false;
favoritesPanel.hidden = false;
setFavoritesExpanded(true);
restoreFavorites();
renderFavorites();
renderDate();
showNewQuote();
