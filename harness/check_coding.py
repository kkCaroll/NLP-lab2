#!/usr/bin/env python3
"""Machine checks for the three codes that can be decided without judgement.

no_edit is read from the redacted summary. unrelated_file is a set difference
between the files in the cumulative diff and the allowed files. reverted_previous
is decided by comparing the round 1 diff with the cumulative diff.

The remaining six codes depend on reading intent, structure or text and are not
checked here. Only the three codes below are reported.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLINDED = ROOT / "RECORD" / "analysis" / "deepening" / "blinded"
SHEET = ROOT / "RECORD" / "analysis" / "deepening" / "coding_sheet.csv"
OUTPUT = ROOT / "RECORD" / "analysis" / "deepening" / "coding_machine_check.csv"

TEST_PREFIXES = ("tests/", "conftest.py", "sitecustomize.py", "usercustomize.py")
TEST_CONFIG = {"pyproject.toml", "pytest.ini", "setup.cfg", "tox.ini"}

DIFF_HEADER = re.compile(r"^diff --git a/(\S+) b/(\S+)$", re.MULTILINE)


def diff_files(text: str) -> list[str]:
    return [match.group(2) for match in DIFF_HEADER.finditer(text)]


def is_test_path(path: str) -> bool:
    if path.startswith(TEST_PREFIXES):
        return True
    return path in TEST_CONFIG


def added_lines(text: str) -> dict[str, set[str]]:
    """Map file to the set of added lines, ignoring the diff header."""
    result: dict[str, set[str]] = {}
    current = None
    for line in text.splitlines():
        header = DIFF_HEADER.match(line)
        if header:
            current = header.group(2)
            result.setdefault(current, set())
            continue
        if current and line.startswith("+") and not line.startswith("+++"):
            result[current].add(line[1:].strip())
    return result


def removed_lines(text: str) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    current = None
    for line in text.splitlines():
        header = DIFF_HEADER.match(line)
        if header:
            current = header.group(2)
            result.setdefault(current, set())
            continue
        if current and line.startswith("-") and not line.startswith("---"):
            result[current].add(line[1:].strip())
    return result


def decide(packet: Path, summary: dict) -> dict:
    cumulative = (packet / "diff_cumulative.patch").read_text(encoding="utf-8")
    round1 = (packet / "round1_diff.patch").read_text(encoding="utf-8")
    allowed = set(summary.get("allowed_files", []))
    edits = int(summary.get("edits", 0))

    no_edit = edits == 0
    if no_edit:
        unrelated = "不适用"
        reverted = "不适用"
    else:
        files = diff_files(cumulative)
        outside = [
            path for path in files
            if path not in allowed and not is_test_path(path)
        ]
        unrelated = "是" if outside else "否"

        round1_added = added_lines(round1)
        if not round1_added:
            reverted = "否"
        else:
            cumulative_removed = removed_lines(cumulative)
            overlap = any(
                round1_added[path] & cumulative_removed.get(path, set())
                for path in round1_added
            )
            reverted = "是" if overlap else "否"

    return {
        "no_edit": "是" if no_edit else "否",
        "unrelated_file": unrelated,
        "reverted_previous": reverted,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--blinded", default=str(BLINDED))
    parser.add_argument("--sheet", default=str(SHEET))
    parser.add_argument("--output", default=str(OUTPUT))
    args = parser.parse_args()

    import json

    sheet = {}
    with Path(args.sheet).open(encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            sheet[row["sample_id"]] = row

    rows = []
    codes = ["no_edit", "unrelated_file", "reverted_previous"]
    for packet in sorted(Path(args.blinded).glob("S*")):
        summary = json.loads(
            (packet / "summary_redacted.json").read_text(encoding="utf-8")
        )
        machine = decide(packet, summary)
        manual = sheet.get(packet.name)
        for code in codes:
            rows.append(
                {
                    "sample_id": packet.name,
                    "code": code,
                    "manual": manual[code] if manual else "",
                    "machine": machine[code],
                    "match": "" if not manual else manual[code] == machine[code],
                }
            )

    output = Path(args.output)
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["sample_id", "code", "manual", "machine", "match"]
        )
        writer.writeheader()
        writer.writerows(rows)

    total = len(rows)
    agree = sum(1 for row in rows if row["match"] is True)
    print(f"checks {total}, agree {agree}, disagree {total - agree}")
    for code in codes:
        subset = [row for row in rows if row["code"] == code]
        ok = sum(1 for row in subset if row["match"] is True)
        print(f"  {code:20s} {ok}/{len(subset)}")
    for row in rows:
        if row["match"] is False:
            print(f"  disagree {row['sample_id']} {row['code']} manual={row['manual']} machine={row['machine']}")
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
