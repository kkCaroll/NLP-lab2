#!/usr/bin/env python3
"""Run one task end to end: round 1, five feedback branches, round 2.

The task sources under tasks/ are never modified. Every episode runs in a
temporary copy that is initialised as a git repository, so round 1 and every
branch are committed and diffed independently.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import shutil
import tempfile
import time
from pathlib import Path

import branching
import grading
import metrics
import prompts
import task_repo
from opencode_runner import RunLimits, run_opencode

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "RECORD" / "runs"
DEFAULT_MODEL = "opencode/minimax-m3.1-flash-free"


def model_slug(model: str) -> str:
    return model.replace("/", "_").replace(":", "_")


def shuffled_conditions(conditions: list[str], seed_text: str) -> tuple[list[str], str]:
    """Return a reproducible task level condition order and its seed digest."""
    digest = hashlib.sha256(seed_text.encode("utf-8")).hexdigest()[:8]
    order = list(conditions)
    random.Random(int(digest, 16)).shuffle(order)
    return order, digest


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def save_episode(
    episode_dir: Path,
    prompt: str,
    pytest_output: str,
    episode: dict,
    cumulative_diff: str,
    delta_diff: str,
) -> None:
    episode_dir.mkdir(parents=True, exist_ok=True)
    (episode_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
    (episode_dir / "pytest.txt").write_text(pytest_output, encoding="utf-8")
    (episode_dir / "summary.json").write_text(
        json.dumps(episode, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (episode_dir / "diff_cumulative.patch").write_text(
        cumulative_diff, encoding="utf-8"
    )
    (episode_dir / "diff_delta.patch").write_text(delta_diff, encoding="utf-8")


def run_episode(
    workspace: Path,
    snapshot: Path,
    prompt: str,
    limits: RunLimits,
    model: str,
    episode_dir: Path,
    config_home: Path,
    data_home: Path,
    config_template: Path,
    base_ref: str,
    previous_ref: str,
    meta: dict,
    commit_message: str,
) -> tuple[dict, str, str]:
    episode_dir.mkdir(parents=True, exist_ok=True)
    tests_before = task_repo.hash_tests(workspace)
    run = run_opencode(
        workspace,
        prompt,
        model,
        limits,
        episode_dir / "events.jsonl",
        config_home,
        data_home,
        config_template,
    )
    task_repo.wait_for_stable_tree(workspace)
    tampered = task_repo.hash_tests(workspace) != tests_before
    if tampered:
        task_repo.restore_tests(snapshot, workspace)

    grading.clean_caches(workspace)
    task_repo.commit_all(workspace, commit_message)
    task_repo.tag(workspace, commit_message)
    pytest_code, pytest_output, results = grading.run_pytest(
        workspace, episode_dir / "junit.xml"
    )
    grade = grading.grade(meta, pytest_code, results)
    episode = metrics.episode_metrics(
        workspace,
        base_ref,
        previous_ref,
        meta,
        grade,
        run,
        tampered,
    )
    episode["results"] = results
    episode["prompt_sha256"] = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    episode["commits"] = {
        "baseline": task_repo.rev_parse(workspace, task_repo.BASELINE),
        "round1": task_repo.rev_parse(workspace, task_repo.ROUND1),
        "head": task_repo.rev_parse(workspace, "HEAD"),
    }
    episode["worktree_clean"] = not task_repo.is_dirty(workspace)

    cumulative_diff = task_repo.diff_text(workspace, base_ref)
    delta_diff = task_repo.diff_text(workspace, previous_ref)
    save_episode(
        episode_dir,
        prompt,
        pytest_output,
        episode,
        cumulative_diff,
        delta_diff,
    )
    return episode, pytest_output, cumulative_diff


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, help="task directory name")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--round1-tool-calls", type=int, default=10)
    parser.add_argument("--round2-tool-calls", type=int, default=15)
    parser.add_argument("--edit-limit", type=int, default=8)
    parser.add_argument("--timeout", type=float, default=300.0)
    parser.add_argument(
        "--config",
        default="harness/configs/main/opencode.json",
        help="OpenCode config template, relative to the project root",
    )
    parser.add_argument(
        "--conditions",
        default=",".join(prompts.CONDITIONS),
        help="comma separated subset of round 2 conditions",
    )
    parser.add_argument(
        "--condition-order-seed",
        default=None,
        help="seed text for within task condition order; defaults to run, model, task",
    )
    parser.add_argument(
        "--no-tests",
        action="store_true",
        help="use the no-test prompt and the ablation config by default",
    )
    parser.add_argument("--skip-branches", action="store_true")
    parser.add_argument("--keep-temp", action="store_true")
    args = parser.parse_args()

    conditions = [item.strip() for item in args.conditions.split(",") if item.strip()]
    unknown = [item for item in conditions if item not in prompts.CONDITIONS]
    if unknown:
        raise SystemExit(f"unknown conditions: {unknown}")

    run_id = args.run_id or time.strftime("%Y-%m-%d_%H%M%S")
    seed_text = args.condition_order_seed or f"{run_id}|{args.model}|{args.task}"
    conditions, order_seed = shuffled_conditions(conditions, seed_text)
    if args.no_tests and args.config == "harness/configs/main/opencode.json":
        args.config = "harness/configs/ablation/opencode.json"
    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output
    config_template = Path(args.config)
    if not config_template.is_absolute():
        config_template = ROOT / config_template
    if not config_template.is_file():
        raise SystemExit(f"config template not found: {config_template}")
    try:
        config_ref = config_template.relative_to(ROOT).as_posix()
    except ValueError:
        config_ref = str(config_template)
    run_root = output / run_id / model_slug(args.model) / args.task
    run_root.mkdir(parents=True, exist_ok=True)

    meta = task_repo.load_meta(args.task)
    task_dir = task_repo.TASKS / args.task
    initial_log = (task_dir / "initial_test_log.txt").read_text(encoding="utf-8")
    source_hash = task_repo.tree_hash(task_dir / "repo")

    config_home = ROOT / ".runner" / "config"

    temp_root = Path(tempfile.mkdtemp(prefix=f"exp_{args.task}_"))
    round1_ws = temp_root / "round1" / "repo"
    snapshot = temp_root / "snapshot" / "repo"
    task_repo.copy_repo(args.task, round1_ws)
    task_repo.snapshot_repo(args.task, snapshot)
    task_repo.init_repo(round1_ws)

    summary = {
        "task": args.task,
        "model": args.model,
        "run_id": run_id,
        "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "limits": {
            "round1_tool_calls": args.round1_tool_calls,
            "round2_tool_calls": args.round2_tool_calls,
            "edits": args.edit_limit,
            "seconds": args.timeout,
        },
        "conditions": conditions,
        "condition_order": conditions,
        "condition_order_seed": order_seed,
        "no_tests": args.no_tests,
        "round1": {},
        "branches": {},
    }
    write_json(
        run_root / "run_config.json",
        {
            "task": args.task,
            "model": args.model,
            "run_id": run_id,
            "limits": summary["limits"],
            "conditions": conditions,
            "condition_order": conditions,
            "condition_order_seed": order_seed,
            "no_tests": args.no_tests,
            "opencode_config": config_ref,
        },
    )

    try:
        round1_prompt = prompts.build_round1(
            meta["issue"], initial_log, allow_tests=not args.no_tests
        )
        round1_limits = RunLimits(
            tool_calls=args.round1_tool_calls,
            edits=args.edit_limit,
            seconds=args.timeout,
        )
        round1, round1_log, round1_diff = run_episode(
            round1_ws,
            snapshot,
            round1_prompt,
            round1_limits,
            args.model,
            run_root / "round1",
            config_home,
            temp_root / "data" / "round1",
            config_template,
            task_repo.BASELINE,
            task_repo.BASELINE,
            meta,
            task_repo.ROUND1,
        )
        summary["round1"] = round1
        print(
            f"{args.task} round1 {'PASS' if round1['all_passed'] else 'FAIL'} "
            f"tools={round1['tool_calls']} edits={round1['edits']} "
            f"diff={round1['edit_lines']} budget={round1['budget_exhausted']}",
            flush=True,
        )

        if round1["all_passed"] or args.skip_branches:
            return 0

        round1_log = task_repo.normalize_paths(round1_log, round1_ws)
        branch_prompts = {
            condition: prompts.build_round2(
                meta["issue"], round1_diff, round1_log, condition
            )
            for condition in conditions
        }
        common_prefix = prompts.round2_prefix(
            meta["issue"], round1_diff, round1_log
        )
        for condition, prompt in branch_prompts.items():
            expected = common_prefix + prompts.FEEDBACKS[condition] + "\n"
            if prompt != expected:
                raise SystemExit(
                    "round 2 prompts differ outside the feedback sentence"
                )

        branches = branching.create_branches(
            round1_ws, temp_root / "branches", conditions
        )
        round2_limits = RunLimits(
            tool_calls=args.round2_tool_calls,
            edits=args.edit_limit,
            seconds=args.timeout,
        )
        for condition, branch_ws in branches.items():
            episode_dir = run_root / "branches" / condition
            print(f"  branch {condition}", flush=True)
            episode, _, _ = run_episode(
                branch_ws,
                snapshot,
                branch_prompts[condition],
                round2_limits,
                args.model,
                episode_dir,
                config_home,
                temp_root / "data" / condition,
                config_template,
                task_repo.BASELINE,
                task_repo.ROUND1,
                meta,
                task_repo.ROUND2,
            )
            summary["branches"][condition] = episode
            print(
                f"    {'PASS' if episode['all_passed'] else 'FAIL'} "
                f"tools={episode['tool_calls']} edits={episode['edits']} "
                f"diff={episode['edit_lines']} delta={episode['delta_lines']} "
                f"budget={episode['budget_exhausted']}",
                flush=True,
            )

        expected_round1 = summary["round1"]["commits"]["head"]
        inherited = {
            condition: episode["commits"]["round1"]
            for condition, episode in summary["branches"].items()
        }
        summary["branch_integrity"] = {
            "expected_round1": expected_round1,
            "inherited_round1": inherited,
            "consistent": all(
                value == expected_round1 for value in inherited.values()
            ),
        }
        if not summary["branch_integrity"]["consistent"]:
            print("warning: branches inherited different round 1 states", flush=True)
        return 0
    finally:
        if summary["round1"]:
            write_json(run_root / "task_summary.json", summary)
        if task_repo.tree_hash(task_dir / "repo") != source_hash:
            print("task sources changed during the run; restoring", flush=True)
            shutil.rmtree(task_dir / "repo")
            shutil.copytree(snapshot, task_dir / "repo")
        if not args.keep_temp:
            shutil.rmtree(temp_root, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
