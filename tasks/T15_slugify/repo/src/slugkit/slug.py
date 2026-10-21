"""Slug generation built on the shared whitespace helpers."""

import re

from .accents import strip_accents
from .whitespace import normalize_whitespace

SLUG_PATTERN = re.compile(r"[^a-z0-9]")
VALID_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def slugify(text):
    """Return a lowercase hyphenated slug for text."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    normalized = normalize_whitespace(strip_accents(text)).lower()
    return SLUG_PATTERN.sub("-", normalized).strip("-")


def slug_parts(text):
    """Return the non-empty segments of a slug."""
    return [part for part in slugify(text).split("-") if part]


def is_slug(text):
    """Return True when text is already a valid slug."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return bool(VALID_SLUG.match(text))


def unique_slug(text, taken):
    """Return a slug that does not appear in taken.

    Repeated names receive a numeric suffix starting at two.
    """
    if not isinstance(taken, (set, list, tuple)):
        raise TypeError("taken must be a set, list or tuple")
    base = slugify(text)
    if base not in taken:
        return base
    index = 2
    while f"{base}-{index}" in taken:
        index += 1
    return f"{base}-{index}"
