"""Envelope construction around JSON payloads."""

from .serialise import json_dumps, json_loads


def build_envelope(payload, ok=True):
    """Return a JSON envelope that wraps payload."""
    if not isinstance(ok, bool):
        raise TypeError("ok must be a boolean")
    return json_dumps({"ok": ok, "data": payload})


def parse_envelope(text):
    """Return the mapping stored in an envelope."""
    document = json_loads(text)
    if not isinstance(document, dict):
        raise ValueError("envelope must be an object")
    if "ok" not in document or "data" not in document:
        raise ValueError("envelope requires ok and data")
    return document


def envelope_ok(text):
    """Return the status flag of an envelope."""
    return parse_envelope(text)["ok"] is True


def wrap_items(items):
    """Return an envelope that wraps a list and its length."""
    if not isinstance(items, (list, tuple)):
        raise TypeError("items must be a list or tuple")
    return build_envelope({"items": list(items), "count": len(items)})


def error_envelope(message):
    """Return an envelope that describes an error."""
    if not isinstance(message, str):
        raise TypeError("message must be a string")
    return build_envelope({"message": message}, ok=False)
