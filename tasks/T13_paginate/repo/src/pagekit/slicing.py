"""Window slicing helpers that reuse the shared limits."""

from .limits import clamp, valid_page_size


def slice_window(items, start, size):
    """Return up to size items from start, clamped to the final window.

    A start value beyond the list falls back to the start of the final
    window so that the returned list keeps the requested window length.
    """
    if not isinstance(items, (list, tuple)):
        raise TypeError("items must be a list or tuple")
    size = valid_page_size(size)
    if not items:
        return []
    last_start = max(0, len(items) - size)
    start = clamp(start, 0, last_start)
    return list(items[start:start + size])


def first_window(items, size):
    """Return the first size items."""
    return slice_window(items, 0, size)


def tail_window(items, size):
    """Return the final size items."""
    if not items:
        return []
    return slice_window(items, len(items) - 1, size)
