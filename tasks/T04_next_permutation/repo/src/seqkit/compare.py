"""Comparison helpers for sequences of comparable values."""


def is_sorted(items):
    """Return True when items are in non-decreasing order."""
    return all(items[index] <= items[index + 1] for index in range(len(items) - 1))


def compare_sequences(left, right):
    """Return -1, 0 or 1 according to lexicographic order."""
    for first, second in zip(left, right):
        if first < second:
            return -1
        if first > second:
            return 1
    if len(left) < len(right):
        return -1
    if len(left) > len(right):
        return 1
    return 0


def count_inversions(items):
    """Return the number of pairs whose order is descending."""
    total = 0
    for first in range(len(items)):
        for second in range(first + 1, len(items)):
            if items[first] > items[second]:
                total += 1
    return total
