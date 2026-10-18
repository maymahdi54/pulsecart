"""Checkout validation tests for PulseCart."""

from __future__ import annotations

import pytest

from pages.catalog_page import CatalogPage
from pages.checkout_page import CheckoutPage

pytestmark = pytest.mark.checkout


def test_checkout_valid_details_places_order(catalog_page: CatalogPage, checkout_page: CheckoutPage) -> None:
    """Valid checkout details place an order and show the success screen."""
    catalog_page.open()
    catalog_page.add_to_cart(0)
    checkout_page.open_modal()
    checkout_page.fill_form(
        name="John Doe",
        email="john@example.com",
        address="123 Main Street",
        card="1234 5678 9012 3456",
    )
    checkout_page.submit()
    assert checkout_page.is_success_visible()


def test_checkout_empty_form_shows_errors(checkout_page: CheckoutPage) -> None:
    """Submitting an empty checkout form shows all field errors."""
    checkout_page.open_modal()
    checkout_page.submit()
    assert checkout_page.get_error_name() != ""
    assert checkout_page.get_error_email() != ""
    assert checkout_page.get_error_address() != ""
    assert checkout_page.get_error_card() != ""


def test_checkout_invalid_email_shows_error(checkout_page: CheckoutPage) -> None:
    """An invalid email address shows an email error."""
    checkout_page.open_modal()
    checkout_page.fill_form(
        name="John Doe",
        email="not-an-email",
        address="123 Main Street",
        card="1234 5678 9012 3456",
    )
    checkout_page.submit()
    assert checkout_page.get_error_email() != ""


def test_checkout_short_card_shows_error(checkout_page: CheckoutPage) -> None:
    """A card number with fewer than 16 digits shows a card error."""
    checkout_page.open_modal()
    checkout_page.fill_form(
        name="John Doe",
        email="john@example.com",
        address="123 Main Street",
        card="1234",
    )
    checkout_page.submit()
    assert checkout_page.get_error_card() != ""
