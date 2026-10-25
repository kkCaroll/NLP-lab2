#!/usr/bin/env python3
"""Three sensitivity analyses for the main condition comparison.

Each scenario re-computes the pass rate by model and condition after removing
one class of episodes or restricting to one difficulty stratum. Rates are over
the full sample, so the branch subset and the reused round one rows are both
included, matching the descriptive table that the report quotes.

Scenarios are described by a filter, never by a re-definition of the outcome.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EPISODES = ROOT / "RECORD" / "tables" / "episode_level.csv"
OUTPUT = ROOT / "RECORD" / "analysis" / "deepening" / "sensitivity.csv"

CONDITIONS = ["pure_continue", "neutral", "method_guidance", "negative", "negative_guidance"]

SCENARIOS = [
    ("all", "全部样本", lambda row: True),
    ("drop_test_tampered", "排除测试篡改", lambda row: row["test_tampered"] == "False"),
    ("drop_budget", "排除预算耗尽", lambda row: row["budget_exhausted"] == "False"),
    ("standard", "仅标准题", lambda row: row["difficulty"] == "标准"),
    ("hard", "仅困难题", lambda row: row["difficulty"] == "困难"),
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episodes", default=str(EPISODES))
    parser.add_argument("--output", default=str(OUTPUT))
    args = parser.parse_args()

    with Path(args.episodes).open(encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))

    models = sorted({row["model"] for row in rows})
    labels = {model: model.split("/")[-1] for model in models}

    out_rows = []
    for name, description, keep in SCENARIOS:
        subset = [row for row in rows if keep(row)]
        for label, group in [
            *[(labels[m], [r for r in subset if r["model"] == m]) for m in models],
            ("pooled", subset),
        ]:
            for condition in CONDITIONS:
                cell = [r for r in group if r["condition"] == condition]
                passed = sum(1 for r in cell if r["all_passed"] == "True")
                rate = passed / len(cell) if cell else None
                out_rows.append(
                    {
                        "scenario": name,
                        "scenario_zh": description,
                        "model": label,
                        "condition": condition,
                        "n": len(cell),
                        "passed": passed,
                        "pass_rate": "" if rate is None else round(rate, 4),
                    }
                )

    print(f"{'scenario':20s} {'model':8s} {'condition':18s} {'n':>3s} {'pass':>4s} {'rate':>6s}")
    for row in out_rows:
        rate = row["pass_rate"]
        print(
            f"{row['scenario']:20s} {row['model']:8s} {row['condition']:18s} "
            f"{row['n']:3d} {row['passed']:4d} {rate if rate != '' else 'na':>6}"
        )

    print()
    print("pass rate range across conditions")
    for name, description, _ in SCENARIOS:
        for label in [*labels.values(), "pooled"]:
            rates = [
                row["pass_rate"]
                for row in out_rows
                if row["scenario"] == name and row["model"] == label and row["pass_rate"] != ""
            ]
            if len(rates) < 2:
                print(f"{name:20s} {label:8s} insufficient cells")
                continue
            spread = max(rates) - min(rates)
            print(f"{name:20s} {label:8s} min {min(rates):.3f} max {max(rates):.3f} spread {spread:.3f}")

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(out_rows[0].keys()))
        writer.writeheader()
        writer.writerows(out_rows)
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
