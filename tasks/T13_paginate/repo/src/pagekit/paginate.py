"""Paging helpers built on the shared numeric limits."""

from .limits import MIN_PAGE, as_int, clamp, valid_page_size


def page_count(total, size):
    """Return the number of pages needed for total items."""
    total = as_int(total, "total")
    if total < 0:
        raise ValueError("total must not be negative")
    size = valid_page_size(size)
    if total == 0:
        return 0
    return (total + size - 1) // size


def resolve_page(page, total, size):
    """Return the requested page clamped to the available range."""
    page = as_int(page, "page")
    count = page_count(total, size)
    if count == 0:
        return MIN_PAGE
    return clamp(page, MIN_PAGE, count)


def paginate(items, page, size):
    """Return the items on the requested page.

    Requests beyond the final page fall back to the final page.
    """
    if not isinstance(items, (list, tuple)):
        raise TypeError("items must be a list or tuple")
    size = valid_page_size(size)
    resolved = resolve_page(page, len(items), size)
    start = (resolved - 1) * size
    return list(items[start:start + size])


def last_page(items, size):
    """Return the items on the final page."""
    if not isinstance(items, (list, tuple)):
        raise TypeError("items must be a list or tuple")
    count = page_count(len(items), size)
    if count == 0:
        return []
    return paginate(items, count, size)
