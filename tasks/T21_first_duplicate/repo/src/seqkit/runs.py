"""Helpers for consecutive runs in sequences."""

from .validate import prepare


def run_lengths(values):
    """Return the length of each run of equal adjacent values."""
    prepared = prepare(values)
    if not prepared:
        return []
    lengths = []
    current = 1
    for previous, value in zip(prepared, prepared[1:]):
        if value == previous:
            current += 1
        else:
            lengths.append(current)
            current = 1
    lengths.append(current)
    return lengths


def repeated_runs(values):
    """Return value and inclusive bounds for each run longer than one."""
    prepared = prepare(values)
    result = []
    start = 0
    for index in range(1, len(prepared) + 1):
        if index == len(prepared) or prepared[index] != prepared[start]:
            if index - start > 1:
                result.append((prepared[start], start, index - 1))
            start = index
    return result


def longest_run_value(values):
    """Return the value in the longest run, or None for an empty sequence."""
    prepared = prepare(values)
    if not prepared:
        return None
    best_value = prepared[0]
    best_length = 1
    current_length = 1
    for previous, value in zip(prepared, prepared[1:]):
        if value == previous:
            current_length += 1
        else:
            current_length = 1
        if current_length > best_length:
            best_value = value
            best_length = current_length
    return best_value
