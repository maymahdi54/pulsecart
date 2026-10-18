"""Authentication tests for PulseCart."""

from __future__ import annotations

import pytest

from pages.login_page import LoginPage

pytestmark = pytest.mark.auth


def test_valid_login_success(login_page: LoginPage) -> None:
    """Valid credentials log the user in and show the welcome screen."""
    login_page.open_modal()
    login_page.login("testuser", "password123")
    assert login_page.is_success_visible()
    assert login_page.get_logged_in_user() == "testuser"


def test_invalid_username_shows_error(login_page: LoginPage) -> None:
    """Invalid username shows an error message."""
    login_page.open_modal()
    login_page.login("wronguser", "password123")
    assert "Invalid" in login_page.get_error_username() or "required" in login_page.get_error_username()


def test_invalid_password_shows_error(login_page: LoginPage) -> None:
    """Invalid password shows an error message."""
    login_page.open_modal()
    login_page.login("testuser", "wrongpassword")
    assert "Invalid" in login_page.get_error_password() or "required" in login_page.get_error_password()


def test_empty_credentials_show_errors(login_page: LoginPage) -> None:
    """Empty username and password show required-field errors."""
    login_page.open_modal()
    login_page.fill_username("")
    login_page.fill_password("")
    login_page.submit()
    assert login_page.get_error_username() != ""
    assert login_page.get_error_password() != ""
