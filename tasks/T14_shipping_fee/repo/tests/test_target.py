from decimal import Decimal

from logistics import parse_parcel, shipping_fee


def test_parse_parcel_converts_grams_to_kilograms():
    parcel = {
        "id": "p1",
        "weight": "2000",
        "unit": "g",
        "zone": "north",
    }
    assert parse_parcel(parcel)["weight_kg"] == Decimal("2")


def test_shipping_fee_uses_kilograms_for_gram_input():
    parcel = {
        "id": "p1",
        "weight": "2000",
        "unit": "g",
        "zone": "north",
    }
    assert shipping_fee(parcel) == Decimal("10.00")
