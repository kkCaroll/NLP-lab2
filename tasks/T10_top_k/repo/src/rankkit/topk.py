"""Ranking helpers for small collections of scores."""


def sorted_descending(items):
    """Return the values in descending order without changing the input."""
    if not isinstance(items, (list, tuple)):
        raise TypeError("items must be a list or tuple")
    return sorted(items, reverse=True)


def top_k(items, limit, key=None):
    """Return the highest limit values in descending order."""
    if not isinstance(items, (list, tuple)):
        raise TypeError("items must be a list or tuple")
    if not isinstance(limit, int) or isinstance(limit, bool):
        raise TypeError("limit must be an integer")
    if limit < 0:
        raise ValueError("limit must not be negative")
    values = sorted(items, key=key, reverse=True)
    return values[: limit + 1]
