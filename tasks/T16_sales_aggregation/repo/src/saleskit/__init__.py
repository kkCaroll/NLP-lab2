"""Utilities for sales records and revenue reports."""

from .aggregate import aggregate_sales, top_region, total_revenue
from .filters import filter_region, refunds_only, sales_only, sort_records
from .metrics import average_sale, refund_rate, region_share
from .money import format_amount, sum_amounts, to_amount
from .records import normalize_record, normalize_records
from .report import sales_report, summary_lines

__all__ = [
    "aggregate_sales",
    "average_sale",
    "filter_region",
    "format_amount",
    "normalize_record",
    "normalize_records",
    "refund_rate",
    "refunds_only",
    "region_share",
    "sales_only",
    "sales_report",
    "sort_records",
    "sum_amounts",
    "summary_lines",
    "to_amount",
    "top_region",
    "total_revenue",
]

__version__ = "0.1.0"
