"""Smoke tests: the sandbox app actually runs. Not exhaustive — this is a toy."""

from datetime import date
from decimal import Decimal

from books import Book, Catalog
from loans import LoanLedger
from payments.fees import DAILY_LATE_FEE, calculate_late_fee, is_fee_waivable


def test_catalog_add_and_find() -> None:
    cat = Catalog()
    book = Book(isbn="978-0", title="Clean Code", author="Martin", year=2008)
    cat.add(book)
    assert cat.find("978-0") == book
    assert cat.count() == 1


def test_loan_lifecycle_marks_returned() -> None:
    ledger = LoanLedger()
    ledger.borrow(isbn="978-0", borrower_id="u1", when=date(2026, 10, 1))
    assert len(ledger.open_loans()) == 1
    ledger.return_book(isbn="978-0", when=date(2026, 10, 5))
    assert ledger.open_loans() == []


def test_late_fee_zero_when_not_overdue() -> None:
    assert calculate_late_fee(0) == Decimal("0.00")


def test_late_fee_scales_with_days() -> None:
    assert calculate_late_fee(3) == DAILY_LATE_FEE * 3


def test_late_fee_capped() -> None:
    assert calculate_late_fee(10_000) == Decimal("10.00")


def test_first_offence_short_delay_is_waivable() -> None:
    assert is_fee_waivable(days_overdue=3, is_first_offence=True) is True
    assert is_fee_waivable(days_overdue=3, is_first_offence=False) is False
    assert is_fee_waivable(days_overdue=20, is_first_offence=True) is False
