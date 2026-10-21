"""Text and payload helpers for non-ASCII content."""

SUPPORTED = (str, int, float, bool, type(None))


def ensure_text(value):
    """Return value as text, decoding UTF-8 bytes."""
    if isinstance(value, bytes):
        return value.decode("utf-8")
    if not isinstance(value, str):
        raise TypeError("value must be text or bytes")
    return value


def has_non_ascii(text):
    """Return True when text contains a character outside ASCII."""
    return any(ord(char) > 127 for char in ensure_text(text))


def sort_payload(payload):
    """Return payload with mapping keys sorted recursively."""
    if isinstance(payload, dict):
        return {key: sort_payload(payload[key]) for key in sorted(payload)}
    if isinstance(payload, list):
        return [sort_payload(item) for item in payload]
    return payload


def json_safe(payload):
    """Return payload with unsupported values converted to text."""
    if isinstance(payload, dict):
        return {
            ensure_text(key): json_safe(value)
            for key, value in payload.items()
        }
    if isinstance(payload, (list, tuple)):
        return [json_safe(item) for item in payload]
    if isinstance(payload, SUPPORTED):
        return payload
    return str(payload)


def count_non_ascii(text):
    """Return the number of non-ASCII characters in text."""
    return sum(1 for char in ensure_text(text) if ord(char) > 127)
