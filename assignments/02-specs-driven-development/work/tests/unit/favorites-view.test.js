import { test, describe, beforeEach } from "node:test";
import assert from "node:assert/strict";
import { FavoritesView } from "../../src/js/ui/favorites-view.js";

function createMockElement() {
  const attributes = new Map();
  const classListSet = new Set();
  const children = [];

  const eventListeners = new Map();

  const el = {
    textContent: "",
    innerHTML: "",
    style: {},
    children,
    setAttribute(name, value) { attributes.set(name, String(value)); },
    getAttribute(name) { return attributes.get(name) || null; },
    classList: {
      add(cls) { classListSet.add(cls); },
      remove(cls) { classListSet.delete(cls); },
      contains(cls) { return classListSet.has(cls); }
    },
    appendChild(child) { children.push(child); },
    querySelectorAll() { return []; },
    addEventListener(event, fn) {
      if (!eventListeners.has(event)) eventListeners.set(event, []);
      eventListeners.get(event).push(fn);
    }
  };
  return el;
}

describe("FavoritesView (US4)", () => {
  let drawer;
  let backdrop;
  let list;
  let emptyState;
  let countBadge;
  let view;
  let removedIds;

  beforeEach(() => {
    drawer = createMockElement();
    backdrop = createMockElement();
    list = createMockElement();
    emptyState = createMockElement();
    countBadge = createMockElement();
    removedIds = [];

    view = new FavoritesView({
      drawerElement: drawer,
      backdropElement: backdrop,
      listElement: list,
      emptyElement: emptyState,
      countBadgeElement: countBadge,
      onRemoveFavorite: (id) => removedIds.push(id)
    });
  });

  test("should open and close drawer modifying classes and aria attributes", () => {
    view.open();
    assert.equal(drawer.classList.contains("is-open"), true);
    assert.equal(backdrop.classList.contains("is-open"), true);
    assert.equal(drawer.getAttribute("aria-hidden"), "false");
    assert.equal(view.isOpen(), true);

    view.close();
    assert.equal(drawer.classList.contains("is-open"), false);
    assert.equal(backdrop.classList.contains("is-open"), false);
    assert.equal(drawer.getAttribute("aria-hidden"), "true");
    assert.equal(view.isOpen(), false);
  });

  test("should render empty state when no favorites exist", () => {
    view.renderFavorites([]);
    assert.equal(emptyState.style.display, "block");
    assert.equal(list.style.display, "none");
    assert.equal(countBadge.style.display, "none");
  });

  test("should render list items and badge when favorites exist", () => {
    const favorites = [
      { id: "q1", text: "Quote One", author: "Author One" },
      { id: "q2", text: "Quote Two", author: "Author Two" }
    ];

    view.renderFavorites(favorites);
    assert.equal(emptyState.style.display, "none");
    assert.equal(list.style.display, "flex");
    assert.equal(countBadge.style.display, "inline-block");
    assert.equal(countBadge.textContent, "2");
    assert.ok(list.innerHTML.includes("Quote One"));
    assert.ok(list.innerHTML.includes("Author Two"));
  });
});
