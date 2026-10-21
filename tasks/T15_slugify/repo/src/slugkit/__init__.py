from .accents import compare_folded, fold_case, has_accent, strip_accents
from .report import format_heading, format_index, format_path, format_unique
from .segments import (
    initials,
    sorted_words,
    split_words,
    unique_words,
    word_count,
)
from .slug import is_slug, slug_parts, slugify, unique_slug
from .title import normalize_title, shorten_title, title_case, title_key
from .whitespace import collapse_blank_lines, indent, normalize_whitespace

__all__ = [
    "collapse_blank_lines",
    "compare_folded",
    "fold_case",
    "format_heading",
    "format_index",
    "format_path",
    "format_unique",
    "has_accent",
    "indent",
    "initials",
    "is_slug",
    "normalize_title",
    "normalize_whitespace",
    "shorten_title",
    "slug_parts",
    "slugify",
    "sorted_words",
    "split_words",
    "strip_accents",
    "title_case",
    "title_key",
    "unique_slug",
    "unique_words",
    "word_count",
]
