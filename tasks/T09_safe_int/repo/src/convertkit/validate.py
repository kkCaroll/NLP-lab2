"""Validation helpers for converted numbers."""

MINIMUM = 0


def is_integer(value):
    """Return True when value denotes an integer without a fractional part."""
    if isinstance(value, bool):
        return False
    if isinstance(value, int):
        return True
    if isinstance(value, float):
        return value.is_integer()
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return False
        try:
            int(text, 10)
        except ValueError:
            return False
        return True
    return False


def require_int(value, name="value"):
    """Return value as an integer or raise when it is not integral."""
    if not is_integer(value):
        raise ValueError(f"{name} must be an integer")
    return int(value)


def clamp(value, low, high):
    """Limit value to the closed interval from low to high."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def positive_or(value, fallback=MINIMUM):
    """Return value when it is positive, otherwise the fallback."""
    number = require_int(value)
    if number > 0:
        return number
    return fallback
