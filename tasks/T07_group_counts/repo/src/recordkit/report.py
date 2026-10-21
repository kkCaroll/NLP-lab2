"""Text rendering helpers for record counts and tables."""


def format_counts(counts):
    """Return counts as a comma-separated text line."""
    ordered = sorted(counts.items(), key=lambda item: str(item[0]))
    return ", ".join(f"{key}: {value}" for key, value in ordered)


def format_table(records, columns):
    """Return records as a simple pipe-separated table."""
    if not isinstance(columns, (list, tuple)) or not columns:
        raise ValueError("columns must be a non-empty list or tuple")
    lines = ["|".join(columns)]
    for record in records:
        lines.append("|".join(str(record.get(column, "")) for column in columns))
    return "\n".join(lines)


def format_records(records):
    """Return one sorted key=value line per record."""
    lines = []
    for record in records:
        pairs = sorted(record.items(), key=lambda item: str(item[0]))
        lines.append(", ".join(f"{key}={value}" for key, value in pairs))
    return lines
