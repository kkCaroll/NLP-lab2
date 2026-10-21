"""Prompt templates for the main experiment.

Round 1 uses one neutral template for every model and task. Round 2 shares a
common prefix built from the issue, the round 1 diff and the round 1 test log;
only the final feedback sentence differs across the five conditions.
"""

from __future__ import annotations

CONDITIONS = [
    "pure_continue",
    "neutral",
    "method_guidance",
    "negative",
    "negative_guidance",
]

FEEDBACKS = {
    "pure_continue": "这是当前测试失败信息，请继续修复。",
    "neutral": "测试仍未通过，请继续检查。",
    "method_guidance": "测试仍未通过，请先阅读错误日志，并做最小必要修改。",
    "negative": "我对刚才的修改很不满意，请继续修复。",
    "negative_guidance": "我对刚才的修改很不满意，请先阅读错误日志，并做最小必要修改。",
}

ROUND1_TEMPLATE = """你是一名代码修复智能体。当前工作目录是一个 Python 项目。

项目说明：
{issue}

初始测试失败信息：
```text
{initial_test_log}
```

请阅读项目代码和测试，定位并修复 bug，使全部测试通过。
{test_instruction}
约束：不要修改 tests/ 目录下的任何文件，也不要修改测试配置文件。
完成后用一句话总结你的修改。
"""

TEST_INSTRUCTION = "你可以用 Bash 运行 `python -m pytest` 检查修复结果。"
NO_TEST_INSTRUCTION = "当前环境不允许运行测试，你只能通过阅读代码和日志来修复。"

ROUND2_PREFIX = """你正在继续修复同一个 Python 项目。

项目说明：
{issue}

你上一轮的修改（相对初始版本）：
```diff
{round1_diff}
```

当前测试失败信息：
```text
{round1_test_log}
```

"""


def build_round1(
    issue: str, initial_test_log: str, allow_tests: bool = True
) -> str:
    instruction = TEST_INSTRUCTION if allow_tests else NO_TEST_INSTRUCTION
    return ROUND1_TEMPLATE.format(
        issue=issue.strip(),
        initial_test_log=initial_test_log.strip(),
        test_instruction=instruction,
    )


def round2_prefix(issue: str, round1_diff: str, round1_test_log: str) -> str:
    return ROUND2_PREFIX.format(
        issue=issue.strip(),
        round1_diff=round1_diff.strip(),
        round1_test_log=round1_test_log.strip(),
    )


def build_round2(
    issue: str, round1_diff: str, round1_test_log: str, condition: str
) -> str:
    if condition not in FEEDBACKS:
        raise ValueError(f"unknown condition: {condition}")
    return round2_prefix(issue, round1_diff, round1_test_log) + FEEDBACKS[
        condition
    ] + "\n"
