"""Catalog and cart tests for PulseCart."""

from __future__ import annotations

import pytest

from pages.catalog_page import CatalogPage

pytestmark = pytest.mark.catalog


def test_product_grid_displays(catalog_page: CatalogPage) -> None:
    """The product grid renders at least one product card."""
    catalog_page.open()
    assert catalog_page.get_product_count() > 0


def test_category_filter_electronics(catalog_page: CatalogPage) -> None:
    """Filtering by Electronics shows only electronics products."""
    catalog_page.open()
    catalog_page.filter_category("electronics")
    # After filtering, all visible product cards should be electronics
    cards = catalog_page.page.locator('[data-testid="product-card"]')
    for i in range(cards.count()):
        category_el = cards.nth(i).locator('.product-category')
        assert "electronics" in category_el.inner_text().lower()


def test_add_to_cart_updates_badge(catalog_page: CatalogPage) -> None:
    """Adding a product to the cart updates the cart badge count."""
    catalog_page.open()
    catalog_page.add_to_cart(0)
    badge = catalog_page.get_cart_badge()
    assert badge == "1"


def test_add_multiple_to_cart(catalog_page: CatalogPage) -> None:
    """Adding multiple products updates the badge with the total quantity."""
    catalog_page.open()
    catalog_page.add_to_cart(0)
    catalog_page.add_to_cart(1)
    badge = catalog_page.get_cart_badge()
    assert badge == "2"


def test_remove_from_cart(catalog_page: CatalogPage) -> None:
    """Removing an item from the cart decrements the badge."""
    catalog_page.open()
    catalog_page.add_to_cart(0)
    catalog_page.open_cart()
    assert catalog_page.get_cart_item_count() >= 1
    catalog_page.remove_cart_item(0)
    catalog_page.page.wait_for_timeout(300)
    # Cart may be empty now
    badge = catalog_page.get_cart_badge()
    badge_count = int(badge) if badge and badge.isdigit() else 0
    assert badge_count == 0
