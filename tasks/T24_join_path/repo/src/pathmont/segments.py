"""Segment checks for paths built from untrusted text."""

FORBIDDEN = ("", ".", "..")


def safe_segment(segment):
    """Return a segment without separators."""
    if not isinstance(segment, str):
        raise TypeError("segment must be a string")
    cleaned = segment.replace("\\", "/").strip("/")
    if cleaned in FORBIDDEN:
        raise ValueError("unsafe path segment")
    if ".." in cleaned.split("/"):
        raise ValueError("unsafe path segment")
    return cleaned


def check_parts(parts):
    """Return parts after checking every segment."""
    if not isinstance(parts, (list, tuple)):
        raise TypeError("parts must be a list or tuple")
    return [safe_segment(part) for part in parts]


def sanitize_segment(segment, replacement="_"):
    """Return a segment with unsupported characters replaced."""
    if not isinstance(segment, str):
        raise TypeError("segment must be a string")
    if not isinstance(replacement, str) or len(replacement) != 1:
        raise ValueError("replacement must be one character")
    cleaned = segment.replace("\\", "/").strip("/")
    result = "".join(
        char if char.isalnum() or char in "-_." else replacement
        for char in cleaned
    )
    return result or replacement


def segment_depth(path):
    """Return the number of segments in path."""
    from .normalize import split_parts

    return len(split_parts(path))
