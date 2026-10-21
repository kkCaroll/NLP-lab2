"""Text rendering for monetary amounts."""

from .rounding import round_money


def format_money(value):
    """Render value with two decimal places."""
    return f"{round_money(value):.2f}"


def format_signed(value):
    """Render value with an explicit sign."""
    amount = round_money(value)
    if amount > 0:
        return f"+{amount:.2f}"
    return f"{amount:.2f}"


def format_table(entries):
    """Render name and amount pairs as aligned lines."""
    if not isinstance(entries, (list, tuple)):
        raise TypeError("entries must be a list or tuple")
    lines = []
    for name, value in entries:
        lines.append(f"{name}: {format_money(value)}")
    return "\n".join(lines)


def format_percent(value, digits=2):
    """Render a percentage with a fixed number of decimals."""
    if isinstance(digits, bool) or not isinstance(digits, int):
        raise TypeError("digits must be an integer")
    if digits < 0:
        raise ValueError("digits must not be negative")
    return f"{value:.{digits}f}%"
