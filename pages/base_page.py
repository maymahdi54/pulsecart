"""Base page object wrapping common Playwright actions."""

from __future__ import annotations

from typing import Optional

from playwright.sync_api import Page, expect


class BasePage:
    """Base page object providing common Playwright helpers."""

    def __init__(self, page: Page, base_url: str = "http://localhost:8765") -> None:
        self.page = page
        self.base_url = base_url

    def goto(self, path: str = "/") -> None:
        self.page.goto(self.base_url + path)

    def click(self, selector: str) -> None:
        self.page.click(selector, force=True)

    def fill(self, selector: str, value: str) -> None:
        self.page.fill(selector, value)

    def wait_for_selector(self, selector: str, timeout: int = 5000) -> None:
        self.page.wait_for_selector(selector, timeout=timeout)

    def get_text(self, selector: str) -> str:
        return self.page.inner_text(selector)

    def get_attribute(self, selector: str, attribute: str) -> Optional[str]:
        return self.page.get_attribute(selector, attribute)

    def is_visible(self, selector: str) -> bool:
        return self.page.is_visible(selector)

    def expect_visible(self, selector: str) -> None:
        expect(self.page.locator(selector)).to_be_visible()

    def expect_hidden(self, selector: str) -> None:
        expect(self.page.locator(selector)).to_be_hidden()

    def expect_text(self, selector: str, expected: str) -> None:
        expect(self.page.locator(selector)).to_have_text(expected)

    def screenshot(self, path: str) -> None:
        self.page.screenshot(path=path, full_page=True)
