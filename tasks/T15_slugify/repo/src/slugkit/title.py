"""Title normalisation built on the shared whitespace helpers."""

from .whitespace import normalize_whitespace

SMALL_WORDS = {
    "a",
    "an",
    "and",
    "at",
    "for",
    "in",
    "of",
    "on",
    "or",
    "the",
    "to",
}


def title_case(text):
    """Return text with capitalised words and lowercase small words."""
    words = normalize_whitespace(text).split(" ")
    if words == [""]:
        return ""
    result = []
    for index, word in enumerate(words):
        lowered = word.lower()
        if index > 0 and lowered in SMALL_WORDS:
            result.append(lowered)
        else:
            result.append(lowered[:1].upper() + lowered[1:])
    return " ".join(result)


def normalize_title(text):
    """Return a single-spaced title with consistent capitalisation."""
    return title_case(text)


def title_key(text):
    """Return a comparison key for a title."""
    return normalize_whitespace(text).casefold()


def shorten_title(text, limit=40):
    """Return a title shortened to at most limit characters."""
    if isinstance(limit, bool) or not isinstance(limit, int):
        raise TypeError("limit must be an integer")
    if limit < 1:
        raise ValueError("limit must be positive")
    normalized = normalize_title(text)
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 1].rstrip() + "…"
