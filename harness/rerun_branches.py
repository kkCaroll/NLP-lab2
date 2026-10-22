#!/usr/bin/env python3
"""Re-run selected round 2 branches at alternative tool call budgets.

The source episodes are reconstructed rather than replayed, because every
round 1 diff in the main run is empty. The branch start state therefore equals
the pristine task repository. The round 2 prompt is copied byte for byte from
the source episode and checked against the recorded prompt_sha256, and every
file under tasks/<task>/repo is checked against tasks_manifest.json.

Usage example, one arm only, first two cases as a smoke test.

    python -I harness/rerun_branches.py \
        --run-id 2026-10-22_budget_rerun \
        --budgets 30 --limit 2
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import shutil
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import task_repo
from opencode_runner import RunLimits
from run_experiment import model_slug, run_episode

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "RECORD" / "runs" / "2026-10-21_main"
DEFAULT_METRICS = ROOT / "RECORD" / "analysis" / "deepening" / "process_metrics.csv"
DEFAULT_OUTPUT = ROOT / "RECORD" / "runs"
DEFAULT_MANIFEST = ROOT / "RECORD" / "analysis" / "tasks_manifest.json"
DEFAULT_MODEL = "opencode/minimax-m3.1-flash-free"

RESULT_FIELDS = [
    "model",
    "task",
    "condition",
    "budget",
    "all_passed",
    "tool_calls",
    "denied_tool_calls",
    "edits",
    "budget_exhausted",
    "timed_out",
    "exit_code",
    "duration_s",
    "prompt_sha256_match",
    "round1_unchanged",
    "error",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def select_cases(metrics_path: Path, model: str, outcome: str) -> list[dict]:
    selected = []
    short_name = model.split("/")[-1]
    with metrics_path.open(encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            if row["condition"] == "round1":
                continue
            if row["outcome"] != outcome:
                continue
            if row["model"] != short_name:
                continue
            selected.append({"task": row["task"], "condition": row["condition"]})
    if not selected:
        raise SystemExit(f"no cases with outcome {outcome} for model {slug}")
    return selected


def verify_task_sources(task: str, manifest: dict) -> list[str]:
    """Return paths whose bytes differ from the recorded manifest."""
    root = task_repo.TASKS / task
    mismatched = []
    for path in sorted((root / "repo").rglob("*")):
        if not path.is_file():
            continue
        if any(part in {"__pycache__", ".pytest_cache", ".git"} for part in path.parts):
            continue
        relative = path.relative_to(ROOT).as_posix()
        expected = manifest.get(relative, {}).get("sha256")
        if expected is None or sha256_file(path) != expected:
            mismatched.append(relative)
    return mismatched


def build_workspace(task: str, temp_root: Path) -> tuple[Path, Path]:
    """Create the pristine round 1 state and a snapshot for test restoration."""
    workspace = temp_root / "repo"
    snapshot = temp_root / "snapshot" / "repo"
    task_repo.copy_repo(task, workspace)
    task_repo.snapshot_repo(task, snapshot)
    task_repo.init_repo(workspace)
    task_repo.tag(workspace, task_repo.ROUND1)
    return workspace, snapshot


def run_pair(
    pair: dict,
    source_root: Path,
    run_root: Path,
    manifest: dict,
    args: argparse.Namespace,
) -> dict:
    model = pair["model"]
    task = pair["task"]
    condition = pair["condition"]
    budget = pair["budget"]
    source_dir = source_root / model_slug(model) / task / "branches" / condition
    episode_dir = (
        run_root / model_slug(model) / task / "branches" / condition
        / f"budget_{budget}"
    )
    record = {
        "model": model,
        "task": task,
        "condition": condition,
        "budget": budget,
        "all_passed": "",
        "tool_calls": "",
        "denied_tool_calls": "",
        "edits": "",
        "budget_exhausted": "",
        "timed_out": "",
        "exit_code": "",
        "duration_s": "",
        "prompt_sha256_match": "",
        "round1_unchanged": "",
        "error": "",
    }
    if (episode_dir / "summary.json").is_file() and not args.force:
        summary = load_json(episode_dir / "summary.json")
        record.update(episode_fields(summary))
        record["error"] = "skipped, summary exists"
        return record

    mismatched = verify_task_sources(task, manifest)
    if mismatched:
        record["error"] = f"task source mismatch: {mismatched[:3]}"
        return record

    prompt = (source_dir / "prompt.txt").read_text(encoding="utf-8")
    expected_prompt = load_json(source_dir / "summary.json").get("prompt_sha256")
    prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    record["prompt_sha256_match"] = prompt_hash == expected_prompt
    if not record["prompt_sha256_match"]:
        record["error"] = "prompt hash mismatch"
        return record

    temp_root = Path(tempfile.mkdtemp(prefix=f"rerun_{task}_{condition}_"))
    try:
        workspace, snapshot = build_workspace(task, temp_root)
        limits = RunLimits(
            tool_calls=budget, edits=args.edit_limit, seconds=args.timeout
        )
        episode, _, _ = run_episode(
            workspace,
            snapshot,
            prompt,
            limits,
            model,
            episode_dir,
            ROOT / ".runner" / "config",
            temp_root / "data",
            args.config,
            task_repo.BASELINE,
            task_repo.ROUND1,
            task_repo.load_meta(task),
            task_repo.ROUND2,
        )
        record.update(episode_fields(episode))
        record["round1_unchanged"] = (
            episode["commits"]["baseline"] == episode["commits"]["round1"]
        )
    finally:
        if not args.keep_temp:
            shutil.rmtree(temp_root, ignore_errors=True)
    return record


def episode_fields(summary: dict) -> dict:
    return {
        "all_passed": bool(summary.get("all_passed")),
        "tool_calls": summary.get("tool_calls"),
        "denied_tool_calls": summary.get("denied_tool_calls"),
        "edits": summary.get("edits"),
        "budget_exhausted": bool(summary.get("budget_exhausted")),
        "timed_out": bool(summary.get("timed_out")),
        "exit_code": summary.get("exit_code"),
        "duration_s": summary.get("duration_s"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-run", default=str(DEFAULT_SOURCE))
    parser.add_argument("--metrics", default=str(DEFAULT_METRICS))
    parser.add_argument("--tasks-manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--outcome", default="budget_cutoff")
    parser.add_argument("--budgets", default="15,30")
    parser.add_argument("--timeout", type=float, default=300.0)
    parser.add_argument("--edit-limit", type=int, default=8)
    parser.add_argument(
        "--config", default=str(ROOT / "harness" / "configs" / "main" / "opencode.json")
    )
    parser.add_argument("--seed", default="20261022")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true")
    parser.add_argument("--keep-temp", action="store_true")
    args = parser.parse_args()

    source_root = Path(args.source_run)
    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output
    run_root = output / args.run_id
    slug = model_slug(args.model)
    manifest = load_json(Path(args.tasks_manifest))

    cases = select_cases(Path(args.metrics), args.model, args.outcome)
    budgets = [int(item) for item in args.budgets.split(",") if item.strip()]
    pairs = [
        {"model": args.model, "task": case["task"], "condition": case["condition"],
         "budget": budget}
        for case in cases
        for budget in budgets
    ]
    random.Random(int(hashlib.sha256(args.seed.encode()).hexdigest()[:8], 16)).shuffle(pairs)
    if args.limit:
        pairs = pairs[: args.limit]

    print(
        f"{len(cases)} cases x {len(budgets)} budgets = {len(pairs)} episodes, "
        f"model {args.model}",
        flush=True,
    )
    if args.dry_run:
        for pair in pairs:
            print(pair["task"], pair["condition"], pair["budget"])
        return 0

    state = {
        "run_id": args.run_id,
        "source_run": str(source_root.relative_to(ROOT).as_posix()),
        "model": args.model,
        "budgets": budgets,
        "edit_limit": args.edit_limit,
        "timeout_s": args.timeout,
        "seed": args.seed,
        "outcome": args.outcome,
        "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "order": pairs,
        "results": [],
        "status": "running",
    }
    write_json(run_root / "run_manifest.json", state)

    for index, pair in enumerate(pairs, start=1):
        print(
            f"[{index}/{len(pairs)}] {pair['task']} {pair['condition']} "
            f"budget={pair['budget']}",
            flush=True,
        )
        try:
            record = run_pair(pair, source_root, run_root, manifest, args)
        except Exception as error:  # noqa: BLE001
            record = dict(pair, error=f"{type(error).__name__}: {error}")
        record["model"] = args.model
        state["results"].append(record)
        write_json(run_root / "run_manifest.json", state)
        print(
            f"    pass={record.get('all_passed')} tools={record.get('tool_calls')} "
            f"edits={record.get('edits')} budget={record.get('budget_exhausted')} "
            f"error={record.get('error')}",
            flush=True,
        )
        bad = record.get("error") and record.get("error") != "skipped, summary exists"
        if bad and not args.continue_on_error:
            state["status"] = "stopped"
            state["stopped_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            write_json(run_root / "run_manifest.json", state)
            print("stopped on anomaly", flush=True)
            return 1
        if record.get("timed_out") and not args.continue_on_error:
            state["status"] = "stopped"
            state["stopped_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            write_json(run_root / "run_manifest.json", state)
            print("stopped on timeout", flush=True)
            return 1

    state["status"] = "completed"
    state["finished_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    write_json(run_root / "run_manifest.json", state)

    results_path = run_root / "results.csv"
    keys = list(RESULT_FIELDS)
    with results_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(state["results"])
    print(f"wrote {results_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
