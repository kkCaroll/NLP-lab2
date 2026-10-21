"""Shared ordering rules for employee records."""

from __future__ import annotations

from .records import normalize_name, parse_age


def record_key(record):
    """Return the multi-key ordering tuple for one record."""
    age = parse_age(record["age"])
    name = normalize_name(record["name"])
    return (-age, name)


def order_records(records):
    """Return records ordered by descending age then ascending name."""
    return sorted(records, key=record_key, reverse=True)
