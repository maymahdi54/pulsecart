# PulseCart

PulseCart is a modern, interactive e-commerce web application paired with an
industry-standard Playwright + pytest test automation framework. Built as a
portfolio project, it demonstrates Page Object Model (POM) architecture,
end-to-end UI testing, positive/negative validation, and CI integration.

Completely copyright-free (Unlicense/Public Domain). No third-party images,
commercial logos, icons, fonts, or copyrighted code snippets — all UI is built
with pure CSS shapes and inline SVG vectors created in-code.

## Repository Layout

```
PulseCart/
├── UNLICENSE                    # Public domain dedication
├── LICENSE                      # Unlicense text
├── requirements.txt             # Python dependencies
├── pytest.ini                   # Pytest + pytest-html configuration
├── README.md                    # This file
├── .gitignore                   # Python, pytest, Playwright, OS ignores
├── app/                         # E-commerce frontend (HTML/CSS/JS)
│   ├── index.html               # PulseCart store UI
│   ├── styles.css               # Dark/modern theme
│   └── app.js                   # Vanilla JS application logic
├── pages/                       # Playwright Page Object Model
│   ├── __init__.py
│   ├── base_page.py             # Base page with common helpers
│   ├── login_page.py            # Login modal page object
│   ├── catalog_page.py          # Catalog & cart page object
│   └── checkout_page.py         # Checkout modal page object
├── tests/                       # Pytest test suites
│   ├── __init__.py
│   ├── conftest.py              # HTTP server + browser fixtures
│   ├── test_authentication.py   # Login / logout tests
│   ├── test_catalog_and_cart.py # Product browse & cart tests
│   └── test_checkout_validation.py # Checkout validation tests
├── utils/                       # Shared test utilities
│   ├── __init__.py
│   └── helpers.py
├── reports/                     # Generated test reports
│   └── .gitkeep
└── .github/
    └── workflows/
        └── tests.yml            # GitHub Actions CI
```

## Features

### Store UI (`app/`)
- Dark/modern aesthetic (`#0f172a`, cyan `#06b6d4` accents)
- Top navigation: logo, live search, cart count badge, user login status
- Category navigation: All, Electronics, Audio, Wearables
- Product grid with dynamic product cards
- Slide-over shopping cart with add/remove, quantity controls, subtotal/tax/total
- Checkout modal with form validation (name, email, address, 16-digit card)
- Login modal with credential validation
- All interactive elements carry `data-testid` attributes for automation

### Test Automation (`pages/` + `tests/`)
- **Page Object Model**: `BasePage` wraps Playwright actions; dedicated pages for
  login, catalog, and checkout
- **Authentication tests**: valid login, invalid username/password, empty credentials
- **Catalog & cart tests**: product grid display, category filtering, add to cart,
  cart badge updates, remove from cart
- **Checkout tests**: valid order placement, empty form errors, invalid email,
  short card number
- **Fixtures**: local HTTP server, headful browser with slow-mo, tracing,
  automatic screenshot capture on failure

## Test Credentials

| Field | Value |
|-------|-------|
| Username | `testuser` |
| Password | `password123` |

## Local Run

```bash
# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Run tests (generates reports/report.html)
pytest

# Run with HTML report explicitly
pytest --html=reports/report.html --self-contained-html

# Run specific marker
pytest -m auth
pytest -m catalog
pytest -m checkout
```

## CI

GitHub Actions (`.github/workflows/tests.yml`) runs on every push and pull
request:
- Python 3.10 setup
- Dependency installation from `requirements.txt`
- Playwright Chromium install + system deps
- `pytest` execution with HTML report

## Architecture

### Page Object Model
- `pages/base_page.py` — `BasePage` wraps `click`, `fill`, `wait_for_selector`,
  `get_text`, `get_attribute`, `is_visible`, and assertion helpers
- `pages/login_page.py` — `LoginPage` encapsulates login modal locators and
  actions (fill credentials, submit, read errors)
- `pages/catalog_page.py` — `CatalogPage` encapsulates product grid, category
  filter, search, add-to-cart, cart slideover interactions
- `pages/checkout_page.py` — `CheckoutPage` encapsulates checkout form fields,
  validation errors, submit, and success state

### Testing Strategy
- **E2E**: Full flows from product browse → cart → checkout → success
- **Positive**: Valid credentials, valid checkout details, successful add-to-cart
- **Negative**: Invalid username/password, empty checkout form, malformed email,
  short card number
- **UI**: Headful Chromium with `slow_mo` for visible navigation, tracing and
  screenshots captured on failure

## License

Dedicated to the public domain under the Unlicense. See `UNLICENSE` and
`LICENSE` for details.
