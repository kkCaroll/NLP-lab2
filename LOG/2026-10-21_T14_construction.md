# 2026-10-21 T14 构造记录

## 题目

- 题目编号：T14
- 题目名称：`shipping_fee`
- 类别：函数逻辑
- 难度：困难
- 来源：原创
- 替换关系：T14 取代 T16 进入 pilot 题集，T16 仍保留为正式任务

## 目录

```text
tasks/T14_shipping_fee/
  repo/
    pyproject.toml
    README.md
    .gitignore
    src/logistics/__init__.py
    src/logistics/units.py
    src/logistics/parcels.py
    src/logistics/rates.py
    src/logistics/fees.py
    src/logistics/batches.py
    tests/test_target.py
    tests/test_regression.py
  meta.json
  initial_test_log.txt
  gold.patch
  ATTRIBUTION.md
```

## Bug

共享换算 helper 的克分支直接返回原始数值，没有换算为千克。缺陷位于 `src/logistics/units.py` 的 `to_kilograms`。`parse_parcel` 与 `shipping_fee` 都调用该 helper，因此同一定位点会通过两条公开路径暴露，模型需要沿调用链判断哪一层才是缺陷来源。

目标测试 2 个，覆盖包裹解析与运费计算。回归测试 14 个，覆盖千克、磅与零克换算，格式转换，包裹描述，基础费率与区域附加费，加急倍率，千克路径运费，报价摘要，批量统计与非法输入校验。

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
T14_shipping_fee: OK
  note: files=6 lines=290 buggy=2 failed, 14 passed gold=16 passed
```

`harness/check_variants.py` 检查结果：

```text
T14_shipping_fee:
  alternative: passed
  wrong: failed
  OK
```

## 备注

- 源码规模为 6 个文件 290 行，符合困难题 4 到 8 个文件、250 到 600 行的约束。
- 首次生成 gold patch 时替换命中了千克与克两个分支。已改为在克分支内定位，当前补丁只修改一行。
- 回归测试故意使用千克与零克输入，两种状态下均通过，避免目标行为被回归测试直接揭示。
- 错误修复变体为除以 100，仍能通过部分断言，但被目标测试判定失败。
- 未对项目仓库执行 git commit。
- 下一步构造 T20 多键排序题，之后用 T01、T05、T14、T20 重新运行 pilot。
