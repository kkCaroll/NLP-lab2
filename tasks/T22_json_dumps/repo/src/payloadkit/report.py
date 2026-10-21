"""Text descriptions of payloads."""

from .normalise import flatten_mapping
from .serialise import json_dumps


def describe_payload(payload):
    """Return a short description of a payload value."""
    if isinstance(payload, dict):
        return f"object with {len(payload)} keys"
    if isinstance(payload, (list, tuple)):
        return f"array with {len(payload)} items"
    return f"value of type {type(payload).__name__}"


def summarize_keys(payload):
    """Return the sorted top level keys of a mapping."""
    if not isinstance(payload, dict):
        raise TypeError("payload must be a dictionary")
    return ", ".join(sorted(payload))


def format_payload(payload):
    """Return payload as JSON text."""
    return json_dumps(payload)


def describe_flat(payload):
    """Return a dotted key summary of a nested mapping."""
    return ", ".join(f"{key}={value}" for key, value in flatten_mapping(payload).items())


def describe_size(payload):
    """Return the number of top level entries."""
    if isinstance(payload, (dict, list, tuple)):
        return len(payload)
    return 1
