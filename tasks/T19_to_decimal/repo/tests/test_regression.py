from decimal import Decimal

import pytest

from moneykit import (
    add_amounts,
    add_tax,
    apply_rate,
    as_percent,
    average_amount,
    ceil_money,
    check_currency,
    currency_label,
    discount_amount,
    floor_money,
    format_money,
    format_percent,
    format_signed,
    format_table,
    is_amount,
    is_zero,
    largest_amount,
    negate,
    percent_of,
    round_money,
    round_units,
    same_amount,
    split_cents,
    subtotal,
    subtract_amounts,
    sum_amounts,
    to_decimal,
)


def test_to_decimal_from_text_and_integers():
    assert to_decimal("1.005") == Decimal("1.005")
    assert to_decimal(" 2.5 ") == Decimal("2.5")
    assert to_decimal(3) == Decimal("3")
    assert to_decimal(Decimal("4.25")) == Decimal("4.25")


def test_to_decimal_errors():
    with pytest.raises(ValueError):
        to_decimal("abc")
    assert is_amount("1.5") is True
    assert is_amount("abc") is False
    assert same_amount("2.50", 2.5) is True


def test_round_money_with_text_inputs():
    assert round_money("2.675") == Decimal("2.68")
    assert round_money("2.674") == Decimal("2.67")
    assert round_money("-2.675") == Decimal("-2.68")


def test_floor_ceil_and_units():
    assert floor_money("2.679") == Decimal("2.67")
    assert ceil_money("2.671") == Decimal("2.68")
    assert round_units("2.5") == Decimal("3")
    assert split_cents("2.675") == (2, 68)


def test_totals():
    assert sum_amounts(["1.10", "2.20"]) == Decimal("3.30")
    assert subtotal(["10.00", "5.00"], "2.50") == Decimal("12.50")
    assert average_amount(["1.00", "2.00"]) == Decimal("1.50")
    assert largest_amount(["1.00", "3.50"]) == Decimal("3.50")
    with pytest.raises(ValueError):
        average_amount([])


def test_rates_and_percentages():
    assert apply_rate("10.00", "0.15") == Decimal("1.50")
    assert percent_of("200.00", "12.5") == Decimal("25.00")
    assert discount_amount("80.00", "10") == Decimal("8.00")
    assert add_tax("100.00", "6") == Decimal("106.00")
    assert as_percent("1", "4") == Decimal("25.00")


def test_currency_helpers():
    assert check_currency(" cny ") == "CNY"
    with pytest.raises(ValueError):
        check_currency("GBP")
    assert currency_label("usd") == "dollar"
    assert add_amounts("1.25", "2.75") == Decimal("4.00")
    assert subtract_amounts("4.00", "1.25") == Decimal("2.75")
    assert negate("1.25") == Decimal("-1.25")
    assert is_zero("0.00") is True


def test_format_helpers():
    assert format_money("1.005") == "1.01"
    assert format_signed("1.5") == "+1.50"
    assert format_signed("-1.5") == "-1.50"
    assert format_table([("tea", "1.5")]) == "tea: 1.50"
    assert format_percent(Decimal("12.5")) == "12.50%"
    with pytest.raises(ValueError):
        format_percent(1, digits=-1)
