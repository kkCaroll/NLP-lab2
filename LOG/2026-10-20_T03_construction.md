# 2026-10-20 T03 构造记录

## 题目

- 题目编号：T03
- 题目名称：`apply_discount`
- 类别：函数逻辑
- 难度：标准
- 来源：原创
- 许可：原创任务

## 目录

```text
tasks/T03_apply_discount/
  repo/
    pyproject.toml
    README.md
    src/pricing/__init__.py
    src/pricing/money.py
    src/pricing/discount.py
    src/pricing/cart.py
    tests/test_target.py
    tests/test_regression.py
  meta.json
  initial_test_log.txt
  gold.patch
  ATTRIBUTION.md
```

## Bug

`apply_discount` 把百分比费率连续除以两次 100，20% 折扣只减去 0.2%。例如金额 100 元时返回 99.80，期望 80.00。缺陷位于 `src/pricing/discount.py`，gold patch 删除一次除法。

目标测试 2 个，覆盖直接折扣与购物车折扣。回归测试 16 个，覆盖金额转换、四舍五入、加减、格式化、行合计、购物车合计、非法输入、零折扣与百分比边界。

## 验证结果

buggy 状态：

```text
2 failed, 16 passed
```

gold 状态：

```text
18 passed
```

`harness/validate_tasks.py` 检查结果：

```text
T03_apply_discount: OK
  note: files=4 lines=109 buggy=2 failed, 16 passed gold=18 passed
```

## 备注

- 源码规模为 4 个文件 109 行，符合标准题约束。
- `--repeat 5` 的五轮 buggy 状态检查结果一致。
- G10 检查通过，替代修复用 `Decimal("0.01")` 乘法，错误修复把除数改为 1000。
- 未对项目仓库执行 git commit。
- 下一步安排 T03 的 V4-Pro 盲解与人工复核。
