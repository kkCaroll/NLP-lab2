"""Position and gap analysis for repeated values."""

from .validate import prepare


def first_repeat_gap(values):
    """Return the shortest distance between two equal values, or None."""
    prepared = prepare(values)
    seen = {}
    gaps = []
    for index, value in enumerate(prepared):
        if value in seen:
            gaps.append(index - seen[value])
        seen[value] = index
    return min(gaps) if gaps else None


def repeat_gaps(values):
    """Return the gaps between successive occurrences of each value."""
    prepared = prepare(values)
    seen = {}
    gaps = {}
    for index, value in enumerate(prepared):
        if value in seen:
            gaps.setdefault(value, []).append(index - seen[value])
        seen[value] = index
    return gaps


def longest_repeated_run(values):
    """Return the length of the longest run of equal adjacent values."""
    prepared = prepare(values)
    if not prepared:
        return 0
    best = 1
    current = 1
    for previous, value in zip(prepared, prepared[1:]):
        if value == previous:
            current += 1
            best = max(best, current)
        else:
            current = 1
    return best
