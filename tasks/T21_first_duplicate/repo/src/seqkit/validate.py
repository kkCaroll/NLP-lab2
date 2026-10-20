"""Input validation for sequence helpers."""


def ensure_sequence(values):
    """Return a list copy of a list or tuple, rejecting text inputs."""
    if isinstance(values, (str, bytes)):
        raise TypeError("values must be a sequence of items, not text")
    if not isinstance(values, (list, tuple)):
        raise TypeError("values must be a list or tuple")
    return list(values)


def ensure_hashable(values):
    """Return a list copy after checking that every value is hashable."""
    checked = []
    for value in values:
        try:
            hash(value)
        except TypeError as exc:
            raise TypeError("all values must be hashable") from exc
        checked.append(value)
    return checked


def prepare(values):
    """Validate a sequence and return a hashable list copy."""
    return ensure_hashable(ensure_sequence(values))
