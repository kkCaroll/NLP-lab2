# 2026-10-20 T01 构造记录

## 题目

- 题目编号：T01
- 题目名称：`next_palindrome`
- 类别：边界条件
- 难度：标准
- 来源：QuixBugs `next_palindrome`
- 来源 commit：`4257f44b0ff1181dedaedee6a447e133219fcebf`
- 许可：MIT

## 目录

```text
tasks/T01_next_palindrome/
  repo/
    pyproject.toml
    README.md
    src/digitkit/__init__.py
    src/digitkit/digits.py
    src/digitkit/palindrome.py
    src/digitkit/report.py
    tests/test_target.py
    tests/test_regression.py
  meta.json
  initial_test_log.txt
  gold.patch
  ATTRIBUTION.md
  LICENSE
```

## Bug

`next_palindrome` 在输入全部由 9 组成且长度大于等于 2 时，返回的序列多一位。例如输入 `[9, 9]` 返回 `[1, 0, 0, 1]`，期望 `[1, 0, 1]`。

该 bug 来自 QuixBugs 原始 buggy 版本，没有额外注入。原题是单文件函数，本题包装为 `digitkit` 小包，并增加 `is_palindrome` 与 `next_palindrome_int` 作为相邻行为。

## 测试划分

目标测试 4 个，位于 `tests/test_target.py`。

- `test_next_palindrome_after_two_nines`
- `test_next_palindrome_after_three_nines`
- `test_next_palindrome_int_after_99`
- `test_next_palindrome_int_after_999`

回归测试 11 个，位于 `tests/test_regression.py`。

- `test_next_palindrome_examples`
- `test_next_palindrome_regular_carry`
- `test_next_palindrome_single_digit`
- `test_is_palindrome`
- `test_next_palindrome_int_regular`
- `test_validate_digits_regular`
- `test_validate_digits_rejects_invalid`
- `test_to_digits_and_from_digits`
- `test_mirror_prefix`
- `test_describe_next_palindrome_regular`
- `test_next_palindrome_length_regular`

## 验证结果

buggy 状态：

```text
4 failed, 11 passed
```

gold 状态：

```text
15 passed
```

`gold.patch` 只有一行改动，将

```python
return [1] + (len(digit_list)) * [0] + [1]
```

改为

```python
return [1] + (len(digit_list) - 1) * [0] + [1]
```

`git apply --check -p1 ../gold.patch` 通过。

`harness/validate_tasks.py` 检查结果：

```text
T01_next_palindrome: OK
  note: files=4 lines=117 buggy=4 failed, 11 passed gold=15 passed
```

## 备注

- 初始测试日志已从 pytest 输出复制到 `initial_test_log.txt`，并统一路径分隔符。
- 初版源码只有 2 个文件 40 行，低于标准题 100 行的下限。后续增加 `digits.py` 与 `report.py`，提供数字校验、整数与序列转换、前缀镜像、转换描述与位数统计，并补充 6 个回归测试，源码规模达到 4 个文件 117 行。
- gold patch 仍为一行改动，补丁范围只涉及 `src/digitkit/palindrome.py`。
- `--repeat 5` 的五轮 buggy 状态检查结果一致。
- 未对项目仓库执行 git commit。
- 等价修复与错误修复检查已通过，见 `2026-10-20_pilot_variant_checks.md`。
- 下一步安排 V4-Pro 盲解与人工复核。
