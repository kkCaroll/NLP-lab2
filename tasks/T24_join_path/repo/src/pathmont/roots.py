"""Helpers that keep paths inside a root directory."""

from .join import join_path
from .normalize import clean_path, require_path


def resolve_under(root, *parts):
    """Return a cleaned path inside root for the given parts."""
    return clean_path(join_path(root, *parts))


def is_within(root, path):
    """Return True when path lies at or below root."""
    root = clean_path(require_path(root, "root"))
    candidate = clean_path(require_path(path))
    if candidate == root:
        return True
    return candidate.startswith(root.rstrip("/") + "/")


def relative_to_root(root, path):
    """Return path relative to root or raise when it lies outside."""
    root = clean_path(require_path(root, "root")).rstrip("/")
    candidate = clean_path(require_path(path))
    if not is_within(root, candidate):
        raise ValueError("path is outside root")
    if candidate == root:
        return "."
    return candidate[len(root) + 1:]


def common_root(paths):
    """Return the longest common directory of paths."""
    if not isinstance(paths, (list, tuple)) or not paths:
        raise ValueError("paths must be a non-empty list or tuple")
    split = [clean_path(path).split("/") for path in paths]
    common = []
    for parts in zip(*split):
        if len(set(parts)) != 1:
            break
        common.append(parts[0])
    return "/".join(common) or "."
