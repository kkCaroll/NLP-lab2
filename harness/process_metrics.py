#!/usr/bin/env python3
"""Recompute episode level process metrics from recorded event streams.

The script only reads an existing run directory. It does not call any model and
does not modify the recorded episodes. Tool call accounting is recomputed from
events.jsonl because the early summary files did not record denied calls.

A tool call that OpenCode rejects by permission rule still increments the
runner's tool call counter, so the nominal limit and the number of usable calls
are not the same quantity. denied_tool_calls records how many slots were lost
in this way. unused_budget records how many slots of the nominal limit were
never reached, which is only informative for episodes that were not cut off.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUN = ROOT / "RECORD" / "runs" / "2026-10-21_main"
DEFAULT_OUTPUT = ROOT / "RECORD" / "analysis" / "deepening" / "process_metrics.csv"

DENIAL_MARKER = "prevents you from using"
EDIT_TOOLS = {"edit", "write", "patch", "multiedit", "apply_patch"}
CONDITIONS = [
    "round1",
    "pure_continue",
    "neutral",
    "method_guidance",
    "negative",
    "negative_guidance",
]
LIMITS = {"round1": 10}

FIELDS = [
    "model",
    "task",
    "condition",
    "episode",
    "all_passed",
    "timed_out",
    "budget_exhausted",
    "tool_call_limit",
    "total_tool_calls",
    "denied_tool_calls",
    "denied_bash_calls",
    "effective_tool_calls",
    "unused_budget",
    "edits",
    "no_edit",
    "first_edit_index_total",
    "first_edit_index_effective",
    "reads_before_first_edit",
    "read_calls",
    "unique_files_read",
    "repeated_read_calls",
    "glob_calls",
    "grep_calls",
    "bash_attempts",
    "pytest_attempts",
    "pytest_attempts_after_edit",
    "last_tools",
    "last_tool_status",
    "outcome",
]


def read_events(path: Path) -> list[dict]:
    events = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return events


def tool_records(events: list[dict]) -> list[dict]:
    """Extract one record per tool_use event in order."""
    records = []
    for event in events:
        if event.get("type") != "tool_use":
            continue
        part = event.get("part", {})
        state = part.get("state", {})
        error = str(state.get("error", ""))
        records.append(
            {
                "tool": part.get("tool", ""),
                "status": state.get("status", ""),
                "denied": state.get("status") == "error"
                and DENIAL_MARKER in error,
                "input": state.get("input", {}) or {},
            }
        )
    return records


def command_text(record: dict) -> str:
    value = record["input"].get("command", "")
    return value if isinstance(value, str) else ""


def file_path(record: dict) -> str:
    value = record["input"].get("filePath", "")
    return value if isinstance(value, str) else ""


def summarize_episode(
    model: str, task: str, condition: str, summary: dict, events: list[dict]
) -> dict:
    records = tool_records(events)
    limit = LIMITS.get(condition, summary.get("limits", {}).get("round2_tool_calls", 15))
    total = len(records)
    denied = sum(1 for item in records if item["denied"])
    denied_bash = sum(
        1 for item in records if item["denied"] and item["tool"] == "bash"
    )
    effective = total - denied

    first_total = None
    first_effective = None
    denials_before = 0
    reads_before = 0
    files_read = []
    for index, item in enumerate(records, start=1):
        if item["denied"]:
            denials_before += 1
        if item["tool"] == "read":
            files_read.append(file_path(item))
            if first_total is None:
                reads_before += 1
        if item["tool"] in EDIT_TOOLS and first_total is None:
            first_total = index
            first_effective = index - denials_before

    edits = sum(1 for item in records if item["tool"] in EDIT_TOOLS)
    pytest_attempts = sum(
        1 for item in records if "pytest" in command_text(item)
    )
    pytest_after = 0
    if first_total is not None:
        pytest_after = sum(
            1
            for item in records[first_total:]
            if "pytest" in command_text(item)
        )

    counts = Counter(item["tool"] for item in records)
    non_empty = [path for path in files_read if path]
    unique_files = len({Path(path).as_posix().lower() for path in non_empty})
    repeated = len(non_empty) - unique_files

    all_passed = bool(summary.get("all_passed"))
    budget = bool(summary.get("budget_exhausted"))
    if all_passed:
        outcome = "pass"
    elif budget:
        outcome = "budget_cutoff"
    else:
        outcome = "model_stop"

    return {
        "model": model,
        "task": task,
        "condition": condition,
        "episode": "round1" if condition == "round1" else "branch",
        "all_passed": all_passed,
        "timed_out": bool(summary.get("timed_out")),
        "budget_exhausted": budget,
        "tool_call_limit": limit,
        "total_tool_calls": total,
        "denied_tool_calls": denied,
        "denied_bash_calls": denied_bash,
        "effective_tool_calls": effective,
        "unused_budget": max(0, limit - total),
        "edits": edits,
        "no_edit": edits == 0,
        "first_edit_index_total": first_total if first_total is not None else "",
        "first_edit_index_effective": (
            first_effective if first_effective is not None else ""
        ),
        "reads_before_first_edit": reads_before,
        "read_calls": counts.get("read", 0),
        "unique_files_read": unique_files,
        "repeated_read_calls": repeated,
        "glob_calls": counts.get("glob", 0),
        "grep_calls": counts.get("grep", 0),
        "bash_attempts": counts.get("bash", 0),
        "pytest_attempts": pytest_attempts,
        "pytest_attempts_after_edit": pytest_after,
        "last_tools": "|".join(item["tool"] for item in records[-3:]),
        "last_tool_status": records[-1]["status"] if records else "",
        "outcome": outcome,
    }


def episodes(run_root: Path):
    for model_dir in sorted(run_root.iterdir()):
        if not model_dir.is_dir():
            continue
        model = model_dir.name.replace("opencode_", "")
        for task_dir in sorted(model_dir.iterdir()):
            if not task_dir.is_dir():
                continue
            candidates = [task_dir / "round1"]
            branch_root = task_dir / "branches"
            if branch_root.is_dir():
                candidates.extend(sorted(branch_root.iterdir()))
            for episode_dir in candidates:
                if not episode_dir.is_dir():
                    continue
                summary_path = episode_dir / "summary.json"
                events_path = episode_dir / "events.jsonl"
                if not summary_path.is_file() or not events_path.is_file():
                    continue
                condition = (
                    "round1" if episode_dir.name == "round1" else episode_dir.name
                )
                yield model, task_dir.name, condition, episode_dir


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", default=str(DEFAULT_RUN))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()

    run_root = Path(args.run)
    output = Path(args.output)
    rows = []
    for model, task, condition, episode_dir in episodes(run_root):
        summary = json.loads(
            (episode_dir / "summary.json").read_text(encoding="utf-8")
        )
        events = read_events(episode_dir / "events.jsonl")
        rows.append(summarize_episode(model, task, condition, summary, events))

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"episodes {len(rows)}")
    print("outcome", Counter(row["outcome"] for row in rows))
    for condition in CONDITIONS:
        subset = [row for row in rows if row["condition"] == condition]
        if not subset:
            continue
        print(
            f"{condition:18s} n={len(subset):3d} "
            f"pass={sum(1 for r in subset if r['all_passed']):3d} "
            f"no_edit={sum(1 for r in subset if r['no_edit']):3d} "
            f"denied={sum(r['denied_tool_calls'] for r in subset):3d} "
            f"unused_median={sorted(r['unused_budget'] for r in subset)[len(subset) // 2]}"
        )
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
