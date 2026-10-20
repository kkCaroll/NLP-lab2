"""Merging and expansion helpers for integer ranges."""

from .parse import validate_range


def merge_ranges(ranges):
    """Return sorted disjoint ranges after merging overlaps and adjacency."""
    prepared = []
    for start, end in ranges:
        prepared.append(validate_range(start, end))
    prepared.sort()
    if not prepared:
        return []
    merged = [list(prepared[0])]
    for start, end in prepared[1:]:
        last = merged[-1]
        if start <= last[1] + 1:
            last[1] = max(last[1], end)
        else:
            merged.append([start, end])
    return [(start, end) for start, end in merged]


def expand_ranges(ranges):
    """Return every integer covered by the given inclusive ranges."""
    result = []
    for start, end in ranges:
        checked_start, checked_end = validate_range(start, end)
        result.extend(range(checked_start, checked_end + 1))
    return result


def unique_values(values):
    """Return values in first-seen order without duplicates."""
    seen = set()
    result = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result
