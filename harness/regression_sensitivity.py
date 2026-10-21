#!/usr/bin/env python3
"""Measure whether the regression suite can detect non-target source changes.

Two diagnostics are supported.

coverage  run only tests/test_regression.py under coverage and report source
          line coverage, split into gold files and other files.
mutation  apply small AST mutations to non-gold source files and check whether
          tests/test_regression.py fails. Target tests already fail on the
          buggy baseline, so they are not used as a mutation signal.

Both diagnostics run on temporary copies and never modify the task sources.
"""

from __future__ import annotations

import argparse
import ast
import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "tasks"
OUT = ROOT / "RECORD" / "analysis"

COMPARE_MAP = {
    ast.Lt: ast.LtE,
    ast.LtE: ast.Lt,
    ast.Gt: ast.GtE,
    ast.GtE: ast.Gt,
    ast.Eq: ast.NotEq,
    ast.NotEq: ast.Eq,
    ast.In: ast.NotIn,
    ast.NotIn: ast.In,
}
BOOL_MAP = {ast.And: ast.Or, ast.Or: ast.And}
BIN_MAP = {ast.Add: ast.Sub, ast.Sub: ast.Add, ast.Mult: ast.Div, ast.Div: ast.Mult}
OP_BY_NAME = {
    cls.__name__: cls
    for cls in set(COMPARE_MAP) | set(COMPARE_MAP.values())
    | set(BOOL_MAP) | set(BOOL_MAP.values())
    | set(BIN_MAP) | set(BIN_MAP.values())
}


def pytest_env() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def run_pytest(repo: Path, target: str) -> tuple[int, str]:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            target,
            "-q",
            "--tb=no",
            "-p",
            "no:cacheprovider",
        ],
        cwd=repo,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=pytest_env(),
        timeout=180,
    )
    return result.returncode, result.stdout + result.stderr


def load_meta(task: str) -> dict:
    return json.loads((TASKS / task / "meta.json").read_text(encoding="utf-8"))


def copy_task(task: str, destination: Path) -> Path:
    shutil.copytree(TASKS / task / "repo", destination)
    return destination


def coverage_task(task: str) -> dict:
    meta = load_meta(task)
    gold_files = set(meta.get("allowed_files", []))
    with tempfile.TemporaryDirectory(prefix=f"cov_{task}_") as temp:
        repo = copy_task(task, Path(temp) / "repo")
        data_file = Path(temp) / ".coverage"
        env = pytest_env()
        env["COVERAGE_FILE"] = str(data_file)
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "coverage",
                "run",
                "--source=src",
                "-m",
                "pytest",
                "tests/test_regression.py",
                "-q",
                "--tb=no",
                "-p",
                "no:cacheprovider",
            ],
            cwd=repo,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            timeout=180,
        )
        json_path = Path(temp) / "coverage.json"
        subprocess.run(
            [
                sys.executable,
                "-m",
                "coverage",
                "json",
                "-o",
                str(json_path),
                "--include=src/*",
            ],
            cwd=repo,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
        )
        payload = (
            json.loads(json_path.read_text(encoding="utf-8"))
            if json_path.is_file()
            else {}
        )
        totals = {"statements": 0, "covered": 0}
        gold_totals = {"statements": 0, "covered": 0}
        other_totals = {"statements": 0, "covered": 0}
        files = {}
        for raw_name, item in payload.get("files", {}).items():
            name = Path(raw_name).as_posix()
            summary = item.get("summary", {})
            statements = int(summary.get("num_statements", 0))
            covered = int(summary.get("covered_lines", 0))
            files[name] = {"statements": statements, "covered": covered}
            totals["statements"] += statements
            totals["covered"] += covered
            target = gold_totals if name in gold_files else other_totals
            target["statements"] += statements
            target["covered"] += covered
        return {
            "task": task,
            "pytest_code": result.returncode,
            "statements": totals["statements"],
            "covered": totals["covered"],
            "gold_statements": gold_totals["statements"],
            "gold_covered": gold_totals["covered"],
            "other_statements": other_totals["statements"],
            "other_covered": other_totals["covered"],
            "files": files,
        }


def mutation_points(path: Path) -> list[dict]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    points = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            for index, op in enumerate(node.ops):
                if type(op) in COMPARE_MAP:
                    points.append(
                        {
                            "kind": "Compare",
                            "line": node.lineno,
                            "col": node.col_offset,
                            "index": index,
                            "new": COMPARE_MAP[type(op)].__name__,
                        }
                    )
        elif isinstance(node, ast.BoolOp) and type(node.op) in BOOL_MAP:
            points.append(
                {
                    "kind": "BoolOp",
                    "line": node.lineno,
                    "col": node.col_offset,
                    "index": None,
                    "new": BOOL_MAP[type(node.op)].__name__,
                }
            )
        elif isinstance(node, ast.BinOp) and type(node.op) in BIN_MAP:
            points.append(
                {
                    "kind": "BinOp",
                    "line": node.lineno,
                    "col": node.col_offset,
                    "index": None,
                    "new": BIN_MAP[type(node.op)].__name__,
                }
            )
        elif isinstance(node, ast.Constant) and type(node.value) in (int, float):
            value = node.value
            new_value = value + 1 if value >= 0 else value - 1
            points.append(
                {
                    "kind": "Constant",
                    "line": node.lineno,
                    "col": node.col_offset,
                    "index": None,
                    "new": new_value,
                }
            )
    return points


def apply_point(source: str, point: dict) -> str:
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if getattr(node, "lineno", None) != point["line"]:
            continue
        if getattr(node, "col_offset", None) != point["col"]:
            continue
        if point["kind"] == "Compare" and isinstance(node, ast.Compare):
            node.ops[point["index"]] = OP_BY_NAME[point["new"]]()
        elif point["kind"] == "BoolOp" and isinstance(node, ast.BoolOp):
            node.op = OP_BY_NAME[point["new"]]()
        elif point["kind"] == "BinOp" and isinstance(node, ast.BinOp):
            node.op = OP_BY_NAME[point["new"]]()
        elif point["kind"] == "Constant" and isinstance(node, ast.Constant):
            node.value = point["new"]
        else:
            continue
        return ast.unparse(tree) + "\n"
    return source


def select_points(paths: list[Path], limit: int) -> list[tuple[Path, dict]]:
    by_file = []
    for path in paths:
        points = mutation_points(path)
        if points:
            by_file.append((path, points))
    selected = []
    index = 0
    while len(selected) < limit:
        added = False
        for path, points in by_file:
            if index < len(points):
                selected.append((path, points[index]))
                added = True
                if len(selected) >= limit:
                    break
        if not added:
            break
        index += 1
    return selected


def mutation_task(task: str, limit: int) -> list[dict]:
    meta = load_meta(task)
    gold_files = set(meta.get("allowed_files", []))
    with tempfile.TemporaryDirectory(prefix=f"mut_{task}_") as temp:
        repo = copy_task(task, Path(temp) / "repo")
        candidates = [
            path
            for path in sorted((repo / "src").rglob("*.py"))
            if path.relative_to(repo).as_posix() not in gold_files
        ]
        if not candidates:
            return [
                {
                    "task": task,
                    "file": "",
                    "line": 0,
                    "kind": "skip",
                    "new": "",
                    "regression_killed": None,
                }
            ]
        selected = select_points(candidates, limit)
        rows = []
        for path, point in selected:
            original = path.read_text(encoding="utf-8")
            mutated = apply_point(original, point)
            if mutated == original:
                continue
            path.write_text(mutated, encoding="utf-8")
            try:
                reg_code, _ = run_pytest(repo, "tests/test_regression.py")
            finally:
                path.write_text(original, encoding="utf-8")
            rows.append(
                {
                    "task": task,
                    "file": path.relative_to(repo).as_posix(),
                    "line": point["line"],
                    "kind": point["kind"],
                    "new": point["new"],
                    "regression_killed": reg_code != 0,
                }
            )
        return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def coverage_main(tasks: list[str]) -> int:
    rows = []
    for task in tasks:
        rows.append(coverage_task(task))
    write_csv(OUT / "regression_coverage.csv", rows)
    (OUT / "regression_coverage.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    for row in rows:
        total = row["statements"]
        covered = row["covered"]
        rate = covered / total if total else 0.0
        print(
            f"{row['task']}: {covered}/{total} = {rate:.3f}, "
            f"non-gold {row['other_covered']}/{row['other_statements']}"
        )
    return 0


def mutation_main(tasks: list[str], limit: int) -> int:
    rows = []
    for task in tasks:
        rows.extend(mutation_task(task, limit))
    write_csv(OUT / "regression_mutation.csv", rows)
    (OUT / "regression_mutation.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    for task in tasks:
        task_rows = [row for row in rows if row["task"] == task]
        killed = sum(1 for row in task_rows if row["regression_killed"])
        total = len(task_rows)
        print(f"{task}: regression killed {killed}/{total}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["coverage", "mutation"])
    parser.add_argument("--tasks", nargs="*", default=None)
    parser.add_argument("--limit", type=int, default=6)
    args = parser.parse_args()
    tasks = args.tasks or sorted(
        path.name for path in TASKS.glob("T*") if path.is_dir()
    )
    OUT.mkdir(parents=True, exist_ok=True)
    if args.mode == "coverage":
        return coverage_main(tasks)
    return mutation_main(tasks, args.limit)


if __name__ == "__main__":
    raise SystemExit(main())
