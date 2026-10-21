"""Stock record normalisation and mutation helpers."""


def normalize_item(item):
    """Return a checked item with defaults for quantity and category."""
    if not isinstance(item, dict):
        raise TypeError("item must be a dictionary")
    name = item.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("item name must be a non-empty string")
    quantity = item.get("quantity", 1)
    if isinstance(quantity, bool) or not isinstance(quantity, int):
        raise TypeError("quantity must be an integer")
    if quantity < 0:
        raise ValueError("quantity must not be negative")
    category = item.get("category", "general")
    if not isinstance(category, str) or not category.strip():
        raise ValueError("category must be a non-empty string")
    return {
        "name": name.strip(),
        "quantity": quantity,
        "category": category.strip(),
    }


def add_item(items, item):
    """Return a new list with the item appended in normalised form."""
    if not isinstance(items, (list, tuple)):
        raise TypeError("items must be a list or tuple")
    result = [normalize_item(entry) for entry in items]
    result.append(normalize_item(item))
    return result


def remove_item(items, name, quantity=1):
    """Return a new list with quantity removed from the named item."""
    if not isinstance(quantity, int) or isinstance(quantity, bool):
        raise TypeError("quantity must be an integer")
    if quantity <= 0:
        raise ValueError("quantity must be positive")
    result = []
    found = False
    for entry in items:
        record = normalize_item(entry)
        if record["name"] == name:
            found = True
            remaining = record["quantity"] - quantity
            if remaining < 0:
                raise ValueError("not enough units to remove")
            record["quantity"] = remaining
        result.append(record)
    if not found:
        raise KeyError(name)
    return result
