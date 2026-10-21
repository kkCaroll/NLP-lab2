"""Grouping helpers for parsed records."""


def _normalise(value):
    """Return a grouping key with surrounding space and case removed."""
    if isinstance(value, str):
        return value.strip()
    return value


def group_counts(records, key):
    """Return counts per distinct value of key, ignoring case and edge space."""
    if not isinstance(records, (list, tuple)):
        raise TypeError("records must be a list or tuple")
    counts = {}
    for record in records:
        if not isinstance(record, dict):
            raise TypeError("each record must be a dictionary")
        value = _normalise(record.get(key, ""))
        counts[value] = counts.get(value, 0) + 1
    return counts


def top_values(counts, limit):
    """Return the most frequent values as pairs, breaking ties by value."""
    if not isinstance(limit, int) or isinstance(limit, bool):
        raise TypeError("limit must be an integer")
    if limit < 0:
        raise ValueError("limit must not be negative")
    ordered = sorted(counts.items(), key=lambda item: (-item[1], str(item[0])))
    return ordered[:limit]
