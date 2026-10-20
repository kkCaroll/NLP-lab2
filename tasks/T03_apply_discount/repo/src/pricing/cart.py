"""Shopping cart totals."""

from .discount import apply_discount
from .money import add_money, round_money, to_decimal


def line_total(price, quantity):
    """Return the total for one cart line."""
    if isinstance(quantity, bool) or not isinstance(quantity, int):
        raise TypeError("quantity must be an integer")
    if quantity < 0:
        raise ValueError("quantity must be non-negative")
    return round_money(to_decimal(price) * quantity)


def cart_total(items):
    """Return the sum of all cart line totals."""
    if not isinstance(items, (list, tuple)):
        raise TypeError("items must be a list or tuple")
    total = to_decimal("0")
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("each item must be a mapping")
        if "price" not in item or "quantity" not in item:
            raise ValueError("each item must contain price and quantity")
        total = add_money(total, line_total(item["price"], item["quantity"]))
    return round_money(total)


def discounted_total(items, percent):
    """Return the cart total after applying a percentage discount."""
    return apply_discount(cart_total(items), percent)
