"""Weight conversion helpers for logistics."""

from decimal import Decimal, InvalidOperation

KG_PER_GRAM = Decimal("1000")
KG_PER_POUND = Decimal("0.45359237")


def to_decimal(value):
    """Return value as a finite Decimal."""
    if isinstance(value, bool):
        raise TypeError("weight must not be boolean")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as error:
        raise ValueError("weight must be numeric") from error
    if not result.is_finite():
        raise ValueError("weight must be finite")
    return result


def normalize_unit(unit):
    """Return a lower-case unit name after checking it is text."""
    if not isinstance(unit, str):
        raise TypeError("unit must be a string")
    normalized = unit.strip().lower()
    if normalized not in {"g", "kg", "lb"}:
        raise ValueError("unit must be g, kg or lb")
    return normalized


def to_kilograms(value, unit):
    """Return a weight in kilograms."""
    amount = to_decimal(value)
    if amount < 0:
        raise ValueError("weight must be non-negative")
    normalized = normalize_unit(unit)
    if normalized == "kg":
        return amount
    if normalized == "g":
        return amount
    return amount * KG_PER_POUND


def to_grams(value, unit):
    """Return a weight in grams."""
    return to_kilograms(value, unit) * KG_PER_GRAM


def format_weight(value, unit="kg"):
    """Return a weight with three fractional digits."""
    amount = to_kilograms(value, unit)
    return f"{amount:.3f} kg"
