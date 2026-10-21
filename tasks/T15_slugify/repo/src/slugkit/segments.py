"""Word and segment helpers shared by reports."""

from .title import title_key
from .whitespace import normalize_whitespace


def split_words(text):
    """Split normalised text into words."""
    normalized = normalize_whitespace(text)
    if not normalized:
        return []
    return normalized.split(" ")


def word_count(text):
    """Return the number of words in text."""
    return len(split_words(text))


def initials(text, limit=3):
    """Return the leading letters of the first words."""
    if isinstance(limit, bool) or not isinstance(limit, int):
        raise TypeError("limit must be an integer")
    if limit < 1:
        raise ValueError("limit must be positive")
    words = split_words(text)[:limit]
    return "".join(word[0].upper() for word in words if word)


def unique_words(text):
    """Return the words of text without repeats, preserving order."""
    seen = set()
    result = []
    for word in split_words(text):
        key = word.casefold()
        if key not in seen:
            seen.add(key)
            result.append(word)
    return result


def sorted_words(text):
    """Return the words of text in title key order."""
    return sorted(split_words(text), key=title_key)
