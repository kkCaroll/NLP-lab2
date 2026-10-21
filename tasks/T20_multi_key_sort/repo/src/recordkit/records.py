"""Validation and normalization for employee records."""

from __future__ import annotations

import re

REQUIRED_FIELDS = ("id", "name", "age", "department")
AGE_PATTERN = re.compile(r"^\d+$")
SPACE_PATTERN = re.compile(r"\s+")


def require_fields(record):
    """Check that a record is a mapping with every required field."""
    if not isinstance(record, dict):
        raise TypeError("record must be a dict")
    missing = [field for field in REQUIRED_FIELDS if field not in record]
    if missing:
        raise KeyError("missing fields: " + ", ".join(missing))


def parse_age(value):
    """Return an age as a non-negative integer."""
    if isinstance(value, bool):
        raise TypeError("age must not be boolean")
    if isinstance(value, int):
        age = value
    elif isinstance(value, str) and AGE_PATTERN.match(value.strip()):
        age = int(value.strip())
    else:
        raise ValueError("age must be a non-negative integer")
    if age < 0:
        raise ValueError("age must be non-negative")
    return age


def normalize_name(value):
    """Return a name with normalized internal spacing."""
    if not isinstance(value, str):
        raise TypeError("name must be a string")
    normalized = SPACE_PATTERN.sub(" ", value.strip())
    if not normalized:
        raise ValueError("name must not be empty")
    return normalized


def normalize_text(value, field):
    """Return trimmed text for a named field."""
    if not isinstance(value, str):
        raise TypeError(f"{field} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field} must not be empty")
    return normalized


def normalize_record(record):
    """Return a validated copy of one record."""
    require_fields(record)
    return {
        "id": normalize_text(record["id"], "id"),
        "name": normalize_name(record["name"]),
        "age": parse_age(record["age"]),
        "department": normalize_text(record["department"], "department"),
    }


def normalize_records(records):
    """Return a list of validated record copies."""
    if isinstance(records, dict) or not isinstance(records, (list, tuple)):
        raise TypeError("records must be a list or tuple")
    return [normalize_record(record) for record in records]
