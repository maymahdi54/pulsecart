"""Catalog page object for PulseCart product browsing."""

from __future__ import annotations

from playwright.sync_api import Page

from .base_page import BasePage


class CatalogPage(BasePage):
    """Page object for the PulseCart catalog and product grid."""

    URL_PATH = "/"

    # Locators
    PRODUCT_GRID = '[data-testid="product-grid"]'
    PRODUCT_CARD = '[data-testid="product-card"]'
    PRODUCT_TITLE = '[data-testid^="product-title-"]'
    PRODUCT_PRICE = '[data-testid^="product-price-"]'
    ADD_TO_CART = '[data-testid^="add-to-cart-"]'
    SEARCH_INPUT = '[data-testid="search-input"]'
    CATEGORY_ALL = '[data-testid="category-all"]'
    CATEGORY_ELECTRONICS = '[data-testid="category-electronics"]'
    CATEGORY_AUDIO = '[data-testid="category-audio"]'
    CATEGORY_WEARABLES = '[data-testid="category-wearables"]'
    CART_BADGE = '[data-testid="cart-badge"]'
    CART_SLIDEOVER = '[data-testid="cart-slideover"]'
    CART_CLOSE = '[data-testid="cart-close-btn"]'
    CART_ITEMS = '[data-testid="cart-items"]'
    CART_EMPTY = '[data-testid="cart-empty"]'
    CART_ITEM = '[data-testid="cart-item"]'
    CART_SUBTOTAL = '[data-testid="cart-subtotal"]'
    CART_TAX = '[data-testid="cart-tax"]'
    CART_TOTAL = '[data-testid="cart-total"]'
    BTN_CHECKOUT = '[data-testid="btn-checkout"]'
    QTY_MINUS = '[data-testid^="qty-minus-"]'
    QTY_PLUS = '[data-testid^="qty-plus-"]'
    QTY_INPUT = '[data-testid^="qty-input-"]'
    REMOVE_ITEM = '[data-testid^="remove-"]'

    def open(self) -> None:
        self.goto()
        self.wait_for_selector(self.PRODUCT_GRID)

    def search(self, query: str) -> None:
        self.fill(self.SEARCH_INPUT, query)

    def filter_category(self, category: str) -> None:
        mapping = {
            "all": self.CATEGORY_ALL,
            "electronics": self.CATEGORY_ELECTRONICS,
            "audio": self.CATEGORY_AUDIO,
            "wearables": self.CATEGORY_WEARABLES,
        }
        self.click(mapping[category])

    def add_to_cart(self, product_index: int = 0) -> None:
        buttons = self.page.locator(self.ADD_TO_CART)
        buttons.nth(product_index).click()

    def get_product_count(self) -> int:
        return self.page.locator(self.PRODUCT_CARD).count()

    def get_cart_badge(self) -> str:
        return self.get_text(self.CART_BADGE)

    def open_cart(self) -> None:
        self.click('[data-testid="nav-cart-btn"]')
        self.wait_for_selector(self.CART_SLIDEOVER)

    def close_cart(self) -> None:
        self.click(self.CART_CLOSE)

    def is_cart_empty(self) -> bool:
        return self.is_visible(self.CART_EMPTY)

    def get_cart_item_count(self) -> int:
        return self.page.locator(self.CART_ITEM).count()

    def remove_cart_item(self, index: int = 0) -> None:
        buttons = self.page.locator(self.REMOVE_ITEM)
        buttons.nth(index).click()

    def get_cart_subtotal(self) -> str:
        return self.get_text(self.CART_SUBTOTAL)

    def get_cart_tax(self) -> str:
        return self.get_text(self.CART_TAX)

    def get_cart_total(self) -> str:
        return self.get_text(self.CART_TOTAL)

    def go_to_checkout(self) -> None:
        self.click(self.BTN_CHECKOUT)
