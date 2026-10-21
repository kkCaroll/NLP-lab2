"""Text rendering for merged records."""

from .fields import field_names
from .records import merge_records


def format_records(records, fields):
    """Render records as one pipe separated line per record."""
    if not isinstance(fields, (list, tuple)):
        raise TypeError("fields must be a list or tuple")
    lines = []
    for record in records:
        values = [str(record.get(field, "")) for field in fields]
        lines.append(" | ".join(values))
    return "\n".join(lines)


def summarize_versions(records):
    """Render identifier and version pairs after merging."""
    merged = merge_records(records)
    return ", ".join(
        f"{record['id']}={record.get('version', 0)}" for record in merged
    )


def summarize_fields(records):
    """Render the field names that appear across records."""
    return ", ".join(field_names(records))


def format_merge(records):
    """Render the merged records as identifier and name pairs."""
    merged = merge_records(records)
    return ", ".join(
        f"{record['id']}:{record.get('name', '')}" for record in merged
    )
