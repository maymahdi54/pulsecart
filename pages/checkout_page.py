"""Checkout page object for PulseCart order validation."""

from __future__ import annotations

from playwright.sync_api import Page

from .base_page import BasePage


class CheckoutPage(BasePage):
    """Page object for the PulseCart checkout modal and validation."""

    URL_PATH = "/"

    # Locators
    CHECKOUT_MODAL = '[data-testid="checkout-modal"]'
    CHECKOUT_CARD = '[data-testid="checkout-card"]'
    CHECKOUT_FORM = '[data-testid="checkout-form"]'
    NAME_INPUT = '[data-testid="checkout-name"]'
    EMAIL_INPUT = '[data-testid="checkout-email"]'
    ADDRESS_INPUT = '[data-testid="checkout-address"]'
    CARD_INPUT = '[data-testid="checkout-card-input"]'
    BTN_SUBMIT = '[data-testid="btn-submit-checkout"]'
    BTN_CANCEL = '[data-testid="btn-cancel-checkout"]'
    BTN_CONTINUE = '[data-testid="btn-continue-shopping"]'
    BTN_CHECKOUT = '[data-testid="btn-checkout"]'
    CART_SLIDEOVER = '[data-testid="cart-slideover"]'
    ERROR_NAME = '[data-testid="error-fullname"]'
    ERROR_EMAIL = '[data-testid="error-email"]'
    ERROR_ADDRESS = '[data-testid="error-address"]'
    ERROR_CARD = '[data-testid="error-card"]'
    ERROR_GENERAL = '[data-testid="checkout-error-general"]'
    CHECKOUT_SUCCESS = '[data-testid="checkout-success"]'

    def open(self) -> None:
        self.goto()
        self.wait_for_selector(self.CHECKOUT_MODAL)

    def open_modal(self) -> None:
        self.goto()
        self.click('[data-testid="nav-cart-btn"]')
        self.wait_for_selector(self.CART_SLIDEOVER)
        self.click(self.BTN_CHECKOUT)
        self.wait_for_selector(self.CHECKOUT_MODAL)

    def fill_name(self, value: str) -> None:
        self.fill(self.NAME_INPUT, value)

    def fill_email(self, value: str) -> None:
        self.fill(self.EMAIL_INPUT, value)

    def fill_address(self, value: str) -> None:
        self.fill(self.ADDRESS_INPUT, value)

    def fill_card(self, value: str) -> None:
        self.fill(self.CARD_INPUT, value)

    def submit(self) -> None:
        submit_btn = self.page.locator(self.BTN_SUBMIT)
        submit_btn.evaluate("el => el.click()")
        self.page.wait_for_timeout(1000)

    def cancel(self) -> None:
        self.click(self.BTN_CANCEL)

    def continue_shopping(self) -> None:
        self.click(self.BTN_CONTINUE)

    def get_error_name(self) -> str:
        return self.get_text(self.ERROR_NAME)

    def get_error_email(self) -> str:
        return self.get_text(self.ERROR_EMAIL)

    def get_error_address(self) -> str:
        return self.get_text(self.ERROR_ADDRESS)

    def get_error_card(self) -> str:
        return self.get_text(self.ERROR_CARD)

    def get_error_general(self) -> str:
        return self.get_text(self.ERROR_GENERAL)

    def is_success_visible(self) -> bool:
        return self.is_visible(self.CHECKOUT_SUCCESS)

    def is_modal_visible(self) -> bool:
        return self.is_visible(self.CHECKOUT_MODAL)

    def fill_form(
        self,
        name: str = "",
        email: str = "",
        address: str = "",
        card: str = "",
    ) -> None:
        self.fill_name(name)
        self.fill_email(email)
        self.fill_address(address)
        self.fill_card(card)
