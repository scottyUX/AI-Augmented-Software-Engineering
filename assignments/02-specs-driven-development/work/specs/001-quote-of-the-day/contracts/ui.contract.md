# Contract: UI Components & DOM Interface

**Path**: `src/index.html` & `src/js/ui/`
**Interface Type**: Document Object Model & User Interaction Contract

## DOM Structure & Required Element Selectors

| Element | Selector / ID | ARIA Attributes | Role / Event Contract |
|---|---|---|---|
| Quote Container | `#quote-container` | `aria-live="polite"` | Dynamic region for quote changes |
| Quote Text | `#quote-text` | N/A | Contains quote string inside `<blockquote>` |
| Quote Author | `#quote-author` | N/A | Contains author attribution inside `<cite>` |
| New Quote Button | `#new-quote-btn` | `aria-label="Show new quote"` | `click` -> triggers new quote selection |
| Favorite Toggle Button | `#favorite-toggle-btn` | `aria-pressed="false|true"`, `aria-label="Add quote to favorites"` | `click` -> toggles active quote's favorite status |
| Toggle Favorites Drawer | `#toggle-favorites-btn` | `aria-expanded="false|true"`, `aria-controls="favorites-drawer"` | `click` -> opens/closes saved favorites panel |
| Favorites Drawer Panel | `#favorites-drawer` | `role="region"`, `aria-label="Saved Favorite Quotes"` | Contains list of favorited quotes |
| Favorites List | `#favorites-list` | `role="list"` | Renders items with text, author, and remove button |
| Remove Favorite Button | `.remove-favorite-btn[data-quote-id]` | `aria-label="Remove quote from favorites"` | `click` -> removes quote from favorites |
| Storage Warning Banner | `#storage-warning` | `role="status"`, `aria-live="polite"` | Visible only when `storage.isPersistent() === false` |

## Visual State Indicators
- **Favorite Active**: Button contains `.is-favorite` class, icon filled, `aria-pressed="true"`.
- **Favorite Inactive**: Button lacks `.is-favorite` class, icon outlined, `aria-pressed="false"`.
- **Drawer Open/Closed**: Container has `.is-open` class, `aria-expanded="true"`.
