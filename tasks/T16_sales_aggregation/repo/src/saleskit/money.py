"""Decimal helpers for monetary values."""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

CENT = Decimal("0.01")


def to_amount(value):
    """Convert a numeric value to a finite Decimal with two decimal places."""
    if isinstance(value, bool):
        raise TypeError("amount must be numeric")
    if isinstance(value, Decimal):
        amount = value
    elif isinstance(value, int):
        amount = Decimal(value)
    elif isinstance(value, float):
        amount = Decimal(str(value))
    elif isinstance(value, str):
        text = value.strip()
        if not text:
            raise ValueError("amount must not be empty")
        try:
            amount = Decimal(text)
        except InvalidOperation as exc:
            raise ValueError("amount is not a valid decimal") from exc
    else:
        raise TypeError("amount must be numeric")
    if not amount.is_finite():
        raise ValueError("amount must be finite")
    return amount.quantize(CENT, rounding=ROUND_HALF_UP)


def format_amount(value):
    """Format a monetary value with two decimal places."""
    return f"{to_amount(value):.2f}"


def sum_amounts(values):
    """Return the sum of monetary values, rounded to cents."""
    total = Decimal("0.00")
    for value in values:
        total += to_amount(value)
    return total.quantize(CENT, rounding=ROUND_HALF_UP)
