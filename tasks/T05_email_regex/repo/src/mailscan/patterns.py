"""Regular expressions and text helpers for email addresses."""

import re

EMAIL_PATTERN = re.compile(
    r"(?<![A-Za-z0-9._%+-])"
    r"[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    r"(?![A-Za-z0-9.-])"
)


def is_email(value):
    """Return True when value is a complete email address."""
    if not isinstance(value, str):
        return False
    return EMAIL_PATTERN.fullmatch(value) is not None


def extract_emails(text):
    """Return all email addresses found in text, in source order."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return EMAIL_PATTERN.findall(text)


def replace_emails(text, replacement="[email]"):
    """Replace every email address in text with replacement."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(replacement, str):
        raise TypeError("replacement must be a string")
    return EMAIL_PATTERN.sub(replacement, text)
