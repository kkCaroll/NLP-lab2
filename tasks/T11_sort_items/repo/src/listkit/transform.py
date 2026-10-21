"""Grouping helpers for lists."""


def partition(items, predicate):
    """Split items into entries that match and entries that do not."""
    if not callable(predicate):
        raise TypeError("predicate must be callable")
    matches = []
    rest = []
    for item in items:
        if predicate(item):
            matches.append(item)
        else:
            rest.append(item)
    return matches, rest


def flatten(groups):
    """Concatenate a sequence of groups into one list."""
    result = []
    for group in groups:
        if not isinstance(group, (list, tuple)):
            raise TypeError("each group must be a list or tuple")
        result.extend(group)
    return result


def chunk(items, size):
    """Split items into consecutive lists of at most size entries."""
    if not isinstance(size, int) or isinstance(size, bool):
        raise TypeError("size must be an integer")
    if size < 1:
        raise ValueError("size must be positive")
    return [list(items[index:index + size]) for index in range(0, len(items), size)]


def rotate(items, steps):
    """Return a rotated copy of items."""
    if not items:
        return []
    offset = steps % len(items)
    return list(items[offset:]) + list(items[:offset])
