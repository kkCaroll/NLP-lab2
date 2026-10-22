#!/usr/bin/env python3
"""Agreement between two coding sheets over the nine qualitative codes.

Reports raw agreement, expected agreement and Cohen kappa for each code, then
pools all judgements for an overall figure. Codes whose two raters show no
variance in the compared subset have an undefined kappa and are reported as
such, since expected agreement equals one and the denominator vanishes.

Works for both the inter-coder comparison and the within-coder recoding.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path

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

VALUES = ("是", "否", "不适用", "不确定")


def load(path: Path) -> dict[str, dict[str, str]]:
    with path.open(encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    return {row["sample_id"].strip(): row for row in rows}


def kappa(pairs: list[tuple[str, str]]) -> tuple[float, float, float | None]:
    n = len(pairs)
    if n == 0:
        return 0.0, 0.0, None
    agree = sum(1 for left, right in pairs if left == right)
    po = agree / n
    first = Counter(left for left, _ in pairs)
    second = Counter(right for _, right in pairs)
    pe = sum(first[value] * second[value] for value in VALUES) / (n * n)
    if pe >= 1.0:
        return po, pe, None
    return po, pe, (po - pe) / (1.0 - pe)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("first", help="first coding sheet, CSV")
    parser.add_argument("second", help="second coding sheet, CSV")
    parser.add_argument("--label-first", default="first")
    parser.add_argument("--label-second", default="second")
    parser.add_argument("--output", help="optional CSV for the per code table")
    args = parser.parse_args()

    first = load(Path(args.first))
    second = load(Path(args.second))
    shared = sorted(set(first) & set(second))

    print(f"first {len(first)} rows, second {len(second)} rows, shared {len(shared)}")
    for name in sorted(set(first) ^ set(second)):
        print(f"  unpaired sample {name}")

    lines = []
    pooled: list[tuple[str, str]] = []
    print()
    print(f"{'code':22s} {'n':>3s} {'agree':>5s} {'po':>6s} {'pe':>6s} {'kappa':>7s}")
    for code in CODES:
        pairs = [
            (first[sample][code].strip(), second[sample][code].strip())
            for sample in shared
            if first[sample].get(code) and second[sample].get(code)
        ]
        pooled.extend(pairs)
        po, pe, value = kappa(pairs)
        agree = sum(1 for left, right in pairs if left == right)
        shown = "na" if value is None else f"{value:.3f}"
        print(f"{code:22s} {len(pairs):3d} {agree:5d} {po:6.3f} {pe:6.3f} {shown:>7s}")
        lines.append(
            {
                "code": code,
                "n": len(pairs),
                "agree": agree,
                "po": round(po, 4),
                "pe": round(pe, 4),
                "kappa": "" if value is None else round(value, 4),
                "disagreements": ";".join(
                    sample
                    for sample in shared
                    if first[sample][code].strip() != second[sample][code].strip()
                ),
            }
        )

    po, pe, value = kappa(pooled)
    agree = sum(1 for left, right in pooled if left == right)
    shown = "na" if value is None else f"{value:.3f}"
    print()
    print(
        f"pooled {len(pooled)} judgements, agree {agree}, "
        f"po {po:.3f}, pe {pe:.3f}, kappa {shown}"
    )
    lines.append(
        {
            "code": "pooled",
            "n": len(pooled),
            "agree": agree,
            "po": round(po, 4),
            "pe": round(pe, 4),
            "kappa": "" if value is None else round(value, 4),
            "disagreements": "",
        }
    )

    if args.output:
        output = Path(args.output)
        with output.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=["code", "n", "agree", "po", "pe", "kappa", "disagreements"],
            )
            writer.writeheader()
            writer.writerows(lines)
        print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
