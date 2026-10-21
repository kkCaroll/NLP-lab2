"""File extension helpers for path text."""

import posixpath

from .normalize import clean_path, require_path


def split_ext(path):
    """Return the base and extension of path."""
    return posixpath.splitext(clean_path(path))


def base_name(path):
    """Return the final segment of path."""
    return posixpath.basename(clean_path(path))


def stem(path):
    """Return the file name without its extension."""
    return split_ext(path)[0]


def extension(path):
    """Return the extension of path including the dot."""
    return split_ext(path)[1]


def with_suffix(path, suffix):
    """Return path with its extension replaced by suffix."""
    if not isinstance(suffix, str):
        raise TypeError("suffix must be a string")
    if suffix and not suffix.startswith("."):
        raise ValueError("suffix must start with a dot")
    base, _ = split_ext(path)
    return base + suffix


def has_extension(path, suffix):
    """Return True when path ends with the given extension."""
    if not isinstance(suffix, str) or not suffix.startswith("."):
        raise ValueError("suffix must start with a dot")
    return extension(path).lower() == suffix.lower()


def require_path_text(path):
    """Return path after checking that it is text."""
    return require_path(path)
