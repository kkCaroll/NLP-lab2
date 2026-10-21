"""Formatting helpers for sequences and permutation steps."""


def format_sequence(items):
    """Return a compact arrow representation of a sequence."""
    return " -> ".join(str(item) for item in items)


def format_permutations(permutations):
    """Return one arrow representation for each permutation."""
    return [format_sequence(items) for items in permutations]


def summarize_step(before, after):
    """Return a readable description of one permutation step."""
    if after is None:
        return f"{format_sequence(before)}; no next permutation"
    return f"{format_sequence(before)} => {format_sequence(after)}"
