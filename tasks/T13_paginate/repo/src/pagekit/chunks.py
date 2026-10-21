"""Batch helpers that turn page calculations into item ranges."""

from .limits import valid_page_size
from .paginate import page_count


def page_ranges(total, size):
    """Return start and end offsets for every page."""
    size = valid_page_size(size)
    count = page_count(total, size)
    return [
        (index * size, min((index + 1) * size, total))
        for index in range(count)
    ]


def chunk_pages(items, size):
    """Split items into one list per page."""
    if not isinstance(items, (list, tuple)):
        raise TypeError("items must be a list or tuple")
    return [
        list(items[start:end])
        for start, end in page_ranges(len(items), size)
    ]


def page_of(index, size):
    """Return the one-based page that contains index."""
    size = valid_page_size(size)
    if isinstance(index, bool) or not isinstance(index, int):
        raise TypeError("index must be an integer")
    if index < 0:
        raise ValueError("index must not be negative")
    return index // size + 1
