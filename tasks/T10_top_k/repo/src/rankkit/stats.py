"""Summary statistics for score lists."""


def _require_values(values):
    if not isinstance(values, (list, tuple)):
        raise TypeError("values must be a list or tuple")
    if not values:
        raise ValueError("values must not be empty")


def mean(values):
    """Return the arithmetic mean of values."""
    _require_values(values)
    return sum(values) / len(values)


def median(values):
    """Return the median of values."""
    _require_values(values)
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def spread(values):
    """Return the difference between the largest and smallest values."""
    _require_values(values)
    return max(values) - min(values)


def rank_of(value, values):
    """Return the one-based rank of value among values."""
    _require_values(values)
    return sum(1 for item in values if item > value) + 1
