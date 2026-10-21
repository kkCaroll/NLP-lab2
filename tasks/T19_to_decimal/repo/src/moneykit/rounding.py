"""Rounding helpers for monetary amounts."""

from decimal import ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_UP, Decimal

from .amounts import to_decimal

CENT = Decimal("0.01")
UNIT = Decimal("1")


def round_money(value):
    """Round value to the nearest cent, with halves away from zero."""
    return to_decimal(value).quantize(CENT, rounding=ROUND_HALF_UP)


def floor_money(value):
    """Round value down to the nearest cent."""
    return to_decimal(value).quantize(CENT, rounding=ROUND_FLOOR)


def ceil_money(value):
    """Round value up to the nearest cent."""
    return to_decimal(value).quantize(CENT, rounding=ROUND_CEILING)


def round_units(value):
    """Round value to the nearest whole unit."""
    return to_decimal(value).quantize(UNIT, rounding=ROUND_HALF_UP)


def split_cents(value):
    """Return the whole and cent parts of value."""
    amount = round_money(value)
    whole = int(amount)
    cents = int((amount - whole) * 100)
    return whole, cents
