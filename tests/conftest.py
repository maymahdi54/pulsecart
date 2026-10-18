"""Shared pytest fixtures for PulseCart tests.

Starts a local HTTP server serving the app/ directory, launches a
Playwright browser context, and captures screenshots on test failure.
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from typing import Generator

import pytest
from playwright.sync_api import Page, sync_playwright

from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.catalog_page import CatalogPage
from pages.checkout_page import CheckoutPage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.join(ROOT, "app")
SCREENSHOT_DIR = os.path.join(ROOT, "reports", "screenshots")
TRACE_DIR = os.path.join(ROOT, "reports", "traces")
BASE_URL = "http://localhost:8765"


@pytest.fixture(scope="session")
def http_server() -> Generator[str, None, None]:
    """Start a local HTTP server serving the app/ directory."""
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    os.makedirs(TRACE_DIR, exist_ok=True)

    proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8765", "--directory", APP_DIR],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    # Wait for server to be ready
    for _ in range(50):
        try:
            import urllib.request
            urllib.request.urlopen(BASE_URL, timeout=1)
            break
        except Exception:
            time.sleep(0.1)
    else:
        proc.terminate()
        raise RuntimeError("HTTP server did not start in time")

    yield BASE_URL

    proc.terminate()
    proc.wait(timeout=5)


@pytest.fixture(scope="function")
def page(http_server: str, request) -> Generator[Page, None, None]:
    """Launch a headful browser page with tracing and screenshot-on-failure."""
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    os.makedirs(TRACE_DIR, exist_ok=True)

    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True, slow_mo=400)
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page_obj = context.new_page()

    test_name = request.node.name
    failed_before = request.session.testsfailed

    yield page_obj

    # Capture screenshot on failure
    if request.session.testsfailed > failed_before:
        screenshot_path = os.path.join(SCREENSHOT_DIR, f"{test_name}.png")
        try:
            page_obj.screenshot(path=screenshot_path, full_page=True)
        except Exception:
            pass

    context.tracing.stop(path=os.path.join(TRACE_DIR, f"{test_name}.zip"))
    context.close()
    browser.close()
    playwright.stop()


@pytest.fixture
def base_page(page: Page) -> BasePage:
    return BasePage(page)


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def catalog_page(page: Page) -> CatalogPage:
    return CatalogPage(page)


@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:
    return CheckoutPage(page)
