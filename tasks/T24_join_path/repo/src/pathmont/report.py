"""Text rendering for paths."""

from .normalize import clean_path, is_absolute_style
from .roots import relative_to_root


def describe_path(path):
    """Return a cleaned path and its absolute or relative kind."""
    kind = "absolute" if is_absolute_style(path) else "relative"
    return f"{clean_path(path)} ({kind})"


def format_tree(paths, indent="  "):
    """Return one indented line per path in sorted order."""
    if not isinstance(paths, (list, tuple)):
        raise TypeError("paths must be a list or tuple")
    if not isinstance(indent, str):
        raise TypeError("indent must be a string")
    return "\n".join(indent + clean_path(path) for path in sorted(paths))


def format_relative(root, paths):
    """Return paths rendered relative to root."""
    if not isinstance(paths, (list, tuple)):
        raise TypeError("paths must be a list or tuple")
    return "\n".join(relative_to_root(root, path) for path in paths)


def format_ext(path):
    """Return the extension of path or a dash when absent."""
    from .extensions import extension

    return extension(path) or "-"


def format_count(paths):
    """Return the number of paths in text."""
    if not isinstance(paths, (list, tuple)):
        raise TypeError("paths must be a list or tuple")
    return f"paths={len(paths)}"
