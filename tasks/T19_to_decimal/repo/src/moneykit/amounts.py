"""Conversion helpers for monetary amounts."""

from decimal import Decimal, InvalidOperation


def to_decimal(value):
    """Return value as an exact decimal amount."""
    if isinstance(value, Decimal):
        return value
    if isinstance(value, float):
        return Decimal(value)
    try:
        return Decimal(str(value).strip())
    except (InvalidOperation, AttributeError):
        raise ValueError(f"not an amount: {value}") from None


def is_amount(value):
    """Return True when value can be converted to an amount."""
    try:
        to_decimal(value)
    except (TypeError, ValueError):
        return False
    return True


def same_amount(left, right):
    """Return True when two values denote the same amount."""
    return to_decimal(left) == to_decimal(right)


def zero():
    """Return the zero amount."""
    return Decimal("0")


def one():
    """Return the unit amount."""
    return Decimal("1")
