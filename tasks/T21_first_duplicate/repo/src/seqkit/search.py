"""Search helpers for duplicate values."""

from .validate import prepare


def _first_repeated(values):
    """Return the repeated value whose first occurrence is earliest."""
    seen = set()
    result = None
    for value in values:
        if value in seen:
            result = value
        seen.add(value)
    return result


def find_first_duplicate(values):
    """Return the first duplicate in positional order, or None."""
    return _first_repeated(prepare(values))


def has_duplicate(values):
    """Return True when the sequence contains any repeated value."""
    return _first_repeated(prepare(values)) is not None


def first_duplicate_index(values):
    """Return the first index of the first duplicate value, or None."""
    prepared = prepare(values)
    duplicate = _first_repeated(prepared)
    if duplicate is None:
        return None
    return prepared.index(duplicate)


def duplicate_positions(values):
    """Return a mapping from duplicated value to all its indexes."""
    prepared = prepare(values)
    positions = {}
    for index, value in enumerate(prepared):
        positions.setdefault(value, []).append(index)
    return {
        value: indexes
        for value, indexes in positions.items()
        if len(indexes) > 1
    }


def find_first_in_sorted(values, target):
    """Return the first index of target in a sorted sequence, or -1."""
    prepared = prepare(values)
    low = 0
    high = len(prepared)
    while low < high:
        middle = (low + high) // 2
        if target == prepared[middle] and (
            middle == 0 or target != prepared[middle - 1]
        ):
            return middle
        if target <= prepared[middle]:
            high = middle
        else:
            low = middle + 1
    return -1
