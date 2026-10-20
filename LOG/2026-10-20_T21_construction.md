# 2026-10-20 T21 构造记录

## 题目

- 题目编号：T21
- 题目名称：`first_duplicate`
- 类别：排序查找
- 难度：困难
- 来源：QuixBugs `find_first_in_sorted` 与原创重复值工具
- 来源 commit：`4257f44b0ff1181dedaedee6a447e133219fcebf`
- 许可：MIT

## 目录

```text
tasks/T21_first_duplicate/
  repo/
    pyproject.toml
    README.md
    src/seqkit/__init__.py
    src/seqkit/validate.py
    src/seqkit/search.py
    src/seqkit/stats.py
    src/seqkit/analysis.py
    src/seqkit/runs.py
    src/seqkit/report.py
    tests/test_target.py
    tests/test_regression.py
  meta.json
  initial_test_log.txt
  gold.patch
  ATTRIBUTION.md
  LICENSE
```

## Bug

`_first_repeated` 在扫描过程中反复覆盖结果，返回最后一次出现的重复值，而不是首次出现位置最靠前的重复值。例如输入 `[3, 1, 3, 2, 1]` 返回 1，期望返回 3。缺陷位于 `src/seqkit/search.py`，gold patch 改为首次命中立即返回。

目标测试 3 个，覆盖最早重复值、其索引与重复报告。回归测试 16 个，覆盖无重复、单一重复、位置、计数、最常见重复值、比例、重复间隔、连续段、有序查找、空序列、非法输入、不可哈希值与元组输入。

## 验证结果

buggy 状态：

```text
3 failed, 16 passed
```

gold 状态：

```text
19 passed
```

`harness/validate_tasks.py` 检查结果：

```text
T21_first_duplicate: OK
  note: files=7 lines=279 buggy=3 failed, 16 passed gold=19 passed
```

## 备注

- 源码规模为 7 个文件 279 行，符合困难题 4 到 8 个文件、250 到 600 行的约束。
- 构造过程中修正了重复间隔语义。`first_repeat_gap` 与 `repeat_gaps` 现在在每次出现后更新最近位置，回归测试与实现一致。
- `--repeat 5` 的五轮 buggy 状态检查结果一致，未出现跳过、随机失败或超时。
- 未对项目仓库执行 git commit。
- 等价修复与错误修复检查已通过，见 `2026-10-20_pilot_variant_checks.md`。
- 下一步安排 V4-Pro 盲解与人工复核。
