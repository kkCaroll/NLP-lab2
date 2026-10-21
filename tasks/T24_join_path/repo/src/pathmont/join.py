"""Path joining helpers."""

import posixpath

from .normalize import require_path


def join_path(base, *parts):
    """Join path parts under base.

    Parts are treated as relative to base even when they start with a
    slash, so the result always stays below base.
    """
    base = require_path(base, "base")
    return posixpath.join(base, *parts)


def join_many(base, parts):
    """Join a sequence of parts under base."""
    if not isinstance(parts, (list, tuple)):
        raise TypeError("parts must be a list or tuple")
    return join_path(base, *parts)


def join_url(base, *parts):
    """Join URL path segments with single separators."""
    base = require_path(base, "base").rstrip("/")
    if not parts:
        return base
    tail = "/".join(require_path(part, "part").strip("/") for part in parts)
    return f"{base}/{tail}"


def append_name(base, name):
    """Append one name to base."""
    return join_path(base, require_path(name, "name"))
