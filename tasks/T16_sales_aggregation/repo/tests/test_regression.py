from decimal import Decimal

import pytest

from saleskit.aggregate import aggregate_sales, top_region, total_revenue
from saleskit.filters import filter_region, refunds_only, sales_only, sort_records
from saleskit.metrics import average_sale, refund_rate, region_share
from saleskit.money import format_amount, sum_amounts, to_amount
from saleskit.records import normalize_record, normalize_records
from saleskit.report import summary_lines


def test_to_amount_rounds_to_cents():
    assert to_amount("10.005") == Decimal("10.01")
    assert to_amount(2) == Decimal("2.00")
    assert to_amount(Decimal("3.456")) == Decimal("3.46")


def test_format_amount_and_sum():
    assert format_amount("7.5") == "7.50"
    assert sum_amounts(["1.10", "2.20"]) == Decimal("3.30")


def test_normalize_record_lowercases_and_rounds():
    record = normalize_record(
        {"region": " North ", "kind": "SALE", "amount": "12.345"}
    )
    assert record == {
        "region": "north",
        "kind": "sale",
        "amount": Decimal("12.35"),
    }


def test_sales_only_aggregation():
    rows = [
        {"region": "north", "kind": "sale", "amount": "75"},
        {"region": "south", "kind": "sale", "amount": "25"},
    ]
    assert aggregate_sales(rows) == {
        "north": Decimal("75.00"),
        "south": Decimal("25.00"),
    }
    assert total_revenue(rows) == Decimal("100.00")


def test_multiple_regions_sales_only():
    rows = [
        {"region": "west", "kind": "sale", "amount": "10"},
        {"region": "east", "kind": "sale", "amount": "20"},
        {"region": "west", "kind": "sale", "amount": "30"},
    ]
    assert aggregate_sales(rows) == {
        "east": Decimal("20.00"),
        "west": Decimal("40.00"),
    }


def test_empty_rows():
    assert aggregate_sales([]) == {}
    assert total_revenue([]) == Decimal("0.00")
    assert top_region([]) is None
    assert summary_lines([]) == ["total: 0.00"]


def test_invalid_kind_raises():
    with pytest.raises(ValueError):
        normalize_record({"region": "north", "kind": "discount", "amount": "1"})


def test_top_region_sales_only():
    rows = [
        {"region": "north", "kind": "sale", "amount": "75"},
        {"region": "south", "kind": "sale", "amount": "25"},
    ]
    assert top_region(rows) == "north"


def test_filters_and_sorting():
    rows = [
        {"region": "north", "kind": "sale", "amount": "10"},
        {"region": "north", "kind": "refund", "amount": "2"},
        {"region": "south", "kind": "sale", "amount": "5"},
    ]
    assert [record["amount"] for record in sales_only(rows)] == [
        Decimal("10.00"),
        Decimal("5.00"),
    ]
    assert [record["amount"] for record in refunds_only(rows)] == [Decimal("2.00")]
    assert [record["amount"] for record in filter_region(rows, "north")] == [
        Decimal("10.00"),
        Decimal("2.00"),
    ]
    assert [record["amount"] for record in sort_records(rows)] == [
        Decimal("2.00"),
        Decimal("10.00"),
        Decimal("5.00"),
    ]


def test_metrics_sales_only():
    rows = [
        {"region": "north", "kind": "sale", "amount": "75"},
        {"region": "south", "kind": "sale", "amount": "25"},
    ]
    assert average_sale(rows) == Decimal("50.00")
    assert region_share(rows) == {
        "north": Decimal("0.7500"),
        "south": Decimal("0.2500"),
    }


def test_refund_rate():
    rows = [
        {"region": "north", "kind": "sale", "amount": "100"},
        {"region": "north", "kind": "refund", "amount": "25"},
    ]
    assert refund_rate(rows) == Decimal("0.2500")


def test_summary_lines_sales_only():
    rows = [
        {"region": "north", "kind": "sale", "amount": "75"},
        {"region": "south", "kind": "sale", "amount": "25"},
    ]
    assert summary_lines(rows) == [
        "north: 75.00",
        "south: 25.00",
        "total: 100.00",
    ]


def test_normalize_records_rejects_non_list():
    with pytest.raises(TypeError):
        normalize_records({"region": "north"})
