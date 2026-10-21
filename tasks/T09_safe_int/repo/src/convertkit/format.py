"""Formatting helpers for converted numbers."""

from .parse import safe_float


def format_number(value, digits=2):
    """Render value with a fixed number of decimal places."""
    if not isinstance(digits, int) or isinstance(digits, bool):
        raise TypeError("digits must be an integer")
    if digits < 0:
        raise ValueError("digits must not be negative")
    return f"{safe_float(value):.{digits}f}"


def format_percent(value, digits=1):
    """Render a ratio as a percentage."""
    return f"{safe_float(value) * 100:.{digits}f}%"


def format_record(record):
    """Render a mapping of names to numeric values as one line."""
    if not isinstance(record, dict):
        raise TypeError("record must be a dictionary")
    parts = [f"{key}={format_number(value)}" for key, value in record.items()]
    return ", ".join(parts)
