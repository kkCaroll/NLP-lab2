"""Ordering helpers for merged records."""

from .fields import require_record


def stable_order(records):
    """Return records ordered by identifier while keeping ties stable."""
    if not isinstance(records, (list, tuple)):
        raise TypeError("records must be a list or tuple")
    return sorted(records, key=lambda record: str(record.get("id", "")))


def sort_by_version(records, descending=True):
    """Return records ordered by version."""
    if not isinstance(records, (list, tuple)):
        raise TypeError("records must be a list or tuple")
    for record in records:
        require_record(record)
    return sorted(
        records,
        key=lambda record: record.get("version", 0),
        reverse=descending,
    )


def unique_ids(records):
    """Return identifiers in first appearance order."""
    if not isinstance(records, (list, tuple)):
        raise TypeError("records must be a list or tuple")
    seen = set()
    result = []
    for record in records:
        key = require_record(record).get("id")
        if key not in seen:
            seen.add(key)
            result.append(key)
    return result


def reorder(records, order):
    """Return records in the order given by a list of identifiers."""
    if not isinstance(order, (list, tuple)):
        raise TypeError("order must be a list or tuple")
    by_id = {}
    for record in records:
        by_id[require_record(record).get("id")] = record
    return [by_id[key] for key in order if key in by_id]
