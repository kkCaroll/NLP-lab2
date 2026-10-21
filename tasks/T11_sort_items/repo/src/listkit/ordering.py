"""Ordering helpers for lists of comparable values."""


def sort_items(items, reverse=False):
    """Return a sorted copy of items."""
    if not isinstance(items, (list, tuple)):
        raise TypeError("items must be a list or tuple")
    return items.sort(reverse=reverse)


def sort_by_key(records, key, reverse=False):
    """Return records sorted by a named field."""
    if not isinstance(records, (list, tuple)):
        raise TypeError("records must be a list or tuple")
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    for record in records:
        if not isinstance(record, dict) or key not in record:
            raise KeyError(f"record without {key}")
    return sorted(records, key=lambda record: record[key], reverse=reverse)


def deduplicate(items):
    """Return items without repeated values, keeping the first occurrence."""
    if not isinstance(items, (list, tuple)):
        raise TypeError("items must be a list or tuple")
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
