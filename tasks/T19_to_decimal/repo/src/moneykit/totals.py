"""Totals and rate calculations for amounts."""

from decimal import Decimal

from .amounts import to_decimal, zero
from .rounding import round_money


def sum_amounts(values):
    """Return the rounded sum of amounts."""
    if not isinstance(values, (list, tuple)):
        raise TypeError("values must be a list or tuple")
    total = zero()
    for value in values:
        total += round_money(value)
    return round_money(total)


def subtotal(values, discount=zero()):
    """Return the total after subtracting a discount."""
    return round_money(sum_amounts(values) - to_decimal(discount))


def apply_rate(value, rate):
    """Return value multiplied by rate and rounded to cents."""
    return round_money(Decimal(str(value)) * Decimal(str(rate)))


def average_amount(values):
    """Return the rounded mean of amounts."""
    if not isinstance(values, (list, tuple)):
        raise TypeError("values must be a list or tuple")
    if not values:
        raise ValueError("values must not be empty")
    return round_money(sum_amounts(values) / len(values))


def largest_amount(values):
    """Return the largest amount after conversion."""
    if not isinstance(values, (list, tuple)):
        raise TypeError("values must be a list or tuple")
    if not values:
        raise ValueError("values must not be empty")
    return max(round_money(value) for value in values)
