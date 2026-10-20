from decimal import Decimal

import pytest

from pricing import (
    add_money,
    apply_discount,
    cart_total,
    discounted_total,
    format_money,
    line_total,
    round_money,
    subtract_money,
    to_decimal,
    validate_percent,
)


def test_to_decimal_accepts_numbers_and_text():
    assert to_decimal(12) == Decimal("12")
    assert to_decimal("12.50") == Decimal("12.50")


def test_to_decimal_rejects_invalid_values():
    with pytest.raises(TypeError):
        to_decimal(True)
    with pytest.raises(ValueError):
        to_decimal("abc")
    with pytest.raises(ValueError):
        to_decimal(float("nan"))


def test_round_money_rounds_half_up():
    assert round_money("1.005") == Decimal("1.01")
    assert round_money("2.344") == Decimal("2.34")


def test_format_money():
    assert format_money("2.5") == "2.50"
    assert format_money(3) == "3.00"


def test_add_and_subtract_money():
    assert add_money("1.10", "2.20") == Decimal("3.30")
    assert subtract_money("3.30", "1.10") == Decimal("2.20")


def test_line_total():
    assert line_total("19.99", 3) == Decimal("59.97")
    assert line_total("5.00", 0) == Decimal("0.00")


def test_cart_total_single_item():
    assert cart_total([{"price": "2.50", "quantity": 4}]) == Decimal("10.00")


def test_cart_total_multiple_items():
    items = [
        {"price": "1.10", "quantity": 2},
        {"price": "2.20", "quantity": 1},
    ]
    assert cart_total(items) == Decimal("4.40")


def test_cart_total_empty():
    assert cart_total([]) == Decimal("0.00")


def test_cart_total_rejects_non_list():
    with pytest.raises(TypeError):
        cart_total("not a cart")


def test_cart_item_requires_price_and_quantity():
    with pytest.raises(ValueError):
        cart_total([{"price": "1.00"}])
    with pytest.raises(ValueError):
        cart_total(["item"])


def test_line_total_rejects_negative_quantity():
    with pytest.raises(ValueError):
        line_total("1.00", -1)


def test_line_total_rejects_boolean_quantity():
    with pytest.raises(TypeError):
        line_total("1.00", True)


def test_apply_discount_zero_percent():
    assert apply_discount("42.00", 0) == Decimal("42.00")


def test_discounted_total_zero_percent():
    assert discounted_total([{"price": "9.99", "quantity": 1}], 0) == Decimal("9.99")


def test_validate_percent_bounds():
    assert validate_percent(0) == Decimal("0")
    assert validate_percent(100) == Decimal("100")
    with pytest.raises(ValueError):
        validate_percent(-1)
    with pytest.raises(ValueError):
        validate_percent(101)
