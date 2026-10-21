"""Path text normalisation using forward slashes."""

import posixpath


def require_path(path, name="path"):
    """Return path after checking that it is text."""
    if not isinstance(path, str):
        raise TypeError(f"{name} must be a string")
    return path


def as_posix(path):
    """Return path with forward slashes."""
    return require_path(path).replace("\\", "/")


def clean_path(path):
    """Return path with redundant separators removed."""
    text = as_posix(path)
    if text == "":
        return "."
    return posixpath.normpath(text)


def is_absolute_style(path):
    """Return True when path starts at the root."""
    return as_posix(path).startswith("/")


def split_parts(path):
    """Return the non-empty segments of path."""
    return [
        part
        for part in clean_path(path).split("/")
        if part and part != "."
    ]


def is_clean(path):
    """Return True when path is already normalised."""
    return clean_path(path) == as_posix(path)
