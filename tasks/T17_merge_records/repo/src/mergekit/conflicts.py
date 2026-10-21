"""Conflict detection between record versions."""

from .fields import require_record


def conflicting_fields(current, candidate):
    """Return field names whose values differ between two records."""
    require_record(current, "current")
    require_record(candidate, "candidate")
    names = sorted(set(current) | set(candidate))
    return [name for name in names if current.get(name) != candidate.get(name)]


def describe_conflicts(current, candidate):
    """Render differing fields and their values as text."""
    names = conflicting_fields(current, candidate)
    if not names:
        return "no conflicts"
    parts = []
    for name in names:
        parts.append(f"{name}: {current.get(name)} -> {candidate.get(name)}")
    return ", ".join(parts)


def has_conflict(current, candidate):
    """Return True when two records differ in any field."""
    return bool(conflicting_fields(current, candidate))


def merge_field(current, candidate, name, prefer_candidate=True):
    """Return one field value from either record."""
    require_record(current, "current")
    require_record(candidate, "candidate")
    if prefer_candidate and name in candidate:
        return candidate[name]
    if name in current:
        return current[name]
    return candidate.get(name)
