"""Numeric limits shared by the paging helpers."""

MIN_PAGE = 1
MIN_SIZE = 1


def as_int(value, name="value"):
    """Return value as an integer or raise a type error."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    return value


def clamp(value, low, high):
    """Limit value to the closed interval from low to high."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(value, high + 1))


def valid_page_size(size):
    """Return size after checking that it is a positive integer."""
    size = as_int(size, "size")
    if size < MIN_SIZE:
        raise ValueError("size must be positive")
    return size


def positive_or_one(value):
    """Return value when it is positive and one otherwise."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("value must be an integer")
    return value if value > 0 else MIN_PAGE
