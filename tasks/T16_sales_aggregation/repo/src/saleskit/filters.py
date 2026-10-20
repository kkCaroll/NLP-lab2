"""Filtering and ordering helpers for normalized sales records."""

from .records import normalize_records


def sales_only(rows):
    """Return normalized sale records."""
    return [record for record in normalize_records(rows) if record["kind"] == "sale"]


def refunds_only(rows):
    """Return normalized refund records."""
    return [record for record in normalize_records(rows) if record["kind"] == "refund"]


def filter_region(rows, region):
    """Return normalized records for one region."""
    if not isinstance(region, str):
        raise TypeError("region must be a string")
    target = region.strip().lower()
    return [record for record in normalize_records(rows) if record["region"] == target]


def sort_records(rows):
    """Return normalized records ordered by region, kind and amount."""
    return sorted(
        normalize_records(rows),
        key=lambda record: (record["region"], record["kind"], record["amount"]),
    )
