#!/usr/bin/env python3
"""Count Bash attempts from OpenCode event streams.

The runner records permission denials, but an unavailable tool is reported as
an invalid call whose input names the intended tool. This script counts both
forms so a no-test ablation can be audited from the raw events.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def count_events(path: Path) -> dict:
    counts = {
        "bash_attempts": 0,
        "bash_completed": 0,
        "bash_permission_denied": 0,
        "bash_unavailable": 0,
        "invalid_calls": 0,
        "edit_calls": 0,
    }
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") != "tool_use":
            continue
        part = event.get("part", {}) or {}
        tool = str(part.get("tool", ""))
        state = part.get("state", {}) or {}
        intended = ""
        if tool == "invalid":
            counts["invalid_calls"] += 1
            intended = str((state.get("input", {}) or {}).get("tool", ""))
        if tool == "bash" or intended == "bash":
            counts["bash_attempts"] += 1
            message = " ".join(
                str(value or "")
                for value in (
                    state.get("error"),
                    (state.get("input", {}) or {}).get("error"),
                    state.get("output"),
                )
            )
            if "prevents you from using" in message:
                counts["bash_permission_denied"] += 1
            elif "unavailable tool" in message:
                counts["bash_unavailable"] += 1
            elif state.get("status") == "completed":
                counts["bash_completed"] += 1
        if tool in {"edit", "write", "patch"}:
            counts["edit_calls"] += 1
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument(
        "--output",
        default=None,
        help="CSV path; defaults to RECORD/analysis/tool_attempts_<run>.csv",
    )
    args = parser.parse_args()
    run_root = ROOT / "RECORD" / "runs" / args.run_id
    rows = []
    for path in sorted(run_root.rglob("events.jsonl")):
        relative = path.relative_to(run_root).parts
        model = relative[0]
        task = relative[1]
        episode = "/".join(relative[2:-1])
        counts = count_events(path)
        rows.append(
            {
                "model": model,
                "task": task,
                "episode": episode,
                **counts,
            }
        )
    output = (
        Path(args.output)
        if args.output
        else ROOT / "RECORD" / "analysis" / f"tool_attempts_{args.run_id}.csv"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    total = sum(row["bash_attempts"] for row in rows)
    completed = sum(row["bash_completed"] for row in rows)
    print(
        f"{len(rows)} episodes, bash attempts {total}, completed {completed}, "
        f"wrote {output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
