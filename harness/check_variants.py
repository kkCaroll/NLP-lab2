#!/usr/bin/env python3
"""Check equivalent and incorrect repairs for pilot tasks.

Each variant replaces one source line in a temporary copy of the task
repository. An equivalent repair must pass the full suite, while an
incorrect repair must fail at least one target or regression test.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

VARIANTS = {
    "T01_next_palindrome": {
        "file": "src/digitkit/palindrome.py",
        "buggy": "return [1] + (len(digit_list)) * [0] + [1]",
        "alternative": "return [1] + [0] * (len(digit_list) - 1) + [1]",
        "wrong": "return [1] + [0] * (len(digit_list) - 2) + [1]",
    },
    "T02_parse_range": {
        "file": "src/rangekit/parse.py",
        "buggy": "return list(range(start, end))",
        "alternative": "return [value for value in range(start, end + 1)]",
        "wrong": "return list(range(start, end + 2))",
    },
    "T03_apply_discount": {
        "file": "src/pricing/discount.py",
        "buggy": 'discount = value * rate / Decimal("100") / Decimal("100")',
        "alternative": 'discount = value * rate * Decimal("0.01")',
        "wrong": 'discount = value * rate / Decimal("1000")',
    },
    "T05_email_regex": {
        "file": "src/mailscan/patterns.py",
        "buggy": 'r"[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}"',
        "alternative": 'r"[A-Za-z0-9._%+\\-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}"',
        "wrong": 'r"[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}"',
    },
    "T16_sales_aggregation": {
        "file": "src/saleskit/aggregate.py",
        "buggy": (
            "        else:\n"
            '            totals[record["region"]] += amount'
        ),
        "alternative": (
            "        else:\n"
            '            totals[record["region"]] = totals[record["region"]] - amount'
        ),
        "wrong": (
            "        else:\n"
            '            totals[record["region"]] += amount'
        ),
    },
    "T21_first_duplicate": {
        "file": "src/seqkit/search.py",
        "buggy": (
            "    seen = set()\n"
            "    result = None\n"
            "    for value in values:\n"
            "        if value in seen:\n"
            "            result = value\n"
            "        seen.add(value)\n"
            "    return result"
        ),
        "alternative": (
            "    positions = {}\n"
            "    for index, value in enumerate(values):\n"
            "        if value in positions:\n"
            "            return values[positions[value]]\n"
            "        positions[value] = index\n"
            "    return None"
        ),
        "wrong": (
            "    seen = set()\n"
            "    result = None\n"
            "    for value in values:\n"
            "        if value in seen:\n"
            "            result = value\n"
            "        seen.add(value)\n"
            "    return result"
        ),
    },
}


def run_suite(repo: Path) -> tuple[int, str]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "--tb=line", "-p", "no:cacheprovider"],
        cwd=repo,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    return result.returncode, result.stdout + result.stderr


def check_task(task_dir: Path, variant: dict[str, str]) -> list[str]:
    errors = []
    source = task_dir / "repo" / variant["file"]
    text = source.read_text(encoding="utf-8")
    if text.count(variant["buggy"]) != 1:
        return [f"buggy line not found exactly once in {variant['file']}"]

    for name in ("alternative", "wrong"):
        with tempfile.TemporaryDirectory(prefix=f"variant_{task_dir.name}_") as temp:
            work = Path(temp) / "repo"
            shutil.copytree(task_dir / "repo", work)
            target = work / variant["file"]
            content = target.read_text(encoding="utf-8")
            target.write_text(
                content.replace(variant["buggy"], variant[name], 1),
                encoding="utf-8",
            )
            code, output = run_suite(work)
            failure = "failed" if code else "passed"
            print(f"  {name}: {failure}")
            if name == "alternative" and code != 0:
                errors.append("equivalent repair does not pass")
            if name == "wrong" and code == 0:
                errors.append("incorrect repair passes")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tasks", nargs="*", help="task directory names")
    args = parser.parse_args()
    names = args.tasks or sorted(VARIANTS)
    failed = False
    for name in names:
        if name not in VARIANTS:
            print(f"{name}: SKIP, no variants defined")
            continue
        task_dir = ROOT / "tasks" / name
        print(f"{name}:")
        errors = check_task(task_dir, VARIANTS[name])
        if errors:
            failed = True
            for error in errors:
                print(f"  error: {error}")
        else:
            print("  OK")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
