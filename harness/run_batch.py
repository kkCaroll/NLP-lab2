#!/usr/bin/env python3
"""Run the main experiment over tasks and models.

Each task is executed by run_experiment.py in a separate process so a crash
cannot corrupt the batch. Completed task summaries are reused on restart.
The batch stops on the first anomalous episode so the cause can be inspected
before more data are collected.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "tasks"
DEFAULT_OUTPUT = ROOT / "RECORD" / "runs"
DEFAULT_MODELS = [
    "opencode/minimax-m3.1-flash-free",
    "opencode/mimo-v2.6-flash-free",
]
CONDITIONS = [
    "pure_continue",
    "neutral",
    "method_guidance",
    "negative",
    "negative_guidance",
]


def model_slug(model: str) -> str:
    return model.replace("/", "_").replace(":", "_")


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def task_names() -> list[str]:
    return sorted(
        path.name
        for path in TASKS.iterdir()
        if path.is_dir() and path.name.startswith("T")
    )


def summary_path(output: Path, run_id: str, model: str, task: str) -> Path:
    return output / run_id / model_slug(model) / task / "task_summary.json"


def add_record(manifest: dict, record: dict) -> None:
    key = (record.get("model"), record.get("task"))
    manifest["runs"] = [
        item
        for item in manifest.get("runs", [])
        if (item.get("model"), item.get("task")) != key
    ]
    manifest["runs"].append(record)


def load_summary(path: Path) -> dict | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def load_json(path: Path) -> dict | None:
    return load_summary(path)


def is_complete(summary: dict, conditions: list[str]) -> bool:
    if not summary.get("round1"):
        return False
    if summary["round1"].get("all_passed"):
        return True
    return set(summary.get("branches", {})) == set(conditions)


def episode_anomalies(summary: dict) -> tuple[list[str], list[str]]:
    problems = []
    warnings = []
    episodes = [("round1", summary.get("round1", {}))]
    episodes.extend(
        (f"branch:{name}", episode)
        for name, episode in summary.get("branches", {}).items()
    )
    for label, episode in episodes:
        if not episode:
            problems.append(f"{label} missing")
            continue
        if episode.get("timed_out"):
            problems.append(f"{label} timed out")
        expected_kill = episode.get("budget_exhausted") and not episode.get(
            "timed_out"
        )
        if episode.get("exit_code") not in (0, None) and not expected_kill:
            problems.append(f"{label} exit code {episode.get('exit_code')}")
        if episode.get("test_tampered"):
            # Test changes are restored before grading and are an outcome,
            # not an infrastructure failure. They are kept and analysed.
            warnings.append(f"{label} modified tests or test config")
    integrity = summary.get("branch_integrity")
    if integrity and not integrity.get("consistent", True):
        problems.append("branches inherited different round 1 states")
    return problems, warnings


def opencode_version() -> str:
    try:
        result = subprocess.run(
            ["opencode", "--version"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
        return (result.stdout + result.stderr).strip()
    except (OSError, subprocess.TimeoutExpired):
        return "unknown"


def config_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_task(
    task: str,
    model: str,
    run_id: str,
    output: Path,
    args: argparse.Namespace,
    log_path: Path,
) -> tuple[int, str]:
    command = [
        sys.executable,
        str(ROOT / "harness" / "run_experiment.py"),
        "--task",
        task,
        "--model",
        model,
        "--run-id",
        run_id,
        "--output",
        str(output),
        "--round1-tool-calls",
        str(args.round1_tool_calls),
        "--round2-tool-calls",
        str(args.round2_tool_calls),
        "--edit-limit",
        str(args.edit_limit),
        "--timeout",
        str(args.timeout),
        "--config",
        args.config,
        "--conditions",
        ",".join(args.conditions),
    ]
    if args.condition_order_seed:
        command.extend(["--condition-order-seed", args.condition_order_seed])
    if args.no_tests:
        command.append("--no-tests")
    started = time.monotonic()
    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    elapsed = time.monotonic() - started
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(
        f"$ {' '.join(command)}\n\n"
        f"--- STDOUT ---\n{result.stdout}\n"
        f"--- STDERR ---\n{result.stderr}\n"
        f"--- exit={result.returncode} elapsed={elapsed:.1f}s ---\n",
        encoding="utf-8",
    )
    return result.returncode, result.stdout


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--models", default=",".join(DEFAULT_MODELS))
    parser.add_argument("--tasks", nargs="*", default=None)
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--round1-tool-calls", type=int, default=10)
    parser.add_argument("--round2-tool-calls", type=int, default=15)
    parser.add_argument("--edit-limit", type=int, default=8)
    parser.add_argument("--timeout", type=float, default=300.0)
    parser.add_argument("--config", default="harness/configs/main/opencode.json")
    parser.add_argument(
        "--conditions", nargs="*", default=CONDITIONS, choices=CONDITIONS
    )
    parser.add_argument(
        "--condition-order-seed",
        default=None,
        help="seed text for within task condition order; defaults to run, model, task",
    )
    parser.add_argument(
        "--no-tests",
        action="store_true",
        help="run the no-test ablation prompt and config",
    )
    parser.add_argument(
        "--allow-anomalies",
        action="store_true",
        help="continue after a timed-out or tampered episode",
    )
    parser.add_argument(
        "--force", action="store_true", help="rerun tasks with existing summaries"
    )
    args = parser.parse_args()

    run_id = args.run_id or time.strftime("%Y-%m-%d_%H%M%S")
    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output
    models = [item.strip() for item in args.models.split(",") if item.strip()]
    tasks = args.tasks or task_names()
    unknown = sorted(set(tasks) - set(task_names()))
    if unknown:
        raise SystemExit(f"unknown tasks: {unknown}")

    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = ROOT / config_path
    main_config = ROOT / "harness" / "configs" / "main" / "opencode.json"
    ablation_config = ROOT / "harness" / "configs" / "ablation" / "opencode.json"
    if args.no_tests and config_path == main_config:
        config_path = ablation_config
    manifest_path = output / run_id / "batch_manifest.json"
    previous = load_json(manifest_path) or {}
    manifest = {
        "run_id": run_id,
        "started_at": previous.get(
            "started_at", time.strftime("%Y-%m-%d %H:%M:%S")
        ),
        "models": models,
        "tasks": tasks,
        "conditions": args.conditions,
        "condition_order_seed": args.condition_order_seed,
        "no_tests": args.no_tests,
        "limits": {
            "round1_tool_calls": args.round1_tool_calls,
            "round2_tool_calls": args.round2_tool_calls,
            "edits": args.edit_limit,
            "seconds": args.timeout,
        },
        "opencode_version": opencode_version(),
        "config": str(config_path.relative_to(ROOT)),
        "config_sha256": config_hash(config_path),
        "runs": previous.get("runs", []),
        "status": "running",
    }
    write_json(manifest_path, manifest)
    print(
        f"run {run_id}, {len(models)} models x {len(tasks)} tasks, "
        f"opencode {manifest['opencode_version']}",
        flush=True,
    )

    for model in models:
        for task in tasks:
            path = summary_path(output, run_id, model, task)
            summary = load_summary(path)
            if summary and is_complete(summary, args.conditions) and not args.force:
                print(f"{model} {task}: skip, already complete", flush=True)
                known = any(
                    item.get("model") == model and item.get("task") == task
                    for item in manifest["runs"]
                )
                if not known:
                    add_record(
                        manifest,
                        {"model": model, "task": task, "status": "skipped"},
                    )
                write_json(manifest_path, manifest)
                continue

            print(f"{model} {task}: running", flush=True)
            log_path = (
                output / run_id / model_slug(model) / task / "batch_task.log"
            )
            code, stdout = run_task(
                task, model, run_id, output, args, log_path
            )
            summary = load_summary(path)
            if code != 0 or summary is None:
                add_record(
                    manifest,
                    {
                        "model": model,
                        "task": task,
                        "status": "failed",
                        "exit_code": code,
                        "stdout_tail": stdout[-2000:],
                    },
                )
                manifest["status"] = "stopped"
                manifest["stopped_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
                write_json(manifest_path, manifest)
                print(f"{model} {task}: FAILED, batch stopped", flush=True)
                return 1

            anomalies, warnings = episode_anomalies(summary)
            branches = summary.get("branches", {})
            record = {
                "model": model,
                "task": task,
                "status": "anomaly" if anomalies else "ok",
                "round1_passed": summary["round1"].get("all_passed"),
                "round1_tool_calls": summary["round1"].get("tool_calls"),
                "branch_count": len(branches),
                "branches_passed": sum(
                    1 for item in branches.values() if item.get("all_passed")
                ),
                "anomalies": anomalies,
                "warnings": warnings,
            }
            add_record(manifest, record)
            write_json(manifest_path, manifest)
            state = "ANOMALY" if anomalies else ("warning" if warnings else "ok")
            detail = "; ".join(anomalies + warnings)
            print(
                f"{model} {task}: round1={'PASS' if record['round1_passed'] else 'FAIL'} "
                f"branches={record['branches_passed']}/{record['branch_count']} "
                f"{state}" + (f" {detail}" if detail else ""),
                flush=True,
            )
            if anomalies and not args.allow_anomalies:
                manifest["status"] = "stopped"
                manifest["stopped_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
                write_json(manifest_path, manifest)
                print("anomaly detected, batch stopped", flush=True)
                return 1

    manifest["status"] = "completed"
    manifest["finished_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    write_json(manifest_path, manifest)
    print("batch completed", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
