from .normalize import collapse_blank_lines, normalize_spaces, strip_punctuation, trim_lines
from .patterns import (
    extract_versions,
    find_version_positions,
    has_prerelease,
    is_version,
    replace_versions,
)
from .report import format_versions, group_by_major, summarize_versions, version_majors

__all__ = [
    "collapse_blank_lines",
    "extract_versions",
    "find_version_positions",
    "format_versions",
    "group_by_major",
    "has_prerelease",
    "is_version",
    "normalize_spaces",
    "replace_versions",
    "strip_punctuation",
    "summarize_versions",
    "trim_lines",
    "version_majors",
]
