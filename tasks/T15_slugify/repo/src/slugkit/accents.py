"""Accent folding used before slug generation."""

import unicodedata


def strip_accents(text):
    """Return text with combining marks removed."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(char for char in decomposed if not unicodedata.combining(char))


def has_accent(text):
    """Return True when text contains a combining mark."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    decomposed = unicodedata.normalize("NFKD", text)
    return any(unicodedata.combining(char) for char in decomposed)


def fold_case(text):
    """Return text without accents in lower case."""
    return strip_accents(text).lower()


def compare_folded(left, right):
    """Return True when two strings match after folding."""
    return fold_case(left) == fold_case(right)
