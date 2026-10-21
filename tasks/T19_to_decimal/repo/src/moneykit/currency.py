"""Currency labels and simple amount arithmetic."""

from decimal import Decimal

from .amounts import to_decimal

SUPPORTED = ("CNY", "EUR", "USD")


def check_currency(code):
    """Return a supported currency code or raise."""
    if not isinstance(code, str):
        raise TypeError("code must be a string")
    code = code.strip().upper()
    if code not in SUPPORTED:
        raise ValueError(f"unsupported currency: {code}")
    return code


def add_amounts(left, right):
    """Return the sum of two amounts without rounding."""
    return to_decimal(left) + to_decimal(right)


def subtract_amounts(left, right):
    """Return the difference of two amounts without rounding."""
    return to_decimal(left) - to_decimal(right)


def negate(value):
    """Return the opposite amount."""
    return -to_decimal(value)


def currency_label(code):
    """Return a short label for a currency code."""
    labels = {"CNY": "yuan", "EUR": "euro", "USD": "dollar"}
    return labels[check_currency(code)]


def is_zero(value):
    """Return True when value is exactly zero."""
    return to_decimal(value) == Decimal("0")
