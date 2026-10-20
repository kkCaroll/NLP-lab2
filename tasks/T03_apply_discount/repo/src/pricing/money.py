"""Decimal money helpers."""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

CENT = Decimal("0.01")


def to_decimal(value):
    """Return value as a Decimal, rejecting booleans and invalid text."""
    if isinstance(value, bool):
        raise TypeError("money values must not be boolean")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as error:
        raise ValueError("money value must be numeric") from error
    if not result.is_finite():
        raise ValueError("money value must be finite")
    return result


def round_money(value):
    """Return a Decimal quantized to cents."""
    return to_decimal(value).quantize(CENT, rounding=ROUND_HALF_UP)


def add_money(left, right):
    """Return the sum of two money values quantized to cents."""
    return round_money(to_decimal(left) + to_decimal(right))


def subtract_money(left, right):
    """Return the difference of two money values quantized to cents."""
    return round_money(to_decimal(left) - to_decimal(right))


def format_money(value):
    """Return a plain decimal string with two fractional digits."""
    return f"{round_money(value):.2f}"
