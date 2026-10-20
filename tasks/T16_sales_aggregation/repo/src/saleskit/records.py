"""Validation and normalization for sales records."""

from .money import to_amount

VALID_KINDS = {"sale", "refund"}
REQUIRED_FIELDS = ("region", "kind", "amount")


def normalize_record(record):
    """Validate one record and return a normalized copy."""
    if not isinstance(record, dict):
        raise TypeError("record must be a mapping")
    for field in REQUIRED_FIELDS:
        if field not in record:
            raise KeyError(field)
    region = record["region"]
    kind = record["kind"]
    if not isinstance(region, str):
        raise TypeError("region must be a string")
    if not isinstance(kind, str):
        raise TypeError("kind must be a string")
    region = region.strip().lower()
    kind = kind.strip().lower()
    if not region:
        raise ValueError("region must not be empty")
    if kind not in VALID_KINDS:
        raise ValueError(f"unknown record kind: {kind}")
    return {
        "region": region,
        "kind": kind,
        "amount": to_amount(record["amount"]),
    }


def normalize_records(rows):
    """Validate and normalize a sequence of records."""
    if not isinstance(rows, (list, tuple)):
        raise TypeError("rows must be a list or tuple")
    return [normalize_record(row) for row in rows]
