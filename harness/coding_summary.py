#!/usr/bin/env python3
"""Join the coding sheet with the blinding manifest and tabulate the codes.

The manifest is only opened here, after coding is complete, so that condition
and model never entered the coding decisions. Groupings are reported at three
levels: overall, by model, by condition, and by outcome. Cells are small, so
the output is descriptive only. No test is run and no interval is computed.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHEET = ROOT / "RECORD" / "analysis" / "deepening" / "coding_sheet.csv"
MANIFEST = ROOT / "RECORD" / "analysis" / "deepening" / "blinding_manifest.csv"
OUTPUT = ROOT / "RECORD" / "analysis" / "deepening" / "coding_summary.csv"

CODES = [
    "no_edit",
    "reads_log_first",
    "locates_callers",
    "only_target_lines",
    "rewrites_function",
    "unrelated_file",
    "defensive_branch",
    "reverted_previous",
    "claims_done_unverified",
]
VALUES = ["是", "否", "不适用", "不确定"]
CONDITIONS = ["pure_continue", "neutral", "method_guidance", "negative", "negative_guidance"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sheet", default=str(SHEET))
    parser.add_argument("--manifest", default=str(MANIFEST))
    parser.add_argument("--output", default=str(OUTPUT))
    args = parser.parse_args()

    with Path(args.manifest).open(encoding="utf-8-sig") as handle:
        manifest = {row["sample_id"]: row for row in csv.DictReader(handle)}
    with Path(args.sheet).open(encoding="utf-8-sig") as handle:
        sheet = list(csv.DictReader(handle))

    merged = []
    missing = []
    for row in sheet:
        meta = manifest.get(row["sample_id"])
        if not meta:
            missing.append(row["sample_id"])
            continue
        merged.append(
            {
                **row,
                "model": meta["model"].split("/")[-1],
                "condition": meta["condition"],
                "outcome": meta["outcome"],
            }
        )
    if missing:
        print(f"missing manifest rows for {missing}")

    groupings = [
        ("overall", "all", lambda row: "全部"),
        ("model", "model", lambda row: row["model"]),
        ("condition", "condition", lambda row: row["condition"]),
        ("outcome", "outcome", lambda row: row["outcome"]),
    ]

    rows_out = []
    for kind, _, key in groupings:
        groups = sorted({key(row) for row in merged})
        if kind == "condition":
            groups = [c for c in CONDITIONS if c in groups] + [
                g for g in groups if g not in CONDITIONS
            ]
        for group in groups:
            cell = [row for row in merged if key(row) == group]
            edited = sum(1 for row in cell if row["no_edit"] == "否")
            for code in CODES:
                counts = Counter(row[code] for row in cell)
                applicable = len(cell) - counts.get("不适用", 0)
                for value in VALUES:
                    count = counts.get(value, 0)
                    if count == 0:
                        continue
                    rows_out.append(
                        {
                            "grouping": kind,
                            "group": group,
                            "n_episodes": len(cell),
                            "n_edited": edited,
                            "code": code,
                            "value": value,
                            "count": count,
                            "share_of_episodes": round(count / len(cell), 4),
                            "share_of_applicable": (
                                round(count / applicable, 4) if applicable else ""
                            ),
                        }
                    )

    for kind in [k for k, _, _ in groupings]:
        print(f"=== {kind} ===")
        subset = [row for row in rows_out if row["grouping"] == kind]
        for row in subset:
            if row["value"] == "是":
                print(
                    f"{row['group']:30s} {row['code']:22s} 是 {row['count']:2d}/"
                    f"{row['n_episodes']:2d} applicable {row['share_of_applicable']}"
                )
        print()

    output = Path(args.output)
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows_out[0].keys()))
        writer.writeheader()
        writer.writerows(rows_out)
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
