"""Payload normalisation before serialisation."""

from .unicode import json_safe, sort_payload


def normalize_payload(payload):
    """Return payload with tuples turned into lists and keys sorted."""
    return sort_payload(json_safe(payload))


def flatten_mapping(payload, prefix=""):
    """Return a flat mapping with dotted keys."""
    if not isinstance(payload, dict):
        raise TypeError("payload must be a dictionary")
    flat = {}
    for key in sorted(payload):
        value = payload[key]
        name = f"{prefix}{key}"
        if isinstance(value, dict) and value:
            flat.update(flatten_mapping(value, prefix=name + "."))
        else:
            flat[name] = value
    return flat


def merge_payloads(base, extra):
    """Return base updated by extra without changing either input."""
    if not isinstance(base, dict) or not isinstance(extra, dict):
        raise TypeError("payloads must be dictionaries")
    merged = dict(base)
    merged.update(extra)
    return merged


def pick_fields(payload, fields):
    """Return the entries of payload named in fields."""
    if not isinstance(payload, dict):
        raise TypeError("payload must be a dictionary")
    return {
        field: payload[field]
        for field in fields
        if field in payload
    }
