#!/usr/bin/env python3
"""Run a blind repair attempt with DeepSeek-V4-Pro through OpenCode.

The model sees only the issue text, the initial pytest log and a copy of the
task repository. Tests are hashed before the run, restored if modified, and
the final state is graded with pytest. Results and raw events are written
under RECORD/calibration/blind.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "tasks"
OUTPUT = ROOT / "RECORD" / "calibration" / "blind"
CONFIG_HOME = ROOT / "RECORD" / "calibration" / "opencode-config"
DATA_HOME = ROOT / "RECORD" / "calibration" / "opencode-data"
CONFIG_TEMPLATE = ROOT / "harness" / "configs" / "blind" / "opencode.json"
MODEL = "deepseek/deepseek-v4-pro"
PILOTS = [
    "T01_next_palindrome",
    "T05_email_regex",
    "T16_sales_aggregation",
    "T21_first_duplicate",
]
PROMPT = """你是一名代码修复智能体。当前工作目录是一个 Python 项目。

项目说明：
{issue}

初始测试失败信息：
```text
{log}
```

请阅读项目代码和测试，定位并修复 bug，使全部测试通过。
你可以用 Bash 运行 `python -m pytest` 检查修复结果。
约束：不要修改 tests/ 目录下的任何文件，也不要修改测试配置文件。
完成后用一句话总结你的修改。
"""


def hash_tests(repo: Path) -> dict[str, str]:
    result = {}
    for path in sorted((repo / "tests").rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        result[str(path.relative_to(repo))] = hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
    return result


def restore_tests(source: Path, target: Path) -> None:
    destination = target / "tests"
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source / "tests", destination)


def run_pytest(repo: Path) -> tuple[int, str]:
    for path in list(repo.rglob("__pycache__")):
        shutil.rmtree(path, ignore_errors=True)
    cache = repo / ".pytest_cache"
    if cache.exists():
        shutil.rmtree(cache, ignore_errors=True)
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "--tb=short",
            "-p",
            "no:cacheprovider",
        ],
        cwd=repo,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        timeout=120,
    )
    return result.returncode, result.stdout + result.stderr


def parse_counts(output: str) -> tuple[int, int]:
    failed = re.search(r"(\d+) failed", output)
    passed = re.search(r"(\d+) passed", output)
    return (
        int(failed.group(1)) if failed else 0,
        int(passed.group(1)) if passed else 0,
    )


def parse_events(events: list[dict]) -> tuple[int, int, float]:
    tool_calls = 0
    edits = 0
    cost = 0.0
    for event in events:
        part = event.get("part", {})
        if event.get("type") == "tool_use":
            tool_calls += 1
            tool = part.get("tool", "")
            if tool in {"edit", "write", "patch"}:
                edits += 1
        if event.get("type") == "step_finish":
            cost += float(part.get("cost", 0.0))
    return tool_calls, edits, cost


def repository_files(root: Path) -> dict[str, Path]:
    files = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in {"__pycache__", ".pytest_cache", ".git"} for part in path.parts):
            continue
        files[path.relative_to(root).as_posix()] = path
    return files


def diff_stats(source: Path, target: Path) -> tuple[int, list[str], str]:
    import difflib

    old_files = repository_files(source)
    new_files = repository_files(target)
    total = 0
    files = []
    chunks = []
    for relative in sorted(set(old_files) | set(new_files)):
        old_path = old_files.get(relative)
        new_path = new_files.get(relative)
        old_lines = (
            old_path.read_text(encoding="utf-8", errors="replace").splitlines(
                keepends=True
            )
            if old_path
            else []
        )
        new_lines = (
            new_path.read_text(encoding="utf-8", errors="replace").splitlines(
                keepends=True
            )
            if new_path
            else []
        )
        if old_lines == new_lines:
            continue
        diff = list(
            difflib.unified_diff(
                old_lines,
                new_lines,
                fromfile=f"a/{relative}",
                tofile=f"b/{relative}",
                n=3,
            )
        )
        if not diff:
            continue
        files.append(relative)
        for line in diff:
            if line.startswith(("+", "-")) and not line.startswith(("+++", "---")):
                total += 1
        chunks.extend(diff)
    return total, files, "".join(chunks)


def run_model(repo: Path, prompt: str, raw_log: Path) -> tuple[int, bool, float, list[dict]]:
    env = dict(os.environ)
    env["XDG_CONFIG_HOME"] = str(CONFIG_HOME)
    env["XDG_DATA_HOME"] = str(DATA_HOME)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    command = [
        "opencode",
        "run",
        "--dir",
        str(repo),
        "--model",
        MODEL,
        "--agent",
        "build",
        "--format",
        "json",
        "--pure",
        "--auto",
        prompt,
    ]
    started = time.monotonic()
    process = subprocess.Popen(
        command,
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    timed_out = False
    try:
        stdout, stderr = process.communicate(timeout=420)
    except subprocess.TimeoutExpired:
        timed_out = True
        subprocess.run(
            ["taskkill", "/PID", str(process.pid), "/T", "/F"],
            capture_output=True,
        )
        stdout, stderr = process.communicate()
    duration = time.monotonic() - started
    raw_log.write_text(stdout + "\n--- STDERR ---\n" + stderr, encoding="utf-8")
    events = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return process.returncode, timed_out, duration, events


def solve(task_name: str) -> dict:
    task_dir = TASKS / task_name
    meta = json.loads((task_dir / "meta.json").read_text(encoding="utf-8"))
    log = (task_dir / "initial_test_log.txt").read_text(encoding="utf-8")
    out_dir = OUTPUT / task_name
    work = out_dir / "repo"
    if work.exists():
        shutil.rmtree(work)
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copytree(task_dir / "repo", work)

    tests_before = hash_tests(work)
    prompt = PROMPT.format(issue=meta["issue"], log=log.strip())
    (out_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
    code, timed_out, duration, events = run_model(
        work, prompt, out_dir / "events.jsonl"
    )
    tampered = hash_tests(work) != tests_before
    if tampered:
        restore_tests(task_dir / "repo", work)
    pytest_code, pytest_output = run_pytest(work)
    (out_dir / "pytest.txt").write_text(pytest_output, encoding="utf-8")
    failed, passed = parse_counts(pytest_output)
    tool_calls, edits, cost = parse_events(events)
    diff_lines, changed_files, patch = diff_stats(task_dir / "repo", work)
    (out_dir / "model.patch").write_text(patch, encoding="utf-8")
    summary = {
        "task": task_name,
        "model": MODEL,
        "exit_code": code,
        "timed_out": timed_out,
        "duration_s": round(duration, 2),
        "pytest_exit_code": pytest_code,
        "tests_failed": failed,
        "tests_passed": passed,
        "all_passed": pytest_code == 0,
        "test_tampered": tampered,
        "tool_calls": tool_calls,
        "edits": edits,
        "cost_usd": round(cost, 6),
        "diff_lines": diff_lines,
        "files_changed": changed_files,
    }
    (out_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return summary


def ensure_config() -> None:
    target = CONFIG_HOME / "opencode" / "opencode.json"
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(CONFIG_TEMPLATE, target)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tasks", nargs="*", default=PILOTS, help="task directory names")
    args = parser.parse_args()
    ensure_config()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    summaries = []
    for task_name in args.tasks:
        print(f"{task_name}: running", flush=True)
        summary = solve(task_name)
        summaries.append(summary)
        status = "PASS" if summary["all_passed"] else "FAIL"
        print(
            f"  {status} passed={summary['tests_passed']} "
            f"failed={summary['tests_failed']} tampered={summary['test_tampered']} "
            f"diff={summary['diff_lines']} cost={summary['cost_usd']}",
            flush=True,
        )
    summary_path = OUTPUT / "summary.json"
    existing = []
    if summary_path.exists():
        existing = json.loads(summary_path.read_text(encoding="utf-8"))
    by_task = {item["task"]: item for item in existing}
    by_task.update({item["task"]: item for item in summaries})
    ordered = [by_task[name] for name in PILOTS if name in by_task]
    ordered.extend(
        item for name, item in by_task.items() if name not in PILOTS
    )
    summary_path.write_text(
        json.dumps(ordered, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
