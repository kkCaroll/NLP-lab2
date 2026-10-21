"""Text rendering for slugs and titles."""

from .slug import slugify, unique_slug
from .title import normalize_title


def format_index(entries):
    """Render name and count pairs as slug lines."""
    if not isinstance(entries, (list, tuple)):
        raise TypeError("entries must be a list or tuple")
    lines = []
    for entry in entries:
        name, count = entry
        lines.append(f"{slugify(name)}: {count}")
    return "\n".join(lines)


def format_path(parts):
    """Render path segments as slugs joined by slashes."""
    if not isinstance(parts, (list, tuple)):
        raise TypeError("parts must be a list or tuple")
    return "/".join(slugify(part) for part in parts)


def format_unique(names):
    """Render names as unique slugs in their original order."""
    if not isinstance(names, (list, tuple)):
        raise TypeError("names must be a list or tuple")
    taken = set()
    result = []
    for name in names:
        slug = unique_slug(name, taken)
        taken.add(slug)
        result.append(slug)
    return result


def format_heading(title, width=30):
    """Render a normalised title with a rule underneath."""
    if isinstance(width, bool) or not isinstance(width, int):
        raise TypeError("width must be an integer")
    if width < 1:
        raise ValueError("width must be positive")
    heading = normalize_title(title)
    return heading + "\n" + "-" * min(len(heading), width)
