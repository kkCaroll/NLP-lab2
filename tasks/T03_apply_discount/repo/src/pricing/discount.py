"""Discount calculation for percentage reductions."""

from decimal import Decimal

from .money import subtract_money, to_decimal


def validate_percent(percent):
    """Return a Decimal percentage between 0 and 100."""
    value = to_decimal(percent)
    if value < 0 or value > 100:
        raise ValueError("percent must be between 0 and 100")
    return value


def apply_discount(amount, percent):
    """Return amount after subtracting the given percentage."""
    value = to_decimal(amount)
    if value < 0:
        raise ValueError("amount must be non-negative")
    rate = validate_percent(percent)
    discount = value * rate / Decimal("100") / Decimal("100")
    return subtract_money(value, discount)
