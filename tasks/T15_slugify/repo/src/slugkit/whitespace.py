"""Whitespace normalisation shared by titles and slugs."""

import re

SPACE_PATTERN = re.compile(r"\s+")


def require_text(text, name="text"):
    """Return text or raise a type error."""
    if not isinstance(text, str):
        raise TypeError(f"{name} must be a string")
    return text


def normalize_whitespace(text):
    """Collapse runs of whitespace into single spaces."""
    return SPACE_PATTERN.sub(" ", require_text(text).strip())


def collapse_blank_lines(text):
    """Reduce repeated blank lines to one empty line."""
    lines = require_text(text).splitlines()
    result = []
    for line in lines:
        stripped = line.rstrip()
        if not stripped and result and not result[-1]:
            continue
        result.append(stripped)
    return "\n".join(result).strip()


def indent(text, prefix="    "):
    """Prefix every non-empty line of text."""
    if not isinstance(prefix, str):
        raise TypeError("prefix must be a string")
    return "\n".join(
        prefix + line if line else line
        for line in require_text(text).splitlines()
    )
