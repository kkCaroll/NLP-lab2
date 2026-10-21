"""Text rendering for paged output and progress bars."""

from .limits import as_int, clamp, valid_page_size
from .paginate import page_count, paginate


def format_progress(done, total, width=10):
    """Render progress as a filled bar followed by a ratio."""
    done = as_int(done, "done")
    total = as_int(total, "total")
    if total <= 0:
        raise ValueError("total must be positive")
    if done < 0:
        raise ValueError("done must not be negative")
    filled = clamp(round(width * done / total), 0, width)
    bar = "#" * filled + "-" * (width - filled)
    return f"[{bar}] {done}/{total}"


def format_page(items, page, size):
    """Render one page as numbered lines."""
    size = valid_page_size(size)
    entries = paginate(items, page, size)
    lines = [
        f"{index}. {entry}"
        for index, entry in enumerate(entries, start=1)
    ]
    return "\n".join(lines)


def format_summary(items, size):
    """Render the page count and item count of a collection."""
    if not isinstance(items, (list, tuple)):
        raise TypeError("items must be a list or tuple")
    return f"items={len(items)} pages={page_count(len(items), size)}"


def format_ranges(total, size):
    """Render page ranges as a comma separated list."""
    from .chunks import page_ranges

    return ", ".join(f"{start}-{end}" for start, end in page_ranges(total, size))
