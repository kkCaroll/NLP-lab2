"""Tolerant conversion from text and objects to numbers."""

DEFAULT_INT = 0
DEFAULT_FLOAT = 0.0


def safe_int(value, default=DEFAULT_INT):
    """Return value as an integer, falling back to default."""
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return default
        try:
            return int(text, 10)
        except ValueError:
            return default
    try:
        return int(value)
    except ValueError:
        return default


def safe_float(value, default=DEFAULT_FLOAT):
    """Return value as a float, falling back to default."""
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return default
        try:
            return float(text)
        except ValueError:
            return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def convert_all(values, default=DEFAULT_INT):
    """Convert every entry of values to an integer."""
    if not isinstance(values, (list, tuple)):
        raise TypeError("values must be a list or tuple")
    return [safe_int(value, default) for value in values]
