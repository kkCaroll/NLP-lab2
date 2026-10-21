"""Boolean conversion shared by configuration and command line helpers."""

TRUE_WORDS = frozenset({"1", "true", "yes", "on"})
FALSE_WORDS = frozenset({"0", "false", "no", "off"})


def parse_bool(value):
    """Return value as a boolean.

    Text values accept one, true, yes and on for true and zero, false,
    no and off for false. Other text raises a value error.
    """
    if isinstance(value, bool):
        return value
    return bool(value)


def format_bool(value):
    """Render value as the text true or false."""
    return "true" if parse_bool(value) else "false"


def is_true(value):
    """Return True only when value denotes true."""
    return parse_bool(value) is True


def toggle(value):
    """Return the opposite of value after conversion."""
    return not parse_bool(value)
