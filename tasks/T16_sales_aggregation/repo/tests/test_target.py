from decimal import Decimal

from saleskit.aggregate import aggregate_sales, total_revenue
from saleskit.report import sales_report


def test_refund_reduces_region_total():
    rows = [
        {"region": "north", "kind": "sale", "amount": "100.00"},
        {"region": "north", "kind": "refund", "amount": "30.00"},
    ]
    assert aggregate_sales(rows) == {"north": Decimal("70.00")}


def test_total_revenue_is_net_of_refunds():
    rows = [
        {"region": "north", "kind": "sale", "amount": "100.00"},
        {"region": "north", "kind": "refund", "amount": "30.00"},
        {"region": "south", "kind": "sale", "amount": "50.00"},
        {"region": "south", "kind": "refund", "amount": "20.00"},
    ]
    assert total_revenue(rows) == Decimal("100.00")


def test_sales_report_uses_net_revenue():
    rows = [
        {"region": "north", "kind": "sale", "amount": "100.00"},
        {"region": "north", "kind": "refund", "amount": "30.00"},
        {"region": "south", "kind": "sale", "amount": "50.00"},
        {"region": "south", "kind": "refund", "amount": "20.00"},
    ]
    report = sales_report(rows)
    assert report["by_region"] == {
        "north": Decimal("70.00"),
        "south": Decimal("30.00"),
    }
    assert report["total"] == Decimal("100.00")
    assert report["top_region"] == "north"
    assert report["lines"] == [
        "north: 70.00",
        "south: 30.00",
        "total: 100.00",
    ]
