"""JSON serialisation helpers."""

import json


class PayloadError(ValueError):
    """Raised when a payload cannot be converted to or from JSON."""


def json_dumps(payload):
    """Return payload as compact JSON text."""
    try:
        return json.dumps(
            payload,
            ensure_ascii=True,
            sort_keys=False,
            separators=(",", ": "),
        )
    except (TypeError, ValueError) as error:
        raise PayloadError(str(error)) from None


def json_loads(text):
    """Return the value encoded in JSON text."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    try:
        return json.loads(text)
    except json.JSONDecodeError as error:
        raise PayloadError(str(error)) from None


def json_bytes(payload):
    """Return payload encoded as UTF-8 JSON bytes."""
    return json_dumps(payload).encode("utf-8")


def is_json_text(text):
    """Return True when text parses as JSON."""
    try:
        json_loads(text)
    except (PayloadError, TypeError):
        return False
    return True
