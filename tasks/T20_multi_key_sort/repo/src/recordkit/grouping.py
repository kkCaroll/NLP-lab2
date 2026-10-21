"""Grouping helpers and department summaries."""

from __future__ import annotations

from .keys import order_records
from .records import normalize_records


def group_by_department(records):
    """Return a mapping from department to records in input order."""
    groups = {}
    for record in normalize_records(records):
        groups.setdefault(record["department"], []).append(record)
    return groups


def department_age_order(records):
    """Return department names ordered by descending age then name."""
    groups = group_by_department(records)
    return {
        department: [record["name"] for record in members]
        for department, members in groups.items()
    }


def department_summary(records):
    """Return one summary row per department."""
    groups = group_by_department(records)
    rows = []
    for department in sorted(groups):
        members = groups[department]
        total = sum(record["age"] for record in members)
        rows.append(
            {
                "department": department,
                "count": len(members),
                "average_age": round(total / len(members), 2),
                "names": [record["name"] for record in members],
            }
        )
    return rows
