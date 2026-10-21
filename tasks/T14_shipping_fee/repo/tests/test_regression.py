from decimal import Decimal

import pytest

from logistics import (
    base_rate,
    batch_summary,
    batch_total,
    describe_parcel,
    express_multiplier,
    express_parcels,
    fee_table,
    format_weight,
    group_by_zone,
    heaviest_parcel,
    parse_parcel,
    quote_summary,
    shipping_fee,
    to_grams,
    to_kilograms,
    zone_surcharge,
)


def test_to_kilograms_kilograms():
    assert to_kilograms("2.5", "kg") == Decimal("2.5")
    assert to_kilograms(3, "KG") == Decimal("3")


def test_to_kilograms_pounds():
    assert to_kilograms("2", "lb") == Decimal("0.90718474")


def test_to_grams():
    assert to_grams("1", "kg") == Decimal("1000")
    assert to_grams("0.5", "kg") == Decimal("500.0")


def test_format_weight():
    assert format_weight("1.5", "kg") == "1.500 kg"


def test_parse_parcel_kilograms():
    parcel = {"id": 7, "weight": "2", "unit": "kg", "zone": " South "}
    parsed = parse_parcel(parcel)
    assert parsed["id"] == "7"
    assert parsed["weight_kg"] == Decimal("2")
    assert parsed["zone"] == "south"
    assert parsed["express"] is False


def test_parse_parcel_zero_grams():
    parcel = {"id": "p0", "weight": "0", "unit": "g", "zone": "north"}
    assert parse_parcel(parcel)["weight_kg"] == Decimal("0")


def test_describe_parcel():
    parcel = {"id": "p1", "weight": "2", "unit": "kg", "zone": "north"}
    assert describe_parcel(parcel) == "p1 2.00kg north standard"


def test_base_rate_and_surcharge():
    assert base_rate("2") == Decimal("10.00")
    assert base_rate("0") == Decimal("5.00")
    assert zone_surcharge("north") == Decimal("0.00")
    assert zone_surcharge("remote") == Decimal("5.00")


def test_express_multiplier():
    assert express_multiplier(True) == Decimal("1.50")
    assert express_multiplier(False) == Decimal("1.00")


def test_shipping_fee_kilograms_express():
    parcel = {
        "id": "p1",
        "weight": "2",
        "unit": "kg",
        "zone": "south",
        "express": True,
    }
    assert shipping_fee(parcel) == Decimal("18.00")


def test_quote_summary_kilograms():
    parcel = {"id": "p1", "weight": "2", "unit": "kg", "zone": "north"}
    assert quote_summary(parcel) == "p1: north 2.00 kg standard 10.00"


def test_batch_helpers():
    parcels = [
        {"id": "p1", "weight": "1", "unit": "kg", "zone": "north"},
        {
            "id": "p2",
            "weight": "2",
            "unit": "kg",
            "zone": "north",
            "express": True,
        },
    ]
    assert batch_total(parcels) == Decimal("22.50")
    assert group_by_zone(parcels) == {"north": ["p1", "p2"]}
    assert heaviest_parcel(parcels)["id"] == "p2"
    assert express_parcels(parcels)[0]["id"] == "p2"
    assert batch_summary(parcels) == "2 parcels, 1 express, total 22.50"
    assert fee_table(parcels)["p1"] == Decimal("7.50")


def test_invalid_units_and_weights():
    with pytest.raises(ValueError):
        to_kilograms("1", "stone")
    with pytest.raises(ValueError):
        to_kilograms("-1", "kg")
    with pytest.raises(TypeError):
        to_kilograms(True, "kg")
    with pytest.raises(ValueError):
        to_kilograms("abc", "kg")


def test_invalid_parcel_shapes():
    with pytest.raises(TypeError):
        parse_parcel("parcel")
    with pytest.raises(ValueError):
        parse_parcel({"id": "p1", "weight": "1", "unit": "kg"})
    with pytest.raises(TypeError):
        parse_parcel(
            {"id": "p1", "weight": "1", "unit": "kg", "zone": "north", "express": 1}
        )
    with pytest.raises(ValueError):
        parse_parcel(
            {"id": "p1", "weight": "1", "unit": "kg", "zone": "west"}
        )
