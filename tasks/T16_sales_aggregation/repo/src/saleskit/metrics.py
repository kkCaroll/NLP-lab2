"""Summary metrics derived from sales records."""

from decimal import Decimal

from .aggregate import aggregate_sales
from .money import CENT
from .records import normalize_records

RATE_QUANTUM = Decimal("0.0001")


def refund_rate(rows):
    """Return refunds divided by gross sales, or zero when sales are zero."""
    records = normalize_records(rows)
    sales = sum(
        (record["amount"] for record in records if record["kind"] == "sale"),
        Decimal("0.00"),
    )
    refunds = sum(
        (record["amount"] for record in records if record["kind"] == "refund"),
        Decimal("0.00"),
    )
    if sales == 0:
        return Decimal("0.00")
    return (refunds / sales).quantize(RATE_QUANTUM)


def average_sale(rows):
    """Return the mean sale amount, or zero when there are no sales."""
    amounts = [
        record["amount"]
        for record in normalize_records(rows)
        if record["kind"] == "sale"
    ]
    if not amounts:
        return Decimal("0.00")
    return (sum(amounts, Decimal("0.00")) / len(amounts)).quantize(CENT)


def region_share(rows):
    """Return each region's share of total net revenue."""
    totals = aggregate_sales(rows)
    total = sum(totals.values(), Decimal("0.00"))
    if total == 0:
        return {}
    return {
        region: (amount / total).quantize(RATE_QUANTUM)
        for region, amount in totals.items()
    }
