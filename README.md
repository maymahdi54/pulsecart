# PulseCart

E-Commerce Test Automation Framework built with Playwright, pytest, and the Page Object Model.

## Overview

PulseCart is a lightweight e-commerce demo application paired with an end-to-end test suite. The framework uses Playwright for browser automation, pytest for test orchestration, and the Page Object Model to keep selectors and interactions maintainable.

## Project Structure

```
app/        # Frontend application (HTML, CSS, JS)
pages/      # Page object models
tests/      # pytest test suites
utils/      # Helper utilities
reports/    # Generated HTML reports, screenshots, and traces
```

## Installation

```bash
pip install -r requirements.txt
playwright install
```

## Running Tests

```bash
pytest
```

Reports are generated under `reports/`.

## License

See `UNLICENSE`.