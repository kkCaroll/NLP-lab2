"""Text rendering for lists and records."""


def format_items(items, separator=", "):
    """Render items as one line separated by the given text."""
    if not isinstance(separator, str):
        raise TypeError("separator must be a string")
    return separator.join(str(item) for item in items)


def format_records(records, fields):
    """Render records as one line per record, following the field order."""
    if not isinstance(fields, (list, tuple)):
        raise TypeError("fields must be a list or tuple")
    lines = []
    for record in records:
        values = [str(record.get(field, "")) for field in fields]
        lines.append(" | ".join(values))
    return "\n".join(lines)


def format_sorted(items, separator=", "):
    """Render items in ascending order as one line."""
    return format_items(sorted(items), separator=separator)
