#!/usr/bin/env python3
"""Pair the two budget arms of the branch rerun and report paired statistics.

Reads RECORD/runs/<run-id>/results.csv and writes a per case table with the
budget 15 and budget 30 outcomes side by side. The exact McNemar test is used
because the two arms observe the same cases.
"""

from __future__ import annotations

import argparse
import csv
import random
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUN = ROOT / "RECORD" / "runs" / "2026-10-22_budget_rerun"
DEFAULT_OUTPUT = ROOT / "RECORD" / "analysis" / "deepening" / "budget_rerun.csv"

FIELDS = [
    "task",
    "condition",
    "baseline_budget",
    "high_budget",
    "baseline_pass",
    "high_pass",
    "baseline_tools",
    "baseline_denied",
    "baseline_edits",
    "baseline_exhausted",
    "baseline_over_edit",
    "high_tools",
    "high_denied",
    "high_edits",
    "high_exhausted",
    "high_over_edit",
    "pattern",
]


def load_rows(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def over_edit(run_root: Path, row: dict) -> str:
    summary = (
        run_root
        / row["model"].replace("/", "_")
        / row["task"]
        / "branches"
        / row["condition"]
        / f"budget_{row['budget']}"
        / "summary.json"
    )
    if not summary.is_file():
        return ""
    import json

    data = json.loads(summary.read_text(encoding="utf-8"))
    return str(bool(data.get("over_edit")))


def exact_mcnemar(b: int, c: int) -> float:
    if b + c == 0:
        return 1.0
    tail = sum(comb(b + c, k) for k in range(0, min(b, c) + 1))
    return min(1.0, 2 * tail / 2 ** (b + c))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", default=str(DEFAULT_RUN))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--low", default="15")
    parser.add_argument("--high", default="30")
    parser.add_argument("--seed", default="20261022")
    args = parser.parse_args()

    run_root = Path(args.run)
    rows = load_rows(run_root / "results.csv")
    low = {row["task"] + "|" + row["condition"]: row for row in rows
           if row["budget"] == args.low}
    high = {row["task"] + "|" + row["condition"]: row for row in rows
            if row["budget"] == args.high}
    keys = sorted(set(low) & set(high))
    if len(keys) != len(low) or len(keys) != len(high):
        raise SystemExit("arms do not cover the same cases")

    out = []
    for key in keys:
        a, b = low[key], high[key]
        low_pass = a["all_passed"] == "True"
        high_pass = b["all_passed"] == "True"
        if low_pass and high_pass:
            pattern = "both_pass"
        elif not low_pass and high_pass:
            pattern = "high_only_pass"
        elif low_pass and not high_pass:
            pattern = "low_only_pass"
        else:
            pattern = "both_fail"
        out.append(
            {
                "task": a["task"],
                "condition": a["condition"],
                "baseline_budget": args.low,
                "high_budget": args.high,
                "baseline_pass": low_pass,
                "high_pass": high_pass,
                "baseline_tools": a["tool_calls"],
                "baseline_denied": a["denied_tool_calls"],
                "baseline_edits": a["edits"],
                "baseline_exhausted": a["budget_exhausted"],
                "baseline_over_edit": over_edit(run_root, a),
                "high_tools": b["tool_calls"],
                "high_denied": b["denied_tool_calls"],
                "high_edits": b["edits"],
                "high_exhausted": b["budget_exhausted"],
                "high_over_edit": over_edit(run_root, b),
                "pattern": pattern,
            }
        )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(out)

    n = len(out)
    low_pass = sum(1 for row in out if row["baseline_pass"])
    high_pass = sum(1 for row in out if row["high_pass"])
    b = sum(1 for row in out if row["pattern"] == "high_only_pass")
    c = sum(1 for row in out if row["pattern"] == "low_only_pass")

    rng = random.Random(int(args.seed))
    pairs = [(row["baseline_pass"], row["high_pass"]) for row in out]
    diffs = []
    for _ in range(10000):
        sample = [pairs[rng.randrange(n)] for _ in range(n)]
        diffs.append(
            sum(1 for _, y in sample if y) / n - sum(1 for x, _ in sample if x) / n
        )
    diffs.sort()

    print(f"cases {n}")
    print(f"budget {args.low}: {low_pass}/{n}")
    print(f"budget {args.high}: {high_pass}/{n}")
    print(f"discordant high only {b}, low only {c}")
    print(f"exact McNemar p {exact_mcnemar(b, c):.5f}")
    print(
        f"risk difference {high_pass / n - low_pass / n:.3f} "
        f"bootstrap 95% CI {diffs[249]:.3f} to {diffs[9749]:.3f}"
    )
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
