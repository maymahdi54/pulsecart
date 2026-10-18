"""Login page object for PulseCart authentication."""

from __future__ import annotations

from playwright.sync_api import Page

from .base_page import BasePage


class LoginPage(BasePage):
    """Page object for the PulseCart login modal."""

    URL_PATH = "/"

    # Locators
    LOGIN_MODAL = '[data-testid="login-modal"]'
    LOGIN_CARD = '[data-testid="login-card"]'
    USERNAME_INPUT = '[data-testid="login-username"]'
    PASSWORD_INPUT = '[data-testid="login-password"]'
    LOGIN_SUBMIT = '[data-testid="login-submit"]'
    LOGIN_CLOSE = '[data-testid="login-close-btn"]'
    LOGIN_CANCEL = '[data-testid="btn-cancel-login"]'
    ERROR_USERNAME = '[data-testid="error-username"]'
    ERROR_PASSWORD = '[data-testid="error-password"]'
    ERROR_GENERAL = '[data-testid="login-error-general"]'
    LOGIN_SUCCESS = '[data-testid="login-success"]'
    LOGGED_IN_USER = '[data-testid="logged-in-user"]'
    CONTINUE_LOGIN = '[data-testid="btn-continue-login"]'

    def open(self) -> None:
        self.goto()
        self.wait_for_selector(self.LOGIN_MODAL)

    def open_modal(self) -> None:
        self.goto()
        self.click('[data-testid="nav-login-btn"]')
        self.wait_for_selector(self.LOGIN_MODAL)
        self.expect_visible(self.LOGIN_MODAL)

    def fill_username(self, value: str) -> None:
        self.fill(self.USERNAME_INPUT, value)

    def fill_password(self, value: str) -> None:
        self.fill(self.PASSWORD_INPUT, value)

    def submit(self) -> None:
        self.click(self.LOGIN_SUBMIT)
        self.page.wait_for_timeout(1000)

    def close(self) -> None:
        self.click(self.LOGIN_CLOSE)

    def cancel(self) -> None:
        self.click(self.LOGIN_CANCEL)

    def get_error_username(self) -> str:
        return self.get_text(self.ERROR_USERNAME)

    def get_error_password(self) -> str:
        return self.get_text(self.ERROR_PASSWORD)

    def get_error_general(self) -> str:
        return self.get_text(self.ERROR_GENERAL)

    def is_success_visible(self) -> bool:
        return self.is_visible(self.LOGIN_SUCCESS)

    def get_logged_in_user(self) -> str:
        return self.get_text(self.LOGGED_IN_USER)

    def is_modal_visible(self) -> bool:
        return self.is_visible(self.LOGIN_MODAL)

    def login(self, username: str, password: str) -> None:
        self.fill_username(username)
        self.fill_password(password)
        self.submit()
        self.page.wait_for_timeout(300)
