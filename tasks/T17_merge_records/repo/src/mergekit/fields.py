"""Field helpers for record completion."""

DEFAULT_VERSION = 1
DEFAULT_SOURCE = "unknown"


def require_record(record, name="record"):
    """Return record after checking that it is a mapping."""
    if not isinstance(record, dict):
        raise TypeError(f"{name} must be a dictionary")
    return record


def fill_missing(record):
    """Return a copy of record with default fields applied."""
    require_record(record)
    filled = dict(record)
    filled.setdefault("version", DEFAULT_VERSION)
    filled.setdefault("source", DEFAULT_SOURCE)
    return filled


def complete_record(record, defaults):
    """Return record completed from a defaults mapping."""
    require_record(record)
    require_record(defaults, "defaults")
    completed = dict(defaults)
    completed.update(record)
    return fill_missing(completed)


def field_names(records):
    """Return every field name that appears across records."""
    if not isinstance(records, (list, tuple)):
        raise TypeError("records must be a list or tuple")
    names = set()
    for record in records:
        names.update(require_record(record).keys())
    return sorted(names)


def shared_fields(records):
    """Return field names present in every record."""
    if not isinstance(records, (list, tuple)) or not records:
        return []
    common = set(require_record(records[0]).keys())
    for record in records[1:]:
        common &= set(require_record(record).keys())
    return sorted(common)
