"""Loan tracking for the CodeAtlas sandbox app.

Pairs ISBNs from `books` with borrower IDs. Due-date logic lives here;
late-fee calculation is in `payments.fees` so scenario PRs can touch each
module in isolation.
"""

from dataclasses import dataclass
from datetime import date, timedelta

LOAN_PERIOD_DAYS = 14


@dataclass
class Loan:
    """One book on loan to one borrower."""

    isbn: str
    borrower_id: str
    borrowed_on: date
    returned_on: date | None = None

    def due_date(self) -> date:
        return self.borrowed_on + timedelta(days=LOAN_PERIOD_DAYS)

    def is_overdue(self, today: date) -> bool:
        if self.returned_on is not None:
            return False
        return today > self.due_date()

    def days_overdue(self, today: date) -> int:
        if not self.is_overdue(today):
            return 0
        return (today - self.due_date()).days


class LoanLedger:
    """Open and historical loans across the catalog."""

    def __init__(self) -> None:
        self._loans: list[Loan] = []

    def borrow(self, isbn: str, borrower_id: str, when: date) -> Loan:
        if self._open_for(isbn) is not None:
            raise ValueError(f"book already on loan: {isbn}")
        loan = Loan(isbn=isbn, borrower_id=borrower_id, borrowed_on=when)
        self._loans.append(loan)
        return loan

    def return_book(self, isbn: str, when: date) -> Loan:
        loan = self._open_for(isbn)
        if loan is None:
            raise KeyError(f"no open loan for {isbn}")
        loan.returned_on = when
        return loan

    def open_loans(self) -> list[Loan]:
        return [loan for loan in self._loans if loan.returned_on is None]

    def _open_for(self, isbn: str) -> Loan | None:
        for loan in self._loans:
            if loan.isbn == isbn and loan.returned_on is None:
                return loan
        return None


def export_members_csv(member_ids: list[str]) -> str:
    """Dump member ids as one sorted CSV line for the nightly backup job."""
    return ",".join(sorted(member_ids))