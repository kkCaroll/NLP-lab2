"""Lexicographic permutation helpers."""


def rotate_suffix(items, start):
    """Return a copy with the suffix beginning at start reversed."""
    if start < 0 or start > len(items):
        raise ValueError("start is outside the sequence")
    return list(items[:start]) + list(reversed(items[start:]))


def next_permutation(items):
    """Return the next lexicographic permutation, or None at the last one."""
    values = list(items)
    if len(values) < 2:
        return None
    pivot = len(values) - 2
    while pivot >= 0 and values[pivot] >= values[pivot + 1]:
        pivot -= 1
    if pivot < 0:
        return None
    successor = len(values) - 1
    while values[successor] <= values[pivot]:
        successor -= 1
    values[pivot], values[successor] = values[successor], values[pivot]
    values[pivot:] = reversed(values[pivot:])
    return values


def permutations_from(items, count):
    """Return up to count successive permutations after items."""
    current = list(items)
    result = []
    for _ in range(count):
        current = next_permutation(current)
        if current is None:
            break
        result.append(current)
    return result
