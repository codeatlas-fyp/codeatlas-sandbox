# CodeAtlas Sandbox

A deliberately tiny library-management Python app used as the **target codebase**
for CodeAtlas scenario pull requests. CodeAtlas evaluates PRs on *this* repo
during the mid-eval demo.

**Important:** this repo is not CodeAtlas. CodeAtlas lives in
[`codeatlas-fyp/codeatlas`](https://github.com/codeatlas-fyp/codeatlas).
This repo is the thing CodeAtlas looks at.

## Layout

```
books.py              # Catalog of books (ISBN, title, author)
loans.py              # Loan ledger (borrow, return, overdue tracking)
payments/
├── __init__.py
└── fees.py           # Late-fee calculation + waiver policy
CODEOWNERS            # Ownership rules — last-match wins, GitHub semantics
tests/test_smoke.py   # Six fast tests proving everything imports and runs
pyproject.toml
```

## Running the tests

```bash
uv sync --extra dev   # or: pip install pytest
uv run pytest
```

## Why this exists

The mid-eval demo needs real pull requests against a real repo so CodeAtlas can
show it works end to end. Each scenario PR (see `SCENARIOS.md`) is designed to
trigger exactly one contradiction case (C2, C5, C9, or none for the PASS case).

See `SCENARIOS.md` for the step-by-step guide to opening those PRs.
