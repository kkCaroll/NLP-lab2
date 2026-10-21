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
    "T04_next_permutation": {
        "file": "src/seqkit/permute.py",
        "buggy": "values[pivot:] = reversed(values[pivot:])",
        "alternative": "values[pivot + 1:] = values[pivot + 1:][::-1]",
        "wrong": "values[pivot:] = reversed(values[pivot:])",
    },
    "T05_email_regex": {
        "file": "src/mailscan/patterns.py",
        "buggy": 'r"[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}"',
        "alternative": 'r"[A-Za-z0-9._%+\\-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}"',
        "wrong": 'r"[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}"',
    },
    "T06_version_scan": {
        "file": "src/textscan/patterns.py",
        "buggy": 'r"(?<![\\w.-])v?(\\d+\\.\\d+\\.\\d+(?:-[0-9A-Za-z.-]+)?)"',
        "alternative": (
            'r"(?<![\\w.-])v?(\\d+\\.\\d+\\.\\d+(?:-[0-9A-Za-z.-]+)?)'
            '(?![0-9A-Za-z_.-])"'
        ),
        "wrong": 'r"(?<![\\w.-])v?(\\d+\\.\\d+\\.\\d+(?:-[0-9A-Za-z.-]+)?)"',
    },
    "T07_group_counts": {
        "file": "src/recordkit/aggregate.py",
        "buggy": "        return value.strip()",
        "alternative": "        return value.strip().casefold()",
        "wrong": "        return value",
    },
    "T08_inventory_summary": {
        "file": "src/inventory/summary.py",
        "buggy": '        total += item.get("quantity", 0)',
        "alternative": (
            '        quantity = item.get("quantity")\n'
            "        total += 1 if quantity is None else quantity"
        ),
        "wrong": '        total += item.get("quantity", 2)',
    },
    "T09_safe_int": {
        "file": "src/convertkit/parse.py",
        "buggy": (
            "    try:\n"
            "        return int(value)\n"
            "    except ValueError:\n"
            "        return default\n"
        ),
        "alternative": (
            "    try:\n"
            "        return int(value)\n"
            "    except (ValueError, TypeError):\n"
            "        return default\n"
        ),
        "wrong": (
            "    try:\n"
            "        return int(value)\n"
            "    except (TypeError, ValueError):\n"
            "        return 0\n"
        ),
    },
    "T10_top_k": {
        "file": "src/rankkit/topk.py",
        "buggy": "    return values[: limit + 1]",
        "alternative": "    return values[:limit]",
        "wrong": "    return values[: limit + 2]",
    },
    "T11_sort_items": {
        "file": "src/listkit/ordering.py",
        "buggy": "    return items.sort(reverse=reverse)",
        "alternative": "    return sorted(items, reverse=reverse)",
        "wrong": (
            "    items.sort(reverse=reverse)\n"
            "    return items"
        ),
    },
    "T12_format_datetime": {
        "file": "src/timekit/format.py",
        "buggy": 'DATE_FORMAT = "%Y-%M-%d"',
        "alternative": 'DATE_FORMAT = "%Y-%m-%d"',
        "wrong": 'DATE_FORMAT = "%Y-%d-%m"',
    },
    "T13_paginate": {
        "file": "src/pagekit/limits.py",
        "buggy": "    return max(low, min(value, high + 1))",
        "alternative": "    return min(max(value, low), high)",
        "wrong": "    return max(low, min(value, high + 2))",
    },
    "T15_slugify": {
        "file": "src/slugkit/slug.py",
        "buggy": 'SLUG_PATTERN = re.compile(r"[^a-z0-9]")',
        "alternative": 'SLUG_PATTERN = re.compile(r"[\\W_]+")',
        "wrong": 'SLUG_PATTERN = re.compile(r"[^a-z]+")',
    },
    "T17_merge_records": {
        "file": "src/mergekit/records.py",
        "buggy": "        if key not in merged:\n            merged[key] = candidate\n",
        "alternative": (
            "        if key not in merged:\n"
            "            merged[key] = candidate\n"
            "        else:\n"
            "            merged[key] = pick_latest(merged[key], candidate)\n"
        ),
        "wrong": "        if key not in merged:\n            merged[key] = candidate\n",
    },
    "T18_parse_bool": {
        "file": "src/confkit/booleans.py",
        "buggy": (
            "    if isinstance(value, bool):\n"
            "        return value\n"
            "    return bool(value)\n"
        ),
        "alternative": (
            "    if isinstance(value, bool):\n"
            "        return value\n"
            "    if isinstance(value, str):\n"
            "        text = value.strip().lower()\n"
            "        if text not in TRUE_WORDS and text not in FALSE_WORDS:\n"
            '            raise ValueError(f"not a boolean: {value}")\n'
            "        return text in TRUE_WORDS\n"
            "    return bool(value)\n"
        ),
        "wrong": (
            "    if isinstance(value, bool):\n"
            "        return value\n"
            "    if isinstance(value, str):\n"
            "        text = value.strip().lower()\n"
            "        if text in TRUE_WORDS:\n"
            "            return False\n"
            "        if text in FALSE_WORDS:\n"
            "            return True\n"
            '        raise ValueError(f"not a boolean: {value}")\n'
            "    return bool(value)\n"
        ),
    },
    "T19_to_decimal": {
        "file": "src/moneykit/amounts.py",
        "buggy": (
            "    if isinstance(value, float):\n"
            "        return Decimal(value)\n"
            "    try:\n"
        ),
        "alternative": (
            "    if isinstance(value, float):\n"
            "        return Decimal(repr(value))\n"
            "    try:\n"
        ),
        "wrong": (
            "    if isinstance(value, float):\n"
            "        return Decimal(round(value, 2))\n"
            "    try:\n"
        ),
    },
    "T22_json_dumps": {
        "file": "src/payloadkit/serialise.py",
        "buggy": (
            "            ensure_ascii=True,\n"
            "            sort_keys=False,\n"
            '            separators=(",", ": "),\n'
        ),
        "alternative": (
            "            ensure_ascii=False,\n"
            "            sort_keys=True,\n"
            '            separators=(",", ":"),\n'
        ),
        "wrong": (
            "            ensure_ascii=False,\n"
            "            sort_keys=True,\n"
            '            separators=(", ", ": "),\n'
        ),
    },
    "T23_parse_flags": {
        "edits": [
            {
                "file": "src/clikit/options.py",
                "buggy": "import argparse\n",
                "alternative": "import argparse\n\nfrom .flags import to_bool\n",
                "wrong": "import argparse\n\nfrom .flags import to_bool\n",
            },
            {
                "file": "src/clikit/options.py",
                "buggy": (
                    '    parser.add_argument("--verbose", type=bool, default=False)'
                ),
                "alternative": (
                    '    parser.add_argument("--verbose", type=to_bool, default=False)'
                ),
                "wrong": (
                    '    parser.add_argument("--verbose", type=to_bool, default=True)'
                ),
            },
        ],
    },
    "T24_join_path": {
        "file": "src/pathmont/join.py",
        "buggy": "    return posixpath.join(base, *parts)",
        "alternative": (
            "    cleaned = [\n"
            '        require_path(part, "part").lstrip("/") for part in parts\n'
            "    ]\n"
            "    return posixpath.join(base, *cleaned)"
        ),
        "wrong": "    return posixpath.normpath(posixpath.join(base, *parts))",
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
    "T14_shipping_fee": {
        "edits": [
            {
                "file": "src/logistics/units.py",
                "buggy": '    if normalized == "g":\n        return amount',
                "alternative": (
                    '    if normalized == "g":\n'
                    '        return amount * Decimal("0.001")'
                ),
                "wrong": (
                    '    if normalized == "g":\n'
                    '        return amount / Decimal("100")'
                ),
            },
            {
                "file": "src/logistics/parcels.py",
                "buggy": (
                    '    weights = [parse_parcel(item)["weight_kg"] for item in parcels]\n'
                    "    if not weights:\n"
                    '        return Decimal("0")\n'
                    '    return sum(weights, start=Decimal("0")) / len(weights)'
                ),
                "alternative": (
                    "    return sum(\n"
                    '        (parse_parcel(item)["weight_kg"] for item in parcels),\n'
                    '        start=Decimal("0"),\n'
                    "    )"
                ),
                "wrong": (
                    '    weights = [parse_parcel(item)["weight_kg"] for item in parcels]\n'
                    "    if not weights:\n"
                    '        return Decimal("0")\n'
                    '    return sum(weights, start=Decimal("0")) / len(weights)'
                ),
            },
        ],
    },
    "T20_multi_key_sort": {
        "edits": [
            {
                "file": "src/recordkit/keys.py",
                "buggy": "return sorted(records, key=record_key, reverse=True)",
                "alternative": "return sorted(records, key=record_key)",
                "wrong": "return sorted(records, key=record_key, reverse=True)",
            },
            {
                "file": "src/recordkit/grouping.py",
                "buggy": 'department: [record["name"] for record in members]',
                "alternative": (
                    'department: [record["name"] for record in order_records(members)]'
                ),
                "wrong": 'department: [record["name"] for record in members]',
            },
        ],
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


def variant_edits(variant: dict) -> list[dict]:
    if "edits" in variant:
        return variant["edits"]
    return [variant]


def check_task(task_dir: Path, variant: dict) -> list[str]:
    errors = []
    edits = variant_edits(variant)
    for edit in edits:
        source = task_dir / "repo" / edit["file"]
        text = source.read_text(encoding="utf-8")
        if text.count(edit["buggy"]) != 1:
            return [f"buggy line not found exactly once in {edit['file']}"]

    for name in ("alternative", "wrong"):
        with tempfile.TemporaryDirectory(prefix=f"variant_{task_dir.name}_") as temp:
            work = Path(temp) / "repo"
            shutil.copytree(task_dir / "repo", work)
            for edit in edits:
                target = work / edit["file"]
                content = target.read_text(encoding="utf-8")
                target.write_text(
                    content.replace(edit["buggy"], edit[name], 1),
                    encoding="utf-8",
                    newline="\n",
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
