# 2026-10-20 T16 构造记录

## 题目

- 题目编号：T16
- 题目名称：`sales_aggregation`
- 类别：数据处理
- 难度：困难
- 来源：BigCodeBench 741
- 来源版本：v0.1.4
- 许可：Apache-2.0

## 目录

```text
tasks/T16_sales_aggregation/
  repo/
    pyproject.toml
    README.md
    src/saleskit/__init__.py
    src/saleskit/money.py
    src/saleskit/records.py
    src/saleskit/aggregate.py
    src/saleskit/filters.py
    src/saleskit/metrics.py
    src/saleskit/report.py
    tests/test_target.py
    tests/test_regression.py
  meta.json
  initial_test_log.txt
  gold.patch
  ATTRIBUTION.md
  LICENSE
```

## Bug

区域聚合在退款分支中把金额加到总额，退款因此增加区域收入。缺陷位于 `src/saleskit/aggregate.py`，gold patch 把加号改为减号。

目标测试 3 个，覆盖区域净收入、总收入和销售报告的退款处理。回归测试 13 个，覆盖金额转换、格式化、记录归一化、纯销售聚合、空输入、非法类型、筛选、指标与摘要。

## 验证结果

buggy 状态：

```text
3 failed, 13 passed
```

gold 状态：

```text
16 passed
```

`harness/validate_tasks.py` 检查结果：

```text
T16_sales_aggregation: OK
  note: files=7 lines=251 buggy=3 failed, 13 passed gold=16 passed
```

## 备注

- 源码规模为 7 个文件 251 行，符合困难题 4 到 8 个文件、250 到 600 行的约束。
- 构造过程中出现过一次字节码残留问题。单行补丁不改变文件大小，Python 未重新编译，导致反向补丁后仍显示 gold 结果。验证脚本现已在每次 pytest 前清除 `__pycache__` 与 `.pytest_cache`，并设置 `PYTHONDONTWRITEBYTECODE=1`。
- `--repeat 5` 的五轮 buggy 状态检查结果一致，未出现跳过、随机失败或超时。
- 未对项目仓库执行 git commit。
- 等价修复与错误修复检查已通过，见 `2026-10-20_pilot_variant_checks.md`。
- 下一步安排 V4-Pro 盲解与人工复核。
