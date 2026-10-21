"""Parsing helpers for date and time text."""

from datetime import date, datetime

DATE_PATTERN = "%Y-%m-%d"
DATETIME_PATTERN = "%Y-%m-%d %H:%M"


def parse_date(text):
    """Parse text as a calendar date."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    try:
        return datetime.strptime(text.strip(), DATE_PATTERN).date()
    except ValueError:
        raise ValueError(f"invalid date: {text}") from None


def parse_datetime(text):
    """Parse text as a date and time without seconds."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    try:
        return datetime.strptime(text.strip(), DATETIME_PATTERN)
    except ValueError:
        raise ValueError(f"invalid datetime: {text}") from None


def parse_optional(text):
    """Parse text when present and return None for empty input."""
    if text is None:
        return None
    if not isinstance(text, str):
        raise TypeError("text must be a string or None")
    text = text.strip()
    if not text:
        return None
    if " " in text:
        return parse_datetime(text)
    return parse_date(text)


def parse_many(texts):
    """Parse a sequence of date strings."""
    if not isinstance(texts, (list, tuple)):
        raise TypeError("texts must be a list or tuple")
    parsed = []
    for text in texts:
        moment = parse_optional(text)
        if moment is not None:
            parsed.append(moment)
    return parsed
