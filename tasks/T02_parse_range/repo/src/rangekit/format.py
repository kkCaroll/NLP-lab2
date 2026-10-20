"""Formatting helpers for inclusive integer ranges."""


def format_range(start, end):
    """Return a compact representation of one inclusive range."""
    if start == end:
        return str(start)
    return f"{start}-{end}"


def format_ranges(ranges):
    """Return compact representations for a sequence of ranges."""
    return [format_range(start, end) for start, end in ranges]


def summarize(ranges):
    """Return a comma-separated summary of a sequence of ranges."""
    return ", ".join(format_ranges(ranges))
