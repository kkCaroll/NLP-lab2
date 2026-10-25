#!/usr/bin/env python3
"""Exact McNemar power and minimum detectable effect for the paired design.

The paired unit is one model task combination that produced a branch in round
one, giving five conditions per unit. Two sided exact McNemar decides on the
discordant pairs only, so the power of a comparison depends on how many pairs
are discordant and how lopsided those pairs are.

For a fixed number of paired units and an assumed discordance rate, the script
finds the smallest split of discordant pairs that reaches the target power, and
converts it back to a risk difference in the full sample. Conditional power
computed from the observed effect is not reported, because it carries no
information about what the design would have detected.
"""

from __future__ import annotations

import argparse
import csv
from itertools import combinations
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EPISODES = ROOT / "RECORD" / "tables" / "episode_level.csv"
OUTPUT_CSV = ROOT / "RECORD" / "analysis" / "deepening" / "power_analysis.csv"

ALPHA = 0.05
TARGET_POWER = 0.80


def exact_p(b: int, n: int) -> float:
    if n == 0:
        return 1.0
    tail = sum(comb(n, k) for k in range(0, min(b, n - b) + 1))
    return min(1.0, 2 * tail / 2 ** n)


def rejection_region(n: int) -> int:
    """Largest b for which the lower tail still rejects at ALPHA."""
    t = -1
    for b in range(0, n // 2 + 1):
        if exact_p(b, n) < ALPHA:
            t = b
    return t


def power_at(p1: float, n: int) -> float:
    t = rejection_region(n)
    if t < 0:
        return 0.0
    total = 0.0
    for b in range(0, n + 1):
        if b <= t or b >= n - t:
            total += comb(n, b) * p1 ** b * (1 - p1) ** (n - b)
    return total


def mde_split(n: int) -> tuple[float, float] | None:
    """Smallest p1 above one half reaching TARGET_POWER, and that power."""
    if rejection_region(n) < 0:
        return None
    step = 0.0005
    p1 = 0.5
    while p1 <= 1.0:
        value = power_at(p1, n)
        if value >= TARGET_POWER:
            return p1, value
        p1 += step
    return None


def load_units(path: Path, model: str | None) -> dict[tuple[str, str], dict[str, bool]]:
    """Keep only units whose five conditions all ran fresh.

    A unit that passed in round one carries its round one state into later
    conditions, so those rows are not five independent measurements. Only the
    units that produced a branch supply a genuine repeated measures structure.
    """
    grouped: dict[tuple[str, str], list[dict]] = {}
    with path.open(encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            if model and row["model"] != model:
                continue
            key = (row["model"], row["task"])
            grouped.setdefault(key, []).append(row)

    units: dict[tuple[str, str], dict[str, bool]] = {}
    for key, rows in grouped.items():
        if any(row["reused_round1"] == "True" for row in rows):
            continue
        units[key] = {row["condition"]: row["all_passed"] == "True" for row in rows}
    return units


def paired_counts(units: dict, first: str, second: str) -> tuple[int, int, int]:
    only_first = only_second = both = 0
    for conditions in units.values():
        if first not in conditions or second not in conditions:
            continue
        left, right = conditions[first], conditions[second]
        if left and right:
            both += 1
        elif left:
            only_first += 1
        elif right:
            only_second += 1
    return only_first, only_second, both


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episodes", default=str(EPISODES))
    parser.add_argument("--output", default=str(OUTPUT_CSV))
    args = parser.parse_args()

    path = Path(args.episodes)
    models = sorted({row["model"] for row in csv.DictReader(path.open(encoding="utf-8-sig"))})
    conditions = ["pure_continue", "neutral", "method_guidance", "negative", "negative_guidance"]
    pairs = list(combinations(conditions, 2))

    pooled = load_units(path, None)
    per_model = {model: load_units(path, model) for model in models}

    print(f"pooled paired units {len(pooled)}")
    for model in models:
        print(f"  {model} {len(per_model[model])}")

    rows = []
    print()
    print("observed discordant structure")
    print(f"{'model':14s} {'pair':46s} {'N':>3s} {'b':>3s} {'c':>3s} {'rd':>7s} {'p':>7s}")
    for label, units in [
        ("pooled", pooled),
        *[(model.split("/")[-1], per_model[model]) for model in models],
    ]:
        for first, second in pairs:
            b, c, _ = paired_counts(units, first, second)
            n = len(units)
            n_disc = b + c
            p = exact_p(b, n_disc)
            rd = (b - c) / n if n else 0.0
            name = f"{first} vs {second}"
            print(f"{label:14s} {name:46s} {n:3d} {b:3d} {c:3d} {rd:7.3f} {p:7.4f}")
            rows.append(
                {
                    "model": label,
                    "comparison": name,
                    "n_units": n,
                    "discordant": n_disc,
                    "only_first": b,
                    "only_second": c,
                    "risk_difference": round(rd, 4),
                    "exact_p": round(p, 4),
                }
            )

    print()
    print("minimum detectable risk difference at 80 percent power")
    print(f"{'N':>3s} {'discordance':>11s} {'n_disc':>6s} {'p1_min':>7s} {'MDE rd':>7s}")
    grid = []
    for n_units in sorted({len(pooled), *[len(per_model[m]) for m in models]}):
        for rate in (0.20, 0.30, 0.40, 0.50, 0.60, 0.70):
            n_disc = round(n_units * rate)
            result = mde_split(n_disc)
            if result is None:
                print(f"{n_units:3d} {rate:11.2f} {n_disc:6d} {'none':>7s} {'none':>7s}")
                grid.append(
                    {
                        "n_units": n_units,
                        "assumed_discordance": rate,
                        "n_discordant": n_disc,
                        "p1_min": "",
                        "mde_risk_difference": "",
                        "achieved_power": "",
                    }
                )
                continue
            p1, achieved = result
            delta = (2 * p1 - 1) * n_disc / n_units
            print(f"{n_units:3d} {rate:11.2f} {n_disc:6d} {p1:7.3f} {delta:7.3f}")
            grid.append(
                {
                    "n_units": n_units,
                    "assumed_discordance": rate,
                    "n_discordant": n_disc,
                    "p1_min": p1,
                    "mde_risk_difference": round(delta, 4),
                    "achieved_power": round(achieved, 4),
                }
            )

    print()
    print("paired units required to detect a given risk difference")
    print(f"{'target rd':>9s} {'discordance':>11s} {'n_disc':>6s} {'units':>6s}")
    required = []
    for target in (0.10, 0.15, 0.20, 0.30):
        for rate in (0.30, 0.40, 0.50):
            found = ""
            for n_units in range(4, 401):
                n_disc = round(n_units * rate)
                result = mde_split(n_disc)
                if result is None:
                    continue
                p1, _ = result
                if (2 * p1 - 1) * n_disc / n_units <= target:
                    found = n_units
                    break
            print(f"{target:9.2f} {rate:11.2f} {'':>6s} {str(found):>6s}")
            required.append(
                {
                    "target_risk_difference": target,
                    "assumed_discordance": rate,
                    "required_units": found,
                }
            )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "model", "comparison", "n_units", "discordant", "only_first",
                "only_second", "risk_difference", "exact_p",
            ],
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(rows)

    grid_path = output.with_name(output.stem + "_grid.csv")
    with grid_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(grid[0].keys()))
        writer.writeheader()
        writer.writerows(grid)

    required_path = output.with_name(output.stem + "_required.csv")
    with required_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(required[0].keys()))
        writer.writeheader()
        writer.writerows(required)

    print(f"wrote {output}")
    print(f"wrote {grid_path}")
    print(f"wrote {required_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
