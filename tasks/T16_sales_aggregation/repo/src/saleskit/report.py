"""Text and dictionary reports for sales records."""

from .aggregate import aggregate_sales, top_region, total_revenue
from .money import format_amount


def summary_lines(rows):
    """Return one line per region followed by a total line."""
    totals = aggregate_sales(rows)
    lines = [
        f"{region}: {format_amount(amount)}"
        for region, amount in totals.items()
    ]
    lines.append(f"total: {format_amount(total_revenue(rows))}")
    return lines


def sales_report(rows):
    """Return a dictionary report with regional and total revenue."""
    totals = aggregate_sales(rows)
    return {
        "by_region": totals,
        "total": total_revenue(rows),
        "top_region": top_region(rows),
        "lines": summary_lines(rows),
    }
