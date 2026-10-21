"""Dictionary and text reports for employee records."""

from __future__ import annotations

from .grouping import department_summary
from .records import normalize_records
from .sorting import sort_records


def summary(records):
    """Return count, oldest, youngest and average age."""
    normalized = normalize_records(records)
    if not normalized:
        return {
            "count": 0,
            "oldest": None,
            "youngest": None,
            "average_age": 0,
        }
    ages = [record["age"] for record in normalized]
    oldest = max(normalized, key=lambda record: record["age"])
    youngest = min(normalized, key=lambda record: record["age"])
    return {
        "count": len(normalized),
        "oldest": oldest["name"],
        "youngest": youngest["name"],
        "average_age": round(sum(ages) / len(ages), 2),
    }


def name_list(records):
    """Return names in display order."""
    return [record["name"] for record in sort_records(records)]


def format_names(records, separator=", "):
    """Return names in display order joined by a separator."""
    return separator.join(name_list(records))


def department_lines(records):
    """Return one text line per department summary row."""
    return [
        f'{row["department"]}: {row["count"]} people, average {row["average_age"]}'
        for row in department_summary(records)
    ]


def format_table(records):
    """Return a tab separated table in display order."""
    rows = ["name\tage\tdepartment"]
    for record in sort_records(records):
        rows.append(
            f'{record["name"]}\t{record["age"]}\t{record["department"]}'
        )
    return "\n".join(rows)
