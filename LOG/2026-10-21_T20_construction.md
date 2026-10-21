# 2026-10-21 T20 构造记录

## 题目

- 题目编号：T20
- 题目名称：`multi_key_sort`
- 类别：排序查找
- 难度：困难
- 来源：原创
- 替换关系：T20 取代 T21 进入 pilot 题集，T21 仍保留为正式任务

## 目录

```text
tasks/T20_multi_key_sort/
  repo/
    pyproject.toml
    README.md
    .gitignore
    src/recordkit/__init__.py
    src/recordkit/records.py
    src/recordkit/keys.py
    src/recordkit/sorting.py
    src/recordkit/grouping.py
    src/recordkit/report.py
    tests/test_target.py
    tests/test_regression.py
  meta.json
  initial_test_log.txt
  gold.patch
  ATTRIBUTION.md
```

## Bug

共享排序键 `record_key` 已经用年龄取负实现降序，排序 helper `order_records` 又传入 `reverse=True`，导致年龄变为升序，姓名次序也由升序变为降序。缺陷位于 `src/recordkit/keys.py` 的 `order_records`。`sort_records`、`top_k` 与 `department_age_order` 都通过该 helper 排序，因此修复需要定位到共享层，而不是逐个调用方调整。

目标测试 2 个，覆盖整体排序顺序以及 `top_k` 与部门内部顺序。回归测试 14 个，覆盖年龄解析、姓名归一化、记录校验、输入不变性、空输入与单条记录、相同键稳定性与并列排名、`k` 参数校验、分组顺序、部门汇总与报告输出。

## 验证结果

buggy 状态：

```text
2 failed, 14 passed
```

gold 状态：

```text
16 passed
```

`harness/validate_tasks.py` 检查结果：

```text
T20_multi_key_sort: OK
  note: files=6 lines=264 buggy=2 failed, 14 passed gold=16 passed
```

`harness/check_variants.py` 检查结果：

```text
T20_multi_key_sort:
  alternative: passed
  wrong: failed
  OK
```

## 备注

- 源码规模为 6 个文件 264 行，符合困难题 4 到 8 个文件、250 到 600 行的约束。初版为 242 行，补充 `format_names` 与 `department_lines` 并增加回归断言后达到下限。
- 首次生成的补丁 hunk 行数写成 4，实际上下文为 5 行，`git apply` 报 corrupt patch。修正 hunk 头后通过。
- 回归测试只使用单条记录、空输入或键完全相同的数据检查顺序相关接口，避免在 buggy 状态下直接失败。
- 未对项目仓库执行 git commit。
- 下一步用 T01、T05、T14、T20 重新运行两道被测模型的 pilot。
