#!/usr/bin/env python3
"""Build blinded qualitative packets and a blank coding sheet.

The script reads the thirty-one sampled branch episodes listed in
RECORD/analysis/qualitative/qualitative_samples.csv, assigns anonymous
identifiers, and writes coding material without model names, condition names or
task names. The mapping stays in a separate manifest that the coder should not
open until coding is complete.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "RECORD" / "analysis" / "qualitative" / "qualitative_samples.csv"
DEFAULT_OUTPUT = ROOT / "RECORD" / "analysis" / "deepening"
CONDITIONS = [
    "pure_continue",
    "neutral",
    "method_guidance",
    "negative",
    "negative_guidance",
]
CODING_FIELDS = [
    "no_edit",
    "reads_log_first",
    "locates_callers",
    "only_target_lines",
    "rewrites_function",
    "unrelated_file",
    "defensive_branch",
    "reverted_previous",
    "claims_done_unverified",
    "evidence",
    "notes",
]
REDACTED_SUMMARY_FIELDS = [
    "all_passed",
    "edit_lines",
    "edit_files",
    "edit_file_count",
    "edit_ratio",
    "over_edit",
    "unrelated_files",
    "test_tampered",
    "tool_calls",
    "edits",
    "steps",
    "tool_breakdown",
    "first_edit_after_read",
    "budget_exhausted",
    "budget_reasons",
    "timed_out",
    "exit_code",
    "duration_s",
    "results",
]
ID_KEYS = {"sessionID", "messageID", "callID", "id", "snapshot"}
CONDITION_SEGMENT_RE = re.compile(
    r"(?i)([\\/])"
    r"(pure_continue|neutral|method_guidance|negative_guidance|negative)"
    r"(?=[\\/])"
)
TEMP_PATH_RE = re.compile(
    r"(?i)[A-Za-z]:[\\/](?:[^\\/\"'\s]+[\\/])*?Temp[\\/]exp_[^\\/\"'\s]+"
)
TMP_PATH_RE = re.compile(r"/tmp/exp_[^/\"'\s]+")
TEMP_REL_RE = re.compile(r"(?i)Temp[\\/]+exp_[^\\/\"'\s]+")
HOME_RE = re.compile(r"(?i)[A-Za-z]:[\\/]+Users[\\/]+[^\\/\"'\s]+")


def repo_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def scrub(value, root_text: str, task: str, model_slug: str):
    if isinstance(value, dict):
        return {
            key: "[redacted]" if key in ID_KEYS else scrub(item, root_text, task, model_slug)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [scrub(item, root_text, task, model_slug) for item in value]
    if isinstance(value, str):
        text = value.replace(root_text, "<REPO>")
        text = text.replace(str(ROOT), "<REPO>")
        text = text.replace(task, "<TASK>")
        text = text.replace(model_slug, "<MODEL>")
        text = CONDITION_SEGMENT_RE.sub(r"\1<CONDITION>", text)
        text = TEMP_PATH_RE.sub("<WORKSPACE>", text)
        text = TMP_PATH_RE.sub("<WORKSPACE>", text)
        text = TEMP_REL_RE.sub("<WORKSPACE>", text)
        text = HOME_RE.sub("<HOME>", text)
        return text
    return value


def read_events(path: Path) -> tuple[list[dict], list[str]]:
    events: list[dict] = []
    stderr: list[str] = []
    collecting = False
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if stripped.startswith("--- STDERR ---"):
            collecting = True
            continue
        if collecting:
            stderr.append(line)
            continue
        if not stripped:
            continue
        try:
            events.append(json.loads(stripped))
        except json.JSONDecodeError:
            stderr.append(line)
    return events, stderr


def write_packet(
    sample_id: str,
    row: dict,
    output: Path,
    test_instructions: str,
) -> tuple[Path, dict]:
    source = (ROOT / row["events_path"]).parent
    packet = output / "blinded" / sample_id
    packet.mkdir(parents=True, exist_ok=True)

    events, stderr = read_events(ROOT / row["events_path"])
    task = row["task"]
    model_slug = row["model"].replace("/", "_").replace(":", "_")
    root_text = ROOT.as_posix()
    cleaned = [scrub(event, root_text, task, model_slug) for event in events]
    with (packet / "events.jsonl").open("w", encoding="utf-8", newline="\n") as handle:
        for event in cleaned:
            handle.write(json.dumps(event, ensure_ascii=False) + "\n")
    (packet / "stderr.txt").write_text("\n".join(stderr), encoding="utf-8")

    for name in ("diff_cumulative.patch", "diff_delta.patch"):
        source_file = source / name
        target = packet / name
        if source_file.exists():
            target.write_text(
                source_file.read_text(encoding="utf-8", errors="replace"),
                encoding="utf-8",
            )
        else:
            target.write_text("", encoding="utf-8")

    round1 = source.parent.parent / "round1" / "diff_cumulative.patch"
    if round1.exists():
        (packet / "round1_diff.patch").write_text(
            round1.read_text(encoding="utf-8", errors="replace"),
            encoding="utf-8",
        )
    else:
        (packet / "round1_diff.patch").write_text("", encoding="utf-8")

    texts = []
    for index, event in enumerate(events, 1):
        part = event.get("part", {})
        if part.get("type") == "text" and part.get("text", "").strip():
            texts.append(f"[text {index}]\n{part['text'].strip()}\n")
    (packet / "final_text.txt").write_text(
        "\n".join(texts) if texts else "(no assistant text)\n",
        encoding="utf-8",
    )

    summary = json.loads((ROOT / row["summary_path"]).read_text(encoding="utf-8"))
    redacted = {key: summary.get(key) for key in REDACTED_SUMMARY_FIELDS}
    meta_path = ROOT / "tasks" / task / "meta.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        redacted["allowed_files"] = meta.get("allowed_files", [])
    else:
        redacted["allowed_files"] = []
    (packet / "summary_redacted.json").write_text(
        json.dumps(redacted, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    (packet / "README.txt").write_text(test_instructions, encoding="utf-8")
    manifest = {
        "sample_id": sample_id,
        "model": row["model"],
        "task": task,
        "condition": row["condition"],
        "outcome": row["outcome"],
        "source": repo_path(source),
    }
    return packet, manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", default=str(SAMPLES))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--seed", type=int, default=20261022)
    parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite an existing coding sheet that already has codes",
    )
    args = parser.parse_args()

    samples = Path(args.samples)
    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output
    with samples.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit("no samples found")

    coding_path = output / "coding_sheet.csv"
    if coding_path.exists() and not args.force:
        with coding_path.open(encoding="utf-8-sig", newline="") as handle:
            existing = list(csv.DictReader(handle))
        if any(
            row.get(field, "").strip()
            for row in existing
            for field in CODING_FIELDS
        ):
            raise SystemExit(
                f"{coding_path} already contains codes; use --force to overwrite"
            )

    random.Random(args.seed).shuffle(rows)
    instructions = (
        "质性编码材料\n\n"
        "按 PLAN/05a_coding_manual.md 编码。只使用本目录中的事件流、diff、"
        "最终文本与脱敏 summary，不打开 prompt.txt，不查找原始运行目录。\n\n"
        "编码完成后填写 ../coding_sheet.csv，sample_id 与本目录名一致。\n"
        "全部编码完成前不要打开 ../blinding_manifest.csv。\n"
    )

    output.mkdir(parents=True, exist_ok=True)
    manifest_rows = []
    for index, row in enumerate(rows, 1):
        sample_id = f"S{index:02d}"
        _, manifest = write_packet(sample_id, row, output, instructions)
        manifest_rows.append(manifest)

    with (output / "blinding_manifest.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(manifest_rows[0].keys()))
        writer.writeheader()
        writer.writerows(manifest_rows)

    with coding_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["sample_id", *CODING_FIELDS]
        )
        writer.writeheader()
        for index in range(1, len(rows) + 1):
            writer.writerow({"sample_id": f"S{index:02d}"})

    print(f"wrote {len(rows)} blinded packets to {repo_path(output / 'blinded')}")
    print(f"wrote {repo_path(coding_path)}")
    print(f"wrote {repo_path(output / 'blinding_manifest.csv')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
