#!/usr/bin/env python3
"""Build the candidate pool for the 24-task repair experiment.

This script reads local source snapshots only. It does not execute any
downloaded code. Outputs PLAN/03_candidate_pool.json and PLAN/03_candidate_pool.md.
"""

from __future__ import annotations

import ast
import json
import re
import sys
import warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QB_DIR = ROOT / "tasks" / "_sources" / "QuixBugs"
BCB_PARQUET = ROOT / "tasks" / "_sources" / "bigcodebench" / "bigcodebench-v0.1.4.parquet"
OUT_JSON = ROOT / "PLAN" / "03_candidate_pool.json"
OUT_MD = ROOT / "PLAN" / "03_candidate_pool.md"

# Manual curation. Category labels follow the seven required error types.
QB_SELECTION = [
    ("find_first_in_sorted", "边界条件/排序查找", "标准", "二分查找重复元素，适合拆分目标与回归用例"),
    ("find_in_sorted", "边界条件/排序查找", "标准", "二分查找边界，适合半开区间错误"),
    ("gcd", "函数逻辑", "标准", "递归与取模，适合一行逻辑错误"),
    ("next_palindrome", "函数逻辑", "标准", "进位与回文边界，适合边界逻辑"),
    ("possible_change", "函数逻辑/数据处理", "标准", "动态规划零钱问题，测试用例较多"),
    ("hanoi", "函数逻辑", "标准", "递归移动序列，适合步骤与边界"),
    ("quicksort", "排序查找", "标准", "分区与递归，测试用例最多"),
    ("kth", "排序查找", "标准", "选择第 k 小，适合边界与重复值"),
    ("mergesort", "排序查找", "标准", "归并与稳定性，适合回归测试"),
    ("bucketsort", "排序查找", "标准", "桶排序边界与空桶"),
    ("to_base", "类型转换", "标准", "整数转任意进制，适合字符映射"),
    ("sqrt", "类型转换", "标准", "整数平方根与精度边界"),
    ("rpn_eval", "数据处理", "标准", "逆波兰表达式求值，适合栈与错误处理"),
    ("shunting_yard", "数据处理", "标准", "中缀转后缀，适合运算符优先级"),
    ("flatten", "数据处理", "标准", "嵌套列表展平，适合递归与类型判断"),
    ("wrap", "数据处理", "标准", "文本换行，适合边界与空白"),
    ("max_sublist_sum", "函数逻辑", "标准", "最大子数组和，适合负数与空输入"),
    ("lis", "函数逻辑", "标准", "最长递增子序列，适合边界与重复值"),
    ("levenshtein", "函数逻辑", "标准", "编辑距离，适合动态规划边界"),
    ("knapsack", "函数逻辑", "标准", "背包问题，适合容量与物品边界"),
    ("bitcount", "函数逻辑", "标准", "位计数，适合负数与零边界"),
    ("get_factors", "函数逻辑", "标准", "因子分解，适合完全平方与素数"),
]

BCB_SELECTION = [
    ("BigCodeBench/25", "数据处理/API 参数误用", "标准", "JSON 序列化、zlib 压缩、base64 编码链"),
    ("BigCodeBench/178", "数据处理/正则", "标准", "从 JSON 响应中提取 IP，正则与 JSON 组合"),
    ("BigCodeBench/202", "数据处理/正则", "标准", "从 JSON 字符串中提取 URL，适合数据清洗"),
    ("BigCodeBench/254", "类型转换", "标准", "小数平方根与 JSON 编码，适合精度与类型"),
    ("BigCodeBench/270", "正则/数据处理", "标准", "词频统计，测试依赖 faker，需重写"),
    ("BigCodeBench/433", "API 参数误用", "标准", "HMAC 签名校验，API 参数与编码组合"),
    ("BigCodeBench/464", "类型转换/API 参数误用", "标准", "JSON 编码 Decimal 与 datetime，测试依赖 pytz，需重写"),
    ("BigCodeBench/466", "API 参数误用", "标准", "JSON 编码 Enum，适合自定义 encoder"),
    ("BigCodeBench/667", "排序查找", "标准", "heapq 取前 n 个高频字母"),
    ("BigCodeBench/682", "数据处理", "标准", "嵌套字典聚合与 Counter"),
    ("BigCodeBench/709", "正则/数据处理", "标准", "base64、HTML 实体、空白归一化"),
    ("BigCodeBench/733", "正则/函数逻辑", "标准", "停用词计数，正则分词"),
    ("BigCodeBench/741", "数据处理", "标准", "按首字符分组求和，groupby"),
    ("BigCodeBench/747", "正则/类型转换", "标准", "提取数字并求平方根和"),
    ("BigCodeBench/761", "数据处理/正则", "标准", "JSON 清洗、邮箱替换、值频次"),
    ("BigCodeBench/766", "正则", "标准", "多模式计数，适合正则边界"),
    ("BigCodeBench/769", "数据处理/排序查找", "标准", "嵌套列表展平与众数"),
    ("BigCodeBench/775", "正则/数据处理", "标准", "按最后一个连字符切分并统计字母"),
    ("BigCodeBench/851", "正则/数据处理", "标准", "textwrap 与整词替换"),
    ("BigCodeBench/867", "正则", "标准", "删除 ASCII 标点"),
    ("BigCodeBench/893", "API 参数误用/数据处理", "标准", "日志时间解析与平均，datetime 组合"),
    ("BigCodeBench/911", "数据处理", "标准", "字母映射与 reduce 乘积"),
    ("BigCodeBench/928", "数据处理/排序查找", "困难候选", "生成全部双字母组合并统计，规模较大"),
    ("BigCodeBench/931", "正则/数据处理", "标准", "清洗后统计相邻字母对"),
    ("BigCodeBench/932", "正则/排序查找", "标准", "最频繁双字母组合"),
    ("BigCodeBench/937", "正则/数据处理", "标准", "字母数字频次统计"),
    ("BigCodeBench/957", "正则/数据处理", "标准", "词数、字符数、唯一字符数"),
    ("BigCodeBench/972", "API 参数误用", "困难候选", "路径分隔与非法字符校验，适合改造为路径拼接任务"),
    ("BigCodeBench/1090", "数据处理/API 参数误用", "困难候选", "JSON 文件指针、ast 解析与键频次"),
    ("BigCodeBench/1098", "正则/排序查找", "标准", "去除 URL 后取 top N 词"),
    ("BigCodeBench/1126", "正则/API 参数误用", "标准", "清洗后 SHA256，适合正则与 API 组合"),
]


def parse_imports(code: str) -> set[str]:
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            tree = ast.parse(code)
    except SyntaxError:
        return set()
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            found.add(node.module.split(".")[0])
    return found


def quixbugs_candidates() -> list[dict]:
    out = []
    for name, category, fit, note in QB_SELECTION:
        src = QB_DIR / "python_programs" / f"{name}.py"
        fixed = QB_DIR / "correct_python_programs" / f"{name}.py"
        cases_file = QB_DIR / "json_testcases" / f"{name}.json"
        embedded = QB_DIR / "python_testcases" / f"test_{name}.py"
        cases = 0
        if cases_file.exists():
            cases = sum(1 for line in cases_file.read_text(encoding="utf-8").splitlines() if line.strip())
        out.append({
            "candidate_id": f"QB-{name}",
            "source": "QuixBugs",
            "source_id": name,
            "category": category,
            "difficulty_fit": fit,
            "loc": len(src.read_text(encoding="utf-8").splitlines()) if src.exists() else None,
            "test_cases": cases,
            "has_embedded_test": embedded.exists(),
            "has_buggy_version": src.exists(),
            "has_fixed_version": fixed.exists(),
            "notes": note,
        })
    return out


def bigcodebench_candidates() -> list[dict]:
    import pyarrow.parquet as pq

    table = pq.read_table(BCB_PARQUET)
    rows = {table.column("task_id")[i].as_py(): i for i in range(table.num_rows)}
    stdlib = set(sys.stdlib_module_names)
    out = []
    for task_id, category, fit, note in BCB_SELECTION:
        i = rows[task_id]
        prompt = table.column("complete_prompt")[i].as_py()
        solution = table.column("canonical_solution")[i].as_py()
        test = table.column("test")[i].as_py()
        libs = ast.literal_eval(table.column("libs")[i].as_py())
        test_imports = sorted(parse_imports(test))
        third_party = sorted(m for m in test_imports if m not in stdlib)
        flags = []
        if third_party:
            flags.append("test_third_party")
        if any(token in test for token in ["open(", "os.", "pathlib", "glob", "shutil", "subprocess", "socket", "smtplib", "urllib"]):
            flags.append("test_io_or_network")
        if any(token in test for token in ["random.", "time.", "datetime.now", "datetime.today"]):
            flags.append("test_nondeterminism")
        if len(re.findall(r"\bassert", test)) < 5:
            flags.append("weak_assertions")
        out.append({
            "candidate_id": f"BCB-{task_id.split('/')[-1]}",
            "source": "BigCodeBench",
            "source_id": task_id,
            "category": category,
            "difficulty_fit": fit,
            "libs": libs,
            "entry_point": table.column("entry_point")[i].as_py(),
            "solution_loc": len(solution.splitlines()),
            "test_loc": len(test.splitlines()),
            "asserts": len(re.findall(r"\bassert", test)),
            "test_methods": len(re.findall(r"^\s+def test_", test, re.M)),
            "test_imports": test_imports,
            "test_third_party": third_party,
            "risk_flags": flags,
            "notes": note,
        })
    return out


def render_markdown(pool: dict) -> str:
    lines = [
        "# 24 题候选池",
        "",
        f"> 生成时间：{pool['generated_at']}",
        "> 来源快照与许可见 `tasks/_sources/`，候选池只记录元数据，不复制源码。",
        "",
        "## 概览",
        "",
        f"- 候选总数：{pool['counts']['total']}",
        f"- QuixBugs：{pool['counts']['QuixBugs']}",
        f"- BigCodeBench：{pool['counts']['BigCodeBench']}",
        "- HumanEval：不进入主候选池，仅用于 harness 冒烟测试。",
        "",
        "## QuixBugs 候选",
        "",
        "| 编号 | 类别 | 适配难度 | 行数 | 用例数 | buggy | fixed | 备注 |",
        "|---|---|---|---:|---:|---|---|---|",
    ]
    for c in pool["candidates"]:
        if c["source"] != "QuixBugs":
            continue
        lines.append(
            f"| {c['candidate_id']} | {c['category']} | {c['difficulty_fit']} | "
            f"{c['loc']} | {c['test_cases']} | {c['has_buggy_version']} | "
            f"{c['has_fixed_version']} | {c['notes']} |"
        )
    lines += [
        "",
        "## BigCodeBench 候选",
        "",
        "| 编号 | 类别 | 适配难度 | 依赖 | 解法行数 | 断言数 | 测试方法数 | 测试第三方依赖 | 备注 |",
        "|---|---|---|---|---:|---:|---:|---|---|",
    ]
    for c in pool["candidates"]:
        if c["source"] != "BigCodeBench":
            continue
        deps = ", ".join(c["test_third_party"]) if c["test_third_party"] else "无"
        lines.append(
            f"| {c['candidate_id']} | {c['category']} | {c['difficulty_fit']} | "
            f"{', '.join(c['libs'])} | {c['solution_loc']} | {c['asserts']} | "
            f"{c['test_methods']} | {deps} | {c['notes']} |"
        )
    lines += [
        "",
        "## 使用规则",
        "",
        "1. 候选池不是最终题目集。最终 24 题按 12 标准加 12 困难选择，并保持七类错误覆盖。",
        "2. BigCodeBench 的原始测试只作为参考。入库前必须重写目标测试与回归测试，去掉第三方依赖和弱断言。",
        "3. QuixBugs 的 JSON 用例可以拆为目标用例与回归用例，但必须补充相邻模块或共享 helper 的回归测试。",
        "4. 困难题通过多文件包装实现，不直接按原题难度认定。共享 helper、多个调用方和回归陷阱是困难题的必要条件。",
        "5. 所有题目必须通过 G1 到 G12、V4-Pro 盲解和人工复核后才可冻结。",
        "",
        "## 已知限制",
        "",
        "- BigCodeBench 的 `libs` 字段不包含测试依赖。本脚本额外解析测试导入，但仍需人工检查。",
        "- 部分 BigCodeBench 测试使用 `faker`、`pytz` 或文件系统。候选池标出这些风险，入库前必须改写。",
        "- QuixBugs 与 BigCodeBench 都是公开基准，存在训练数据污染。最终题目需要改写标识符、常量和调用链。",
        "- 本脚本不执行下载代码，只做静态读取。",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    qb = quixbugs_candidates()
    bcb = bigcodebench_candidates()
    pool = {
        "generated_at": "2026-10-20",
        "sources": {
            "QuixBugs": {
                "path": "tasks/_sources/QuixBugs",
                "commit": "4257f44b0ff1181dedaedee6a447e133219fcebf",
                "license": "MIT",
            },
            "BigCodeBench": {
                "path": "tasks/_sources/bigcodebench/bigcodebench-v0.1.4.parquet",
                "version": "v0.1.4",
                "license": "Apache-2.0",
            },
        },
        "counts": {
            "total": len(qb) + len(bcb),
            "QuixBugs": len(qb),
            "BigCodeBench": len(bcb),
        },
        "candidates": qb + bcb,
    }
    OUT_JSON.write_text(json.dumps(pool, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_MD.write_text(render_markdown(pool), encoding="utf-8")
    print(f"wrote {OUT_JSON} and {OUT_MD}")
    print(pool["counts"])


if __name__ == "__main__":
    main()
