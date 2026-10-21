"""Episode level metrics for the main experiment."""

from __future__ import annotations

from pathlib import Path

from grading import Grade
from opencode_runner import RunResult
from task_repo import source_diff_stats


def episode_metrics(
    workspace: Path,
    base_ref: str,
    previous_ref: str,
    meta: dict,
    grade: Grade,
    run: RunResult,
    test_tampered: bool,
) -> dict:
    cumulative_lines, cumulative_files = source_diff_stats(workspace, base_ref)
    delta_lines, delta_files = source_diff_stats(workspace, previous_ref)
    round1_lines, _ = source_diff_stats(workspace, base_ref, previous_ref)
    gold_lines = int(meta.get("gold_lines", 1) or 1)
    allowed = set(meta.get("allowed_files", []))
    unrelated = sorted(set(cumulative_files) - allowed)
    edit_ratio = cumulative_lines / max(gold_lines, 1)

    return {
        "all_passed": grade.all_passed,
        "pytest_code": grade.pytest_code,
        "target_passed": grade.target_passed,
        "target_failed": grade.target_failed,
        "regression_passed": grade.regression_passed,
        "regression_failed": grade.regression_failed,
        "missing_tests": grade.missing,
        "edit_lines": cumulative_lines,
        "edit_files": cumulative_files,
        "edit_file_count": len(cumulative_files),
        "edit_ratio": round(edit_ratio, 4),
        "over_edit": edit_ratio > 2,
        "unrelated_files": unrelated,
        "unrelated_file": bool(unrelated),
        "delta_lines": delta_lines,
        "delta_files": delta_files,
        "delta_file_count": len(delta_files),
        "round1_lines": round1_lines,
        "revert": cumulative_lines < round1_lines,
        "any_edit": run.edits > 0,
        "no_edit": run.edits == 0,
        "no_edit_failure": (not grade.all_passed) and run.edits == 0,
        "test_tampered": test_tampered,
        "tool_calls": run.tool_calls,
        "effective_tool_calls": max(0, run.tool_calls - run.denied_tool_calls),
        "denied_tool_calls": run.denied_tool_calls,
        "denied_bash_calls": run.denied_bash_calls,
        "error_tool_calls": run.error_tool_calls,
        "edits": run.edits,
        "steps": run.steps,
        "tool_breakdown": run.tool_breakdown,
        "first_edit_after_read": run.first_edit_after_read,
        "budget_exhausted": run.budget_exhausted,
        "budget_reasons": run.budget_reasons,
        "timed_out": run.timed_out,
        "exit_code": run.exit_code,
        "duration_s": round(run.duration_s, 2),
        "cost_usd": round(run.cost_usd, 6),
    }
