"""Text to boolean conversion for command line flags."""

TRUE_WORDS = frozenset({"1", "true", "yes", "on"})
FALSE_WORDS = frozenset({"0", "false", "no", "off"})


def to_bool(text):
    """Return text as a boolean flag value."""
    if isinstance(text, bool):
        return text
    if not isinstance(text, str):
        raise TypeError("flag value must be a string")
    normalized = text.strip().lower()
    if normalized in TRUE_WORDS:
        return True
    if normalized in FALSE_WORDS:
        return False
    raise ValueError(f"not a flag value: {text}")


def format_bool(value):
    """Render a flag value as text."""
    return "true" if to_bool(value) else "false"


def invert(value):
    """Return the opposite flag value."""
    return not to_bool(value)
