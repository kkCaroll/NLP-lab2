"""Helpers for simple comma-separated records."""


def split_fields(line):
    """Return stripped fields from one comma-separated line."""
    if not isinstance(line, str):
        raise TypeError("line must be a string")
    return [field.strip() for field in line.split(",")]


def parse_header(text):
    """Return the header fields from the first non-empty line."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    for line in text.splitlines():
        if line.strip():
            return split_fields(line)
    return []


def parse_rows(text):
    """Return records parsed from a header line and data lines."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        return []
    headers = split_fields(lines[0])
    records = []
    for line in lines[1:]:
        fields = split_fields(line)
        record = dict.fromkeys(headers, "")
        record.update(zip(headers, fields))
        records.append(record)
    return records
