// Built-in Quote Collection
const QUOTES = [
  { id: '1', text: "The only way to do great work is to love what you do.", author: "Steve Jobs" },
  { id: '2', text: "Strive not to be a success, but rather to be of value.", author: "Albert Einstein" },
  { id: '3', text: "The future belongs to those who believe in the beauty of their dreams.", author: "Eleanor Roosevelt" },
  { id: '4', text: "It always seems impossible until it is done.", author: "Nelson Mandela" },
  { id: '5', text: "Do what you can, with what you have, where you are.", author: "Theodore Roosevelt" },
  { id: '6', text: "Act as if what you do makes a difference. It does.", author: "William James" },
  { id: '7', text: "Believe you can and you're halfway there.", author: "Theodore Roosevelt" },
  { id: '8', text: "Quality is not an act, it is a habit.", author: "Aristotle" }
];

const STORAGE_KEY = 'quote_app_favorites';
let currentQuote = null;

// DOM Elements
const quoteTextEl = document.getElementById('quoteText');
const quoteAuthorEl = document.getElementById('quoteAuthor');
const favoriteBtn = document.getElementById('favoriteBtn');
const favTextEl = document.getElementById('favText');
const newQuoteBtn = document.getElementById('newQuoteBtn');
const viewFavoritesBtn = document.getElementById('viewFavoritesBtn');
const favCountEl = document.getElementById('favCount');
const favoritesModal = document.getElementById('favoritesModal');
const closeModalBtn = document.getElementById('closeModalBtn');
const favoritesListEl = document.getElementById('favoritesList');

// LocalStorage Helpers
function getFavorites() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch (e) {
    console.error('Failed to read favorites from localStorage:', e);
    return [];
  }
}

function saveFavorites(favorites) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(favorites));
  } catch (e) {
    console.error('Failed to save favorites to localStorage:', e);
  }
}

function isFavorite(id) {
  return getFavorites().includes(id);
}

function updateFavCount() {
  const favorites = getFavorites();
  favCountEl.textContent = favorites.length;
}

// Display Quote
function displayQuote(quote) {
  currentQuote = quote;
  quoteTextEl.textContent = quote.text;
  quoteAuthorEl.textContent = `— ${quote.author}`;
  updateFavoriteButtonState();
}

function getRandomQuote() {
  let availableQuotes = QUOTES;
  if (QUOTES.length > 1 && currentQuote) {
    availableQuotes = QUOTES.filter(q => q.id !== currentQuote.id);
  }
  const randomIndex = Math.floor(Math.random() * availableQuotes.length);
  return availableQuotes[randomIndex];
}

function updateFavoriteButtonState() {
  if (!currentQuote) return;
  const faved = isFavorite(currentQuote.id);
  if (faved) {
    favoriteBtn.classList.add('active');
    favTextEl.textContent = 'Favorited';
  } else {
    favoriteBtn.classList.remove('active');
    favTextEl.textContent = 'Favorite';
  }
  updateFavCount();
}

// Event Listeners
newQuoteBtn.addEventListener('click', () => {
  displayQuote(getRandomQuote());
});

favoriteBtn.addEventListener('click', () => {
  if (!currentQuote) return;
  let favorites = getFavorites();
  if (favorites.includes(currentQuote.id)) {
    favorites = favorites.filter(id => id !== currentQuote.id);
  } else {
    favorites.push(currentQuote.id);
  }
  saveFavorites(favorites);
  updateFavoriteButtonState();
});

// Modal Logic
function renderFavoritesModal() {
  const favoriteIds = getFavorites();
  const favQuotes = QUOTES.filter(q => favoriteIds.includes(q.id));

  favoritesListEl.innerHTML = '';
  if (favQuotes.length === 0) {
    favoritesListEl.innerHTML = '<p style="color: var(--text-secondary); text-align: center; padding: 2rem 0;">No favorite quotes saved yet!</p>';
    return;
  }

  favQuotes.forEach(q => {
    const item = document.createElement('div');
    item.className = 'fav-item';
    item.innerHTML = `
      <div class="fav-item-content">
        <p>"${q.text}"</p>
        <span>— ${q.author}</span>
      </div>
      <button class="btn-remove-fav" data-id="${q.id}" title="Remove from favorites">&times;</button>
    `;

    item.querySelector('.btn-remove-fav').addEventListener('click', (e) => {
      const idToRemove = e.currentTarget.getAttribute('data-id');
      const updated = getFavorites().filter(id => id !== idToRemove);
      saveFavorites(updated);
      renderFavoritesModal();
      updateFavoriteButtonState();
    });

    favoritesListEl.appendChild(item);
  });
}

viewFavoritesBtn.addEventListener('click', () => {
  renderFavoritesModal();
  favoritesModal.classList.remove('hidden');
});

closeModalBtn.addEventListener('click', () => {
  favoritesModal.classList.add('hidden');
});

favoritesModal.addEventListener('click', (e) => {
  if (e.target === favoritesModal) {
    favoritesModal.classList.add('hidden');
  }
});

// Initialization
displayQuote(getRandomQuote());
updateFavCount();
