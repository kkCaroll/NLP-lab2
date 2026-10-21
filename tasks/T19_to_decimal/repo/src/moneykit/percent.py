"""Percentage helpers for monetary amounts."""

from decimal import Decimal

from .rounding import round_money


def percent_of(value, percent):
    """Return percent of value, rounded to cents."""
    share = Decimal(str(percent)) / Decimal("100")
    return round_money(Decimal(str(value)) * share)


def as_percent(part, whole):
    """Return part as a percentage of whole."""
    part = Decimal(str(part))
    whole = Decimal(str(whole))
    if whole == 0:
        raise ValueError("whole must not be zero")
    return (part / whole * 100).quantize(Decimal("0.01"))


def discount_amount(value, percent):
    """Return the amount removed by a percentage discount."""
    return percent_of(value, percent)


def add_tax(value, percent):
    """Return value with a percentage tax added."""
    return round_money(Decimal(str(value)) + percent_of(value, percent))
