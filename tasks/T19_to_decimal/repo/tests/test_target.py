from decimal import Decimal

from moneykit import format_money, round_money


def test_round_money_rounds_a_float_half_cent_upwards():
    assert round_money(2.675) == Decimal("2.68")


def test_format_money_rounds_a_float_half_cent_upwards():
    assert format_money(1.005) == "1.01"
