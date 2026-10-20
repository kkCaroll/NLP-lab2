"""Utilities for duplicate detection in sequences."""

from .analysis import first_repeat_gap, longest_repeated_run, repeat_gaps
from .report import duplicate_report
from .runs import longest_run_value, repeated_runs, run_lengths
from .search import (
    duplicate_positions,
    find_first_duplicate,
    find_first_in_sorted,
    first_duplicate_index,
    has_duplicate,
)
from .stats import duplicate_counts, duplicate_ratio, most_common_duplicate
from .validate import ensure_hashable, ensure_sequence, prepare

__all__ = [
    "duplicate_counts",
    "duplicate_positions",
    "duplicate_ratio",
    "duplicate_report",
    "ensure_hashable",
    "ensure_sequence",
    "find_first_duplicate",
    "find_first_in_sorted",
    "first_duplicate_index",
    "first_repeat_gap",
    "has_duplicate",
    "longest_repeated_run",
    "longest_run_value",
    "most_common_duplicate",
    "prepare",
    "repeat_gaps",
    "repeated_runs",
    "run_lengths",
]
