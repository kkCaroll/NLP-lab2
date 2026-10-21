"""Text formatting for inventory records."""


def format_item(item):
    """Return one normalised item as a compact text line."""
    name = item.get("name", "")
    quantity = item.get("quantity", 1)
    category = item.get("category", "general")
    return f"{name} x{quantity} [{category}]"


def format_summary(summary):
    """Return units followed by category counts as a text line."""
    parts = [f"units={summary['units']}"]
    for category, count in sorted(summary.get("categories", {}).items()):
        parts.append(f"{category}={count}")
    return ", ".join(parts)
