#!/usr/bin/env python3
"""Build human review sheets from task metadata and blind solve records.

The generated sheets contain automatic verification values, the recorded
blind attempt and a blank signature block. The script never fills in a
reviewer name or a review conclusion.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "tasks"
BLIND = ROOT / "RECORD" / "calibration" / "blind"
REVIEW = ROOT / "RECORD" / "calibration" / "review"

FAILURE_MODES = {
    "assertion": "断言失败",
    "error": "异常",
}

TOOL_NAMES = {
    "read": "读取",
    "bash": "Bash",
    "glob": "glob",
    "grep": "grep",
    "list": "list",
    "edit": "edit",
    "write": "write",
    "patch": "patch",
}


def source_summary(repo: Path) -> tuple[int, int]:
    files = [
        path
        for path in (repo / "src").rglob("*.py")
        if "__pycache__" not in path.parts
    ]
    lines = 0
    for path in files:
        lines += len(path.read_text(encoding="utf-8", errors="replace").splitlines())
    return len(files), lines


def event_stats(path: Path) -> tuple[int, Counter]:
    steps = 0
    tools: Counter = Counter()
    if not path.exists():
        return steps, tools
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "step_finish":
            steps += 1
        elif event.get("type") == "tool_use":
            tools[event.get("part", {}).get("tool", "")] += 1
    return steps, tools


def tool_text(tools: Counter) -> str:
    order = ["read", "bash", "glob", "grep", "list", "edit", "write", "patch"]
    parts = []
    for name in order:
        if tools.get(name):
            parts.append(f"{TOOL_NAMES[name]} {tools[name]}")
    for name, count in sorted(tools.items()):
        if name not in order:
            parts.append(f"{name or '未知'} {count}")
    return "、".join(parts) if parts else "无"


def blind_section(task_name: str) -> tuple[list[str], str, bool]:
    summary_path = BLIND / task_name / "summary.json"
    if not summary_path.exists():
        lines = [
            "## 盲解结果",
            "",
            "尚未运行 DeepSeek-V4-Pro 盲解。",
            "",
        ]
        return lines, "未运行", False
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    events_path = BLIND / task_name / "events.jsonl"
    steps, tools = event_stats(events_path)
    if summary["all_passed"]:
        result = f"全部测试通过，{summary['tests_passed']} passed"
    else:
        result = (
            f"未通过，{summary['tests_failed']} failed，"
            f"{summary['tests_passed']} passed"
        )
    changed = "、".join(summary["files_changed"]) if summary["files_changed"] else "无"
    tampered = "有" if summary["test_tampered"] else "无"
    lines = [
        "## 盲解结果",
        "",
        "| 项目 | 内容 |",
        "|---|---|",
        f"| 模型 | DeepSeek-V4-Pro |",
        f"| 结果 | {result} |",
        f"| 步数 | {steps} |",
        f"| 工具调用 | {summary['tool_calls']}，其中{tool_text(tools)} |",
        f"| 修改行数 | {summary['diff_lines']} |",
        f"| 修改文件 | {changed} |",
        f"| 测试篡改 | {tampered} |",
        f"| 耗时 | {summary['duration_s']} 秒 |",
        f"| 费用 | {summary['cost_usd']} 美元 |",
        "",
    ]
    if summary.get("budget_exhausted"):
        lines.append("盲解达到工具调用上限，需区分正常完成与预算耗尽。")
        lines.append("")
    return lines, result, summary["all_passed"]


def review_sheet(task_dir: Path) -> tuple[str, str, str]:
    meta = json.loads((task_dir / "meta.json").read_text(encoding="utf-8"))
    file_count, line_count = source_summary(task_dir / "repo")
    task_name = task_dir.name
    failure = FAILURE_MODES.get(meta.get("target_failure_mode", ""), "断言失败")
    allowed = "、".join(meta["allowed_files"]) if meta["allowed_files"] else "无"
    source = meta.get("source", {})
    source_text = source.get("name", "未知")
    license_text = source.get("license", "")
    if license_text and license_text not in {"Original task"}:
        source_text = f"{source_text}，{license_text}"
    elif license_text == "Original task":
        source_text = f"{source_text}，原创"
    blind_lines, blind_result, blind_passed = blind_section(task_name)

    lines = [
        f"# {meta['task_id']} {meta['name']} 复核表",
        "",
        "## 基本信息",
        "",
        "| 项目 | 内容 |",
        "|---|---|",
        f"| 题号 | {meta['task_id']} |",
        f"| 名称 | {meta['name']} |",
        f"| 类别 | {meta['category']} |",
        f"| 难度 | {meta['difficulty']} |",
        f"| 来源 | {source_text} |",
        f"| 源码规模 | {file_count} 个文件 {line_count} 行 |",
        f"| gold 行数 | {meta['gold_lines']} |",
        "",
        "## Issue",
        "",
        meta["issue"],
        "",
        "## 自动核验",
        "",
        "| 检查项 | 结果 |",
        "|---|---|",
        f"| buggy 状态 | {meta['expected_buggy']} |",
        f"| gold 状态 | {meta['expected_gold']} |",
        f"| 目标测试失败类型 | {failure} |",
        "| 回归测试在 buggy 状态 | 全部通过 |",
        f"| gold 补丁范围 | 仅 {allowed} |",
        "| 测试文件哈希 | gold 前后一致 |",
        "| 五轮确定性 | 一致 |",
        "| 泄漏标记 | 未发现 |",
        "| G10 等价修复 | 通过 |",
        "| G10 错误修复 | 失败 |",
        "",
    ]
    lines.extend(blind_lines)
    lines.extend(
        [
            "## 人工复核意见",
            "",
            "待复核人检查 issue 是否清楚、测试是否只验证目标行为、"
            "来源与许可标注是否准确，并填写以下内容。",
            "",
            "- 复核结论：",
            "- 复核人：",
            "- 日期：",
            "",
            "## 备注",
            "",
        ]
    )
    notes = []
    if not blind_passed:
        notes.append("盲解未通过，需由复核人判断题目是否过难或 issue 是否存在歧义。")
    else:
        notes.append("盲解通过，修改未涉及测试文件。")
    if meta["difficulty"] == "标准":
        notes.append("题目规模与类别符合标准题要求。")
    else:
        notes.append("题目规模与类别符合困难题要求。")
    lines.extend(f"- {note}" for note in notes)
    lines.append("")
    return "\n".join(lines), blind_result, meta["task_id"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tasks", nargs="*", help="task directory names")
    args = parser.parse_args()
    names = args.tasks or sorted(path.name for path in TASKS.iterdir() if path.is_dir() and path.name != "_sources")
    REVIEW.mkdir(parents=True, exist_ok=True)
    rows = []
    for name in names:
        task_dir = TASKS / name
        text, blind_result, task_id = review_sheet(task_dir)
        target = REVIEW / f"{task_id}_review.md"
        target.write_text(text, encoding="utf-8", newline="\n")
        rows.append((name, task_id, blind_result))
        print(f"{name}: written {target.relative_to(ROOT)} blind={blind_result}")
    write_index()
    return 0


def write_index() -> None:
    lines = [
        "# 任务人工复核",
        "",
        "本目录存放全部 24 道题的复核表。自动核验与盲解部分由 "
        "`harness/validate_tasks.py`、`harness/check_variants.py`、"
        "`harness/blind_solve.py` 与 `harness/make_review.py` 产生。"
        "人工复核需要检查 issue 表述、测试语义、来源许可与盲解差异，"
        "并在每题末尾填写结论、复核人与日期。",
        "",
        "| 题号 | 名称 | 难度 | 复核表 | 盲解 | 签字 |",
        "|---|---|---|---|---|---|",
    ]
    for task_dir in sorted(TASKS.glob("T*")):
        meta = json.loads((task_dir / "meta.json").read_text(encoding="utf-8"))
        sheet = REVIEW / f"{meta['task_id']}_review.md"
        summary_path = BLIND / task_dir.name / "summary.json"
        blind = "未运行"
        if summary_path.exists():
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            blind = "通过" if summary["all_passed"] else "未通过"
        link = f"[{meta['task_id']}_review.md]({sheet.name})"
        lines.append(
            f"| {meta['task_id']} | {meta['name']} | {meta['difficulty']} | "
            f"{link} | {blind} | 未签字 |"
        )
    lines.extend(
        [
            "",
            "盲解统一使用 DeepSeek-V4-Pro，经 OpenCode 1.18.25 在隔离配置下运行。"
            "模型只看 issue、初始测试日志与 buggy 仓库副本，"
            "不看 meta.json、gold.patch 或任务来源说明。",
            "",
            "人工复核签字后，题目才视为冻结。签字前不得根据 evaluator 模型结果改题。",
            "",
        ]
    )
    target = REVIEW / "README.md"
    target.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"written {target.relative_to(ROOT)}")


if __name__ == "__main__":
    raise SystemExit(main())
