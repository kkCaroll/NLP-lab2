"""Summary helpers for inventory records."""

from .stock import normalize_item


def total_units(items):
    """Return the total quantity, counting an omitted quantity as one."""
    if not isinstance(items, (list, tuple)):
        raise TypeError("items must be a list or tuple")
    total = 0
    for item in items:
        if not isinstance(item, dict):
            raise TypeError("each item must be a dictionary")
        total += item.get("quantity", 0)
    return total


def count_categories(items):
    """Return the number of items per category."""
    if not isinstance(items, (list, tuple)):
        raise TypeError("items must be a list or tuple")
    counts = {}
    for item in items:
        record = normalize_item(item)
        category = record["category"]
        counts[category] = counts.get(category, 0) + 1
    return counts


def low_stock(items, threshold):
    """Return names whose quantity is at or below the threshold."""
    if not isinstance(threshold, int) or isinstance(threshold, bool):
        raise TypeError("threshold must be an integer")
    if threshold < 0:
        raise ValueError("threshold must not be negative")
    names = []
    for item in items:
        record = normalize_item(item)
        if record["quantity"] <= threshold:
            names.append(record["name"])
    return names


def summarize_inventory(items):
    """Return total units and category counts for a list of items."""
    return {
        "units": total_units(items),
        "categories": count_categories(items),
    }
