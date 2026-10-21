"""Text normalisation helpers."""

import string


def normalize_spaces(text):
    """Return text with runs of whitespace collapsed to one space."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return " ".join(text.split())


def trim_lines(text):
    """Return text with leading and trailing space removed on each line."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return "\n".join(line.strip() for line in text.splitlines())


def collapse_blank_lines(text):
    """Return text without empty or whitespace-only lines."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return "\n".join(line for line in text.splitlines() if line.strip())


def strip_punctuation(text):
    """Return text without leading and trailing ASCII punctuation."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return text.strip(string.punctuation)
