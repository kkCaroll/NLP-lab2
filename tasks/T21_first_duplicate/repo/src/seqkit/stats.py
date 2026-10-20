"""Counts and rankings for duplicate values."""

from collections import Counter

from .validate import prepare


def duplicate_counts(values):
    """Return counts for values that occur more than once."""
    counts = Counter(prepare(values))
    return {
        value: count
        for value, count in counts.items()
        if count > 1
    }


def most_common_duplicate(values):
    """Return the most frequent duplicate, breaking ties by text order."""
    counts = duplicate_counts(values)
    if not counts:
        return None
    return max(counts.items(), key=lambda item: (item[1], str(item[0])))[0]


def duplicate_ratio(values):
    """Return the share of positions occupied by duplicated values."""
    prepared = prepare(values)
    if not prepared:
        return 0.0
    repeated = sum(duplicate_counts(prepared).values())
    return repeated / len(prepared)
