#!/usr/bin/env python3
"""Build a deterministic qualitative sample and an empty coding sheet.

Two successful and two failed branch episodes are selected per model and
condition. When fewer than two are available, all are selected. The sheet keeps
artifact paths so every code can be traced back to the diff, prompt and event
stream.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "RECORD" / "runs"
CONDITIONS = [
    "pure_continue",
    "neutral",
    "method_guidance",
    "negative",
    "negative_guidance",
]
CODING_FIELDS = [
    "reads_log_first",
    "locates_callers",
    "only_target_lines",
    "rewrites_function",
    "unrelated_file",
    "defensive_branch",
    "reverted_previous",
    "claims_done_unverified",
    "notes",
]


def model_slug(model: str) -> str:
    return model.replace("/", "_").replace(":", "_")


def select(group: pd.DataFrame, outcome: bool, limit: int = 2) -> list[dict]:
    subset = group[group["all_passed"] == outcome].sort_values("task")
    return subset.head(limit).to_dict("records")


def repo_path(path: Path) -> str:
    """Return a repository-relative POSIX path for portable traceability."""
    return path.relative_to(ROOT).as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default="2026-10-21_main")
    parser.add_argument(
        "--episodes",
        default=str(ROOT / "RECORD" / "tables" / "episode_level.csv"),
    )
    parser.add_argument(
        "--output",
        default=str(ROOT / "RECORD" / "analysis" / "qualitative"),
    )
    args = parser.parse_args()
    frame = pd.read_csv(args.episodes)
    branch = frame[
        (frame["valid"] == True)  # noqa: E712
        & (frame["round1_passed"] == False)  # noqa: E712
    ]
    rows = []
    for model in sorted(branch["model"].unique()):
        for condition in CONDITIONS:
            group = branch[
                (branch["model"] == model) & (branch["condition"] == condition)
            ]
            for outcome, label in ((True, "success"), (False, "failure")):
                for record in select(group, outcome):
                    episode_dir = (
                        RUNS
                        / args.run_id
                        / model_slug(model)
                        / record["task"]
                        / "branches"
                        / condition
                    )
                    rows.append(
                        {
                            "model": model,
                            "task": record["task"],
                            "condition": condition,
                            "outcome": label,
                            "edit_lines": record["edit_lines"],
                            "edit_ratio": record["edit_ratio"],
                            "diff_path": repo_path(
                                episode_dir / "diff_cumulative.patch"
                            ),
                            "events_path": repo_path(episode_dir / "events.jsonl"),
                            "prompt_path": repo_path(episode_dir / "prompt.txt"),
                            "summary_path": repo_path(episode_dir / "summary.json"),
                        }
                    )
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    with (output / "qualitative_samples.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    coding_rows = [
        {**row, **{field: "" for field in CODING_FIELDS}} for row in rows
    ]
    with (output / "qualitative_coding.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(coding_rows[0].keys()))
        writer.writeheader()
        writer.writerows(coding_rows)
    print(f"wrote {len(rows)} samples to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
