"""Parsing and validation helpers for inclusive integer ranges."""


def validate_value(value):
    """Return value after checking it is an integer but not a boolean."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("range values must be integers")
    return value


def validate_range(start, end):
    """Return a checked pair of inclusive range endpoints."""
    validate_value(start)
    validate_value(end)
    if start > end:
        raise ValueError("range start must not exceed end")
    return start, end


def parse_range(text):
    """Return every integer in an inclusive range such as 1-5."""
    if not isinstance(text, str):
        raise TypeError("range text must be a string")
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("range text must not be empty")
    if "-" not in cleaned:
        return [validate_value(int(cleaned))]
    start_text, end_text = cleaned.split("-", 1)
    start = int(start_text)
    end = int(end_text)
    validate_range(start, end)
    return list(range(start, end))


def parse_many(items):
    """Return the concatenation of several parsed range strings."""
    if isinstance(items, (str, bytes)) or not isinstance(items, (list, tuple)):
        raise TypeError("items must be a list or tuple")
    result = []
    for item in items:
        result.extend(parse_range(item))
    return result
