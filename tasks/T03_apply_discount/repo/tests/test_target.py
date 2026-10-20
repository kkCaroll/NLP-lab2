from decimal import Decimal

from pricing import apply_discount, discounted_total


def test_apply_discount_subtracts_percentage():
    assert apply_discount("100.00", 20) == Decimal("80.00")


def test_discounted_total_subtracts_percentage():
    items = [{"price": "50.00", "quantity": 2}]
    assert discounted_total(items, 20) == Decimal("80.00")
