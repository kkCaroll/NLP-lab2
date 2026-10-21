"""Run pytest and grade a workspace against target and regression tests."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Grade:
    pytest_code: int
    all_passed: bool
    target_passed: int
    regression_passed: int
    target_failed: list[str] = field(default_factory=list)
    regression_failed: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    results: dict[str, str] = field(default_factory=dict)


def clean_caches(workspace: Path) -> None:
    for path in list(workspace.rglob("__pycache__")):
        shutil.rmtree(path, ignore_errors=True)
    cache = workspace / ".pytest_cache"
    if cache.exists():
        shutil.rmtree(cache, ignore_errors=True)


def run_pytest(workspace: Path, junit_path: Path) -> tuple[int, str, dict[str, str]]:
    clean_caches(workspace)
    if junit_path.exists():
        junit_path.unlink()
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
            f"--junitxml={junit_path}",
        ],
        cwd=workspace,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        timeout=180,
    )
    output = result.stdout + result.stderr
    results = parse_junit(workspace, junit_path) if junit_path.exists() else {}
    clean_caches(workspace)
    return result.returncode, output, results


def _node_id(workspace: Path, classname: str, name: str) -> str | None:
    parts = [part for part in (classname or "").split(".") if part]
    for index in range(len(parts), 0, -1):
        candidate = "/".join(parts[:index]) + ".py"
        if (workspace / candidate).is_file():
            node = candidate
            for extra in parts[index:]:
                node += f"::{extra}"
            return f"{node}::{name}"
    return None


def parse_junit(workspace: Path, junit_path: Path) -> dict[str, str]:
    try:
        root = ET.parse(junit_path).getroot()
    except ET.ParseError:
        return {}
    results: dict[str, str] = {}
    for case in root.iter("testcase"):
        name = case.get("name", "")
        classname = case.get("classname", "")
        node = _node_id(workspace, classname, name)
        if node is None:
            node = f"{classname}::{name}"
        status = "passed"
        for child in case:
            if child.tag in {"failure", "error"}:
                status = child.tag
                break
            if child.tag == "skipped":
                status = "skipped"
        results[node] = status
    return results


def parse_counts(output: str) -> tuple[int, int]:
    failed = re.search(r"(\d+) failed", output)
    passed = re.search(r"(\d+) passed", output)
    return (
        int(failed.group(1)) if failed else 0,
        int(passed.group(1)) if passed else 0,
    )


def grade(meta: dict, pytest_code: int, results: dict[str, str]) -> Grade:
    targets = list(meta.get("target_tests", []))
    regressions = list(meta.get("regression_tests", []))

    target_failed = [node for node in targets if results.get(node) != "passed"]
    regression_failed = [node for node in regressions if results.get(node) != "passed"]
    missing = [node for node in targets + regressions if node not in results]

    all_passed = pytest_code == 0 and not target_failed and not regression_failed
    return Grade(
        pytest_code=pytest_code,
        all_passed=all_passed,
        target_passed=len(targets) - len(target_failed),
        target_failed=target_failed,
        regression_passed=len(regressions) - len(regression_failed),
        regression_failed=regression_failed,
        missing=missing,
        results=results,
    )
