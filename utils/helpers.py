"""Shared test helper utilities for PulseCart."""

from __future__ import annotations

import re
from typing import Optional


def format_currency(amount: float) -> str:
    """Format a numeric amount as a currency string."""
    return f"${amount:,.2f}"


def parse_currency(value: str) -> Optional[float]:
    """Parse a currency string like '$1,234.56' into a float."""
    cleaned = value.replace("$", "").replace(",", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return None


def is_valid_email(email: str) -> bool:
    """Return True if the string looks like a valid email address."""
    return bool(re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email))


def is_valid_card(card: str) -> bool:
    """Return True if the string contains exactly 16 digits."""
    digits = re.sub(r"\D", "", card)
    return len(digits) == 16


def slugify(text: str) -> str:
    """Convert a string to a URL-safe slug."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
