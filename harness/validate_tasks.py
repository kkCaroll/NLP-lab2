#!/usr/bin/env python3
"""Validate task packages against the local buggy and gold states.

This script runs pytest in each task repository, applies the gold patch,
checks that test files remain unchanged, and inspects source size and
leakage markers. It does not call a model or perform blind solving.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAK_PATTERN = re.compile(r"\b(BUG|FIXME|TODO|HACK)\b")


def clear_caches(repo: Path) -> None:
    for path in list(repo.rglob("__pycache__")):
        shutil.rmtree(path, ignore_errors=True)
    cache = repo / ".pytest_cache"
    if cache.exists():
        shutil.rmtree(cache, ignore_errors=True)


def run_pytest(repo: Path, target: str | None = None) -> tuple[int, str]:
    clear_caches(repo)
    command = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "--tb=short",
        "-p",
        "no:cacheprovider",
    ]
    if target:
        command.append(target)
    env = dict(os_environ())
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        command,
        cwd=repo,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    return result.returncode, result.stdout + result.stderr


def os_environ() -> dict[str, str]:
    import os

    return dict(os.environ)


def parse_counts(output: str) -> tuple[int, int] | None:
    match = re.search(r"(\d+) failed, (\d+) passed", output)
    if match:
        return int(match.group(1)), int(match.group(2))
    match = re.search(r"(\d+) failed", output)
    if match:
        return int(match.group(1)), 0
    match = re.search(r"(\d+) passed", output)
    if match:
        return 0, int(match.group(1))
    return None


def hash_tree(path: Path) -> dict[str, str]:
    result = {}
    for file_path in sorted(path.rglob("*.py")):
        if "__pycache__" in file_path.parts:
            continue
        if file_path.is_file():
            result[str(file_path.relative_to(path))] = hashlib.sha256(
                file_path.read_bytes()
            ).hexdigest()
    return result


def source_summary(repo: Path) -> tuple[int, int]:
    files = sorted((repo / "src").rglob("*.py"))
    lines = sum(len(path.read_text(encoding="utf-8").splitlines()) for path in files)
    return len(files), lines


def leakage_markers(repo: Path) -> list[str]:
    markers = []
    for path in sorted(repo.rglob("*")):
        if not path.is_file() or path.suffix not in {".py", ".md", ".toml", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in LEAK_PATTERN.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            markers.append(f"{path.relative_to(repo)}:{line}:{match.group(1)}")
    return markers


def validate_task(task_dir: Path, repeat: int) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    notes: list[str] = []
    meta_path = task_dir / "meta.json"
    repo = task_dir / "repo"
    patch_path = task_dir / "gold.patch"
    if not meta_path.exists() or not repo.exists() or not patch_path.exists():
        return [f"missing required file in {task_dir}"], notes

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    expected_buggy = meta["expected_buggy"]
    expected_gold = meta["expected_gold"]
    expected_buggy_counts = parse_counts(expected_buggy)
    expected_gold_counts = parse_counts(expected_gold)
    if expected_buggy_counts is None or expected_gold_counts is None:
        return ["cannot parse expected counts in meta.json"], notes
    file_count, line_count = source_summary(repo)
    difficulty = meta.get("difficulty", "")
    if difficulty == "标准":
        if not 2 <= file_count <= 4 or not 100 <= line_count <= 250:
            errors.append(
                f"standard size outside target: files={file_count} lines={line_count}"
            )
    elif difficulty == "困难":
        if not 4 <= file_count <= 8 or not 250 <= line_count <= 600:
            errors.append(
                f"hard size outside target: files={file_count} lines={line_count}"
            )

    markers = leakage_markers(repo)
    if markers:
        errors.append("leakage markers: " + ", ".join(markers[:5]))

    tests_before = hash_tree(repo / "tests")
    buggy_return, buggy_output = run_pytest(repo)
    buggy_counts = parse_counts(buggy_output)
    if buggy_counts is None:
        errors.append("cannot parse buggy pytest output")
    elif buggy_counts != expected_buggy_counts:
        errors.append(f"buggy counts {buggy_counts} != {expected_buggy_counts}")
    for _ in range(max(0, repeat - 1)):
        _, repeated_output = run_pytest(repo)
        if parse_counts(repeated_output) != buggy_counts:
            errors.append("buggy state is not deterministic across repeats")
            break

    _, target_output = run_pytest(repo, "tests/test_target.py")
    target_counts = parse_counts(target_output)
    if target_counts is None or target_counts[0] == 0:
        errors.append("target tests do not fail in the buggy state")

    _, regression_output = run_pytest(repo, "tests/test_regression.py")
    regression_counts = parse_counts(regression_output)
    if regression_counts is None or regression_counts[0] != 0:
        errors.append("regression tests do not all pass in the buggy state")

    patch_text = patch_path.read_text(encoding="utf-8")
    changed_files = [
        line[6:].strip()
        for line in patch_text.splitlines()
        if line.startswith("+++ b/")
    ]
    if changed_files != meta.get("allowed_files", []):
        errors.append(f"patch changes {changed_files} != {meta.get('allowed_files')}")

    gold_lines = 0
    current_file = None
    for line in patch_text.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[6:].strip()
        elif line.startswith("+++ /dev/null"):
            current_file = None
        elif (
            current_file
            and current_file.endswith(".py")
            and not current_file.startswith("tests/")
            and "/tests/" not in current_file
        ):
            if line.startswith(("+", "-")) and not line.startswith(("+++", "---")):
                gold_lines += 1
    if gold_lines != meta.get("gold_lines"):
        errors.append(
            f"gold patch lines {gold_lines} != meta gold_lines {meta.get('gold_lines')}"
        )

    check = subprocess.run(
        ["git", "apply", "--check", "-p1", str(patch_path)],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    if check.returncode != 0:
        errors.append("gold patch does not apply cleanly: " + check.stderr.strip())
        return errors, notes

    applied = False
    try:
        apply_result = subprocess.run(
            ["git", "apply", "-p1", str(patch_path)],
            cwd=repo,
            capture_output=True,
            text=True,
        )
        if apply_result.returncode != 0:
            errors.append("gold patch application failed: " + apply_result.stderr.strip())
            return errors, notes
        applied = True
        gold_return, gold_output = run_pytest(repo)
        gold_counts = parse_counts(gold_output)
        if gold_counts is None:
            errors.append("cannot parse gold pytest output")
        elif gold_counts != expected_gold_counts:
            errors.append(f"gold counts {gold_counts} != {expected_gold_counts}")
        tests_after = hash_tree(repo / "tests")
        if tests_before != tests_after:
            errors.append("test files changed while applying the gold patch")
    finally:
        if applied:
            subprocess.run(
                ["git", "apply", "-R", "-p1", str(patch_path)],
                cwd=repo,
                capture_output=True,
                text=True,
            )
            clear_caches(repo)

    notes.append(
        f"files={file_count} lines={line_count} buggy={expected_buggy} gold={expected_gold}"
    )
    return errors, notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tasks", nargs="*", help="task directories")
    parser.add_argument("--repeat", type=int, default=1, help="buggy-state repeats")
    args = parser.parse_args()
    if args.tasks:
        task_dirs = [Path(item).resolve() for item in args.tasks]
    else:
        task_dirs = sorted(path for path in (ROOT / "tasks").glob("T*") if path.is_dir())

    failed = False
    for task_dir in task_dirs:
        errors, notes = validate_task(task_dir, args.repeat)
        status = "OK" if not errors else "FAIL"
        print(f"{task_dir.name}: {status}")
        for note in notes:
            print(f"  note: {note}")
        for error in errors:
            print(f"  error: {error}")
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
