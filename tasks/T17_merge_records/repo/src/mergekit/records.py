"""Record merging by identifier."""

from .fields import fill_missing, require_record


def record_key(record):
    """Return the identifier of a record."""
    require_record(record)
    if "id" not in record:
        raise KeyError("record without id")
    key = record["id"]
    if not isinstance(key, (str, int)) or isinstance(key, bool):
        raise TypeError("id must be a string or an integer")
    return key


def pick_latest(current, candidate):
    """Return the record with the higher version."""
    require_record(current)
    require_record(candidate)
    current_version = current.get("version", 0)
    candidate_version = candidate.get("version", 0)
    if candidate_version > current_version:
        return candidate
    return current


def group_by_id(records):
    """Group records by identifier, preserving input order."""
    if not isinstance(records, (list, tuple)):
        raise TypeError("records must be a list or tuple")
    groups = {}
    for record in records:
        groups.setdefault(record_key(record), []).append(record)
    return groups


def merge_records(records):
    """Merge records by identifier, keeping the latest version.

    The merged list follows the order in which identifiers first appear.
    """
    if not isinstance(records, (list, tuple)):
        raise TypeError("records must be a list or tuple")
    merged = {}
    for record in records:
        key = record_key(record)
        candidate = fill_missing(record)
        if key not in merged:
            merged[key] = candidate
    return list(merged.values())


def latest_versions(records):
    """Return a mapping from identifier to the highest version number."""
    if not isinstance(records, (list, tuple)):
        raise TypeError("records must be a list or tuple")
    versions = {}
    for record in records:
        key = record_key(record)
        version = record.get("version", 0)
        if key not in versions or version > versions[key]:
            versions[key] = version
    return versions
