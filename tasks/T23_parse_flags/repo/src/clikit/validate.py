"""Validation helpers for command line values."""

MIN_REPEAT = 1
MAX_REPEAT = 10
MAX_NAME = 40


def normalize_name(name):
    """Return a trimmed name with single spaces."""
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    normalized = " ".join(name.split())
    if not normalized:
        raise ValueError("name must not be empty")
    if len(normalized) > MAX_NAME:
        raise ValueError(f"name must be at most {MAX_NAME} characters")
    return normalized


def check_repeat(repeat):
    """Return a repeat count inside the supported range."""
    if isinstance(repeat, bool) or not isinstance(repeat, int):
        raise TypeError("repeat must be an integer")
    if repeat < MIN_REPEAT or repeat > MAX_REPEAT:
        raise ValueError(f"repeat must be between {MIN_REPEAT} and {MAX_REPEAT}")
    return repeat


def check_command(command):
    """Return a supported command name."""
    if command not in ("greet", "summarize"):
        raise ValueError(f"unsupported command: {command}")
    return command
