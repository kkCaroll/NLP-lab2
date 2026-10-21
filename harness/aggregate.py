#!/usr/bin/env python3
"""Aggregate episode records into task level and condition level tables.

Round 1 passing tasks never enter a feedback branch. Their round 1 final
state is reused for all five conditions, as specified in the experiment
plan. A missing branch is reported as missing and excluded from that
condition's denominators instead of being counted as a repair failure.
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "RECORD" / "runs"
TABLES = ROOT / "RECORD" / "tables"
CONDITIONS = [
    "pure_continue",
    "neutral",
    "method_guidance",
    "negative",
    "negative_guidance",
]


def model_slug(model: str) -> str:
    return model.replace("/", "_").replace(":", "_")


def load_json(path: Path) -> dict | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def quantile(values: list[float], fraction: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * fraction
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def distribution(values: list[float]) -> dict:
    if not values:
        return {"mean": None, "median": None, "iqr": None, "min": None, "max": None}
    return {
        "mean": round(statistics.mean(values), 4),
        "median": round(statistics.median(values), 4),
        "iqr": round(quantile(values, 0.75) - quantile(values, 0.25), 4),
        "min": round(min(values), 4),
        "max": round(max(values), 4),
    }


def regression_failures(episode: dict, meta: dict) -> int:
    failed = set(episode.get("regression_failed", []))
    missing = set(episode.get("missing_tests", []))
    regressions = set(meta.get("regression_tests", []))
    return len(failed | (missing & regressions))


def final_episode(summary: dict, condition: str) -> tuple[dict | None, bool]:
    round1 = summary.get("round1") or {}
    if round1.get("all_passed"):
        return round1, True
    return summary.get("branches", {}).get(condition), False


def task_row(
    run_id: str,
    model: str,
    task: str,
    meta: dict,
    summary: dict,
    condition: str,
) -> dict:
    episode, reused = final_episode(summary, condition)
    row = {
        "run_id": run_id,
        "model": model,
        "task": task,
        "difficulty": meta.get("difficulty"),
        "category": meta.get("category"),
        "condition": condition,
        "reused_round1": reused,
        "round1_passed": bool((summary.get("round1") or {}).get("all_passed")),
        "valid": episode is not None,
    }
    if episode is None:
        row.update(
            {
                "all_passed": None,
                "target_failed": None,
                "regression_failed": None,
                "edit_lines": None,
                "delta_lines": None,
                "edit_file_count": None,
                "edit_ratio": None,
                "over_edit": None,
                "unrelated_file": None,
                "test_tampered": None,
                "budget_exhausted": None,
                "timed_out": None,
                "tool_calls": None,
                "duration_s": None,
                "round1_lines": None,
                "revert": None,
                "any_edit": None,
                "no_edit": None,
                "no_edit_failure": None,
                "effective_tool_calls": None,
                "denied_tool_calls": None,
                "denied_bash_calls": None,
                "error_tool_calls": None,
                "first_edit_after_read": None,
            }
        )
        return row
    row.update(
        {
            "all_passed": bool(episode.get("all_passed")),
            "target_failed": len(episode.get("target_failed", [])),
            "regression_failed": regression_failures(episode, meta),
            "edit_lines": episode.get("edit_lines"),
            "delta_lines": episode.get("delta_lines"),
            "edit_file_count": episode.get("edit_file_count"),
            "edit_ratio": episode.get("edit_ratio"),
            "over_edit": episode.get("over_edit"),
            "unrelated_file": episode.get("unrelated_file"),
            "test_tampered": episode.get("test_tampered"),
            "budget_exhausted": episode.get("budget_exhausted"),
            "timed_out": episode.get("timed_out"),
            "tool_calls": episode.get("tool_calls"),
            "duration_s": episode.get("duration_s"),
            "round1_lines": episode.get("round1_lines"),
            "revert": episode.get("revert"),
            "any_edit": episode.get("any_edit"),
            "no_edit": episode.get("no_edit"),
            "no_edit_failure": episode.get("no_edit_failure"),
            "effective_tool_calls": episode.get("effective_tool_calls"),
            "denied_tool_calls": episode.get("denied_tool_calls"),
            "denied_bash_calls": episode.get("denied_bash_calls"),
            "error_tool_calls": episode.get("error_tool_calls"),
            "first_edit_after_read": episode.get("first_edit_after_read"),
        }
    )
    row["repair_success"] = bool(
        not reused and not row["round1_passed"] and row["all_passed"]
    )
    return row


def condition_summary(rows: list[dict], meta_by_task: dict) -> dict:
    valid = [row for row in rows if row["valid"]]
    round1_pass = sum(1 for row in valid if row["round1_passed"])
    repair = sum(1 for row in valid if row.get("repair_success"))
    failures = sum(1 for row in valid if not row["round1_passed"])
    regression_tests = sum(
        len(meta_by_task[row["task"]].get("regression_tests", []))
        for row in valid
    )
    regression_failed = sum(row["regression_failed"] or 0 for row in valid)
    edit_sizes = [row["edit_lines"] for row in valid if row["edit_lines"] is not None]
    edit_ratios = [
        row["edit_ratio"] for row in valid if row["edit_ratio"] is not None
    ]
    deltas = [row["delta_lines"] for row in valid if row["delta_lines"] is not None]
    return {
        "n_valid": len(valid),
        "n_missing": len(rows) - len(valid),
        "round1_passed": round1_pass,
        "round1_failed": failures,
        "repaired": repair,
        "pass_rate": round((round1_pass + repair) / len(valid), 4) if valid else None,
        "repair_success": round(repair / failures, 4) if failures else None,
        "regression_rate": (
            round(regression_failed / regression_tests, 4)
            if regression_tests
            else None
        ),
        "regression_failed": regression_failed,
        "regression_tests": regression_tests,
        "edit_size": distribution(edit_sizes),
        "edit_ratio": distribution(edit_ratios),
        "delta_lines": distribution(deltas),
        "edit_files": distribution(
            [row["edit_file_count"] for row in valid if row["edit_file_count"] is not None]
        ),
        "over_edit_rate": (
            round(sum(1 for row in valid if row["over_edit"]) / len(valid), 4)
            if valid
            else None
        ),
        "unrelated_file_rate": (
            round(sum(1 for row in valid if row["unrelated_file"]) / len(valid), 4)
            if valid
            else None
        ),
        "test_tamper_rate": (
            round(sum(1 for row in valid if row["test_tampered"]) / len(valid), 4)
            if valid
            else None
        ),
        "budget_exhausted_rate": (
            round(sum(1 for row in valid if row["budget_exhausted"]) / len(valid), 4)
            if valid
            else None
        ),
        "timeout_rate": (
            round(sum(1 for row in valid if row["timed_out"]) / len(valid), 4)
            if valid
            else None
        ),
        "any_edit_rate": (
            round(sum(1 for row in valid if row.get("any_edit")) / len(valid), 4)
            if valid
            else None
        ),
        "no_edit_rate": (
            round(sum(1 for row in valid if row.get("no_edit")) / len(valid), 4)
            if valid
            else None
        ),
        "no_edit_failure_rate": (
            round(
                sum(1 for row in valid if row.get("no_edit_failure")) / len(valid),
                4,
            )
            if valid
            else None
        ),
        "revert_rate": (
            round(sum(1 for row in valid if row.get("revert")) / len(valid), 4)
            if valid
            else None
        ),
        "effective_tool_calls": distribution(
            [
                row["effective_tool_calls"]
                for row in valid
                if row.get("effective_tool_calls") is not None
            ]
        ),
        "denied_bash_calls": sum(
            row["denied_bash_calls"] or 0
            for row in valid
            if row.get("denied_bash_calls") is not None
        ),
        "error_tool_calls": sum(
            row["error_tool_calls"] or 0
            for row in valid
            if row.get("error_tool_calls") is not None
        ),
    }


def markdown_table(summary: dict) -> str:
    lines = [
        "| 模型 | 条件 | 有效题数 | 第一轮通过 | 修复成功 | PassRate | RepairSuccess | RegressionRate | EditSize 中位数 | EditRatio 中位数 | OverEditRate |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for model, conditions in summary.items():
        for condition in CONDITIONS:
            item = conditions.get(condition, {})
            lines.append(
                f"| {model} | {condition} | {item.get('n_valid', 0)} | "
                f"{item.get('round1_passed', 0)} | {item.get('repaired', 0)} | "
                f"{fmt(item.get('pass_rate'))} | {fmt(item.get('repair_success'))} | "
                f"{fmt(item.get('regression_rate'))} | "
                f"{fmt((item.get('edit_size') or {}).get('median'))} | "
                f"{fmt((item.get('edit_ratio') or {}).get('median'))} | "
                f"{fmt(item.get('over_edit_rate'))} |"
            )
    return "\n".join(lines)


def fmt(value) -> str:
    if value is None:
        return "NA"
    return f"{value:.3f}" if isinstance(value, float) else str(value)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--output", default=str(TABLES))
    args = parser.parse_args()

    run_root = RUNS / args.run_id
    manifest = load_json(run_root / "batch_manifest.json") or {}
    models = manifest.get("models") or []
    if not models:
        models = sorted(
            path.name
            for path in run_root.iterdir()
            if path.is_dir() and path.name.startswith("opencode_")
        )
    tasks = manifest.get("tasks") or sorted(
        path.name
        for path in (ROOT / "tasks").iterdir()
        if path.is_dir() and path.name.startswith("T")
    )

    rows = []
    meta_by_task = {}
    missing_tasks = []
    for model in models:
        for task in tasks:
            meta_path = ROOT / "tasks" / task / "meta.json"
            meta = load_json(meta_path)
            if meta is None:
                missing_tasks.append(f"{task}: meta missing")
                continue
            meta_by_task[task] = meta
            summary = load_json(
                run_root / model_slug(model) / task / "task_summary.json"
            )
            if summary is None:
                missing_tasks.append(f"{task}: summary missing for {model}")
                rows_for_task = [
                    {
                        "run_id": args.run_id,
                        "model": model,
                        "task": task,
                        "difficulty": meta.get("difficulty"),
                        "category": meta.get("category"),
                        "condition": condition,
                        "reused_round1": False,
                        "round1_passed": None,
                        "valid": False,
                        "all_passed": None,
                        "target_failed": None,
                        "regression_failed": None,
                        "edit_lines": None,
                        "delta_lines": None,
                        "edit_file_count": None,
                        "edit_ratio": None,
                        "over_edit": None,
                        "unrelated_file": None,
                        "test_tampered": None,
                        "budget_exhausted": None,
                        "timed_out": None,
                        "tool_calls": None,
                        "duration_s": None,
                        "round1_lines": None,
                        "revert": None,
                        "any_edit": None,
                        "no_edit": None,
                        "no_edit_failure": None,
                        "effective_tool_calls": None,
                        "denied_tool_calls": None,
                        "denied_bash_calls": None,
                        "error_tool_calls": None,
                        "first_edit_after_read": None,
                        "repair_success": None,
                    }
                    for condition in CONDITIONS
                ]
                rows.extend(rows_for_task)
                continue
            for condition in CONDITIONS:
                rows.append(
                    task_row(args.run_id, model, task, meta, summary, condition)
                )

    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with (output / "episode_level.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    summary = {}
    for model in models:
        model_rows = [row for row in rows if row["model"] == model]
        summary[model] = {
            condition: condition_summary(
                [row for row in model_rows if row["condition"] == condition],
                meta_by_task,
            )
            for condition in CONDITIONS
        }

    (output / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    branch_rows = [
        row for row in rows if row["valid"] and not row["reused_round1"]
    ]
    branch_summary = {
        model: {
            condition: condition_summary(
                [
                    row
                    for row in branch_rows
                    if row["model"] == model and row["condition"] == condition
                ],
                meta_by_task,
            )
            for condition in CONDITIONS
        }
        for model in models
    }
    (output / "summary_branch.json").write_text(
        json.dumps(branch_summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    markdown = [
        f"# 主实验聚合 {args.run_id}",
        "",
        f"有效任务记录 {len(rows)} 行，缺失 {len(missing_tasks)} 项。",
        "",
        markdown_table(summary),
        "",
        "## 分支子集",
        "",
        "第一轮失败任务的第二轮分支，不含第一轮通过任务在五条件中复用的终态。",
        "",
        markdown_table(branch_summary),
        "",
    ]
    if missing_tasks:
        markdown.append("## 缺失")
        markdown.append("")
        markdown.extend(f"- {item}" for item in missing_tasks)
        markdown.append("")
    (output / "summary.md").write_text(
        "\n".join(markdown), encoding="utf-8", newline="\n"
    )
    print(
        f"wrote {output / 'episode_level.csv'}, {output / 'summary.json'}, "
        f"{output / 'summary_branch.json'}, {output / 'summary.md'}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
