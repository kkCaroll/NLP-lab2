"""Ordering, selection and ranking helpers."""

from __future__ import annotations

from .keys import order_records, record_key
from .records import normalize_records


def sort_records(records):
    """Return records in display order."""
    return order_records(normalize_records(records))


def top_k(records, k):
    """Return the first k records in display order."""
    if isinstance(k, bool) or not isinstance(k, int):
        raise TypeError("k must be an integer")
    if k <= 0:
        return []
    return sort_records(records)[:k]


def rank_records(records):
    """Return records with competition ranks in display order."""
    ordered = sort_records(records)
    ranked = []
    previous = None
    rank = 0
    for index, record in enumerate(ordered, start=1):
        key = record_key(record)
        if key != previous:
            rank = index
            previous = key
        ranked.append({"rank": rank, "record": record})
    return ranked
