"""Combined reports for duplicate detection."""

from .analysis import first_repeat_gap, longest_repeated_run, repeat_gaps
from .search import (
    duplicate_positions,
    find_first_duplicate,
    first_duplicate_index,
    has_duplicate,
)
from .stats import duplicate_counts, duplicate_ratio, most_common_duplicate


def duplicate_report(values):
    """Return a dictionary with positional and frequency information."""
    return {
        "first_duplicate": find_first_duplicate(values),
        "first_index": first_duplicate_index(values),
        "has_duplicate": has_duplicate(values),
        "positions": duplicate_positions(values),
        "counts": duplicate_counts(values),
        "most_common": most_common_duplicate(values),
        "first_gap": first_repeat_gap(values),
        "gaps": repeat_gaps(values),
        "longest_run": longest_repeated_run(values),
        "ratio": duplicate_ratio(values),
    }
