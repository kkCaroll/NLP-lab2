"""Regional aggregation for sales and refund records."""

from collections import defaultdict
from decimal import Decimal

from .money import CENT
from .records import normalize_records


def aggregate_sales(rows):
    """Return net revenue by region, sorted by region name."""
    totals = defaultdict(lambda: Decimal("0.00"))
    for record in normalize_records(rows):
        amount = record["amount"]
        if record["kind"] == "sale":
            totals[record["region"]] += amount
        else:
            totals[record["region"]] += amount
    return {
        region: total.quantize(CENT)
        for region, total in sorted(totals.items())
    }


def total_revenue(rows):
    """Return total net revenue across all regions."""
    return sum(aggregate_sales(rows).values(), Decimal("0.00")).quantize(CENT)


def top_region(rows):
    """Return the region with the largest net revenue, or None for no rows."""
    totals = aggregate_sales(rows)
    if not totals:
        return None
    return max(totals.items(), key=lambda item: (item[1], item[0]))[0]
