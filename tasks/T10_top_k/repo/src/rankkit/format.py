"""Text rendering for ranked entries."""

from .stats import mean, spread


def format_ranking(entries):
    """Render named scores as a numbered ranking."""
    if not isinstance(entries, (list, tuple)):
        raise TypeError("entries must be a list or tuple")
    lines = []
    for index, entry in enumerate(entries, start=1):
        name, score = entry
        lines.append(f"{index}. {name}: {score}")
    return "\n".join(lines)


def summarize(values):
    """Render count, mean and spread of a score list."""
    return f"count={len(values)} mean={mean(values):.2f} spread={spread(values)}"


def format_table(entries, width=12):
    """Render name and score columns with a fixed name width."""
    if not isinstance(width, int) or isinstance(width, bool):
        raise TypeError("width must be an integer")
    if width < 1:
        raise ValueError("width must be positive")
    rows = [f"{'name':<{width}} score"]
    for name, score in entries:
        rows.append(f"{name:<{width}} {score}")
    return "\n".join(rows)
