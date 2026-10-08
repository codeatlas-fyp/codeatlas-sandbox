"""Late-fee calculation for overdue loans.

The sandbox PRs modify functions here; the Jira ticket SBX-4 (late fee) is the
"honest implementation" demo. SBX-9 (unexplained change) adds `format_receipt`
without a matching ticket.
"""

from decimal import Decimal

DAILY_LATE_FEE = Decimal("0.25")
MAX_LATE_FEE = Decimal("10.00")


def calculate_late_fee(days_overdue: int) -> Decimal:
    """Return the late fee for `days_overdue` days, capped at MAX_LATE_FEE.

    Fees are a flat per-day rate; the cap is enforced to avoid runaway charges
    on long-forgotten loans.
    """
    if days_overdue <= 0:
        return Decimal("0.00")
    fee = Decimal(days_overdue) * DAILY_LATE_FEE
    return min(fee, MAX_LATE_FEE)


def is_fee_waivable(days_overdue: int, is_first_offence: bool) -> bool:
    """Fees under one week are waivable for first-time offenders."""
    return is_first_offence and days_overdue <= 7
