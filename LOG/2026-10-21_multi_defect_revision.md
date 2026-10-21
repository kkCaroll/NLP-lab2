# 2026-10-21 T14 与 T20 多缺陷改造

## 背景

替换为免费模型后，五个可用模型在 T14 与 T20 上仍首轮通过。按用户决定，保留免费模型方向，同时把 T14 与 T20 改造为多缺陷题，使只修复一处缺陷无法通过全部目标测试。

## T14 改造

新增第二处缺陷。`total_weight` 先收集各包裹的千克重量，再除以包裹数量，返回平均重量。

目标测试增加 `test_total_weight_sums_mixed_units`，使用 2000 克与 1 千克两个包裹，期望合计 3 千克。该测试同时依赖克换算修复与求和修复。

gold patch 涉及两个文件。

```text
src/logistics/units.py    克分支改为除以 KG_PER_GRAM
src/logistics/parcels.py  total_weight 改为直接求和
```

验证结果。

```text
T14_shipping_fee: OK
  note: files=6 lines=292 buggy=3 failed, 14 passed gold=17 passed
```

## T20 改造

新增第二处缺陷。`department_age_order` 直接按分组输入顺序返回姓名，没有调用共享排序 helper。

目标测试 `test_top_k_and_department_order_share_multi_key_order` 同时检查 top_k 与部门内部顺序。仅修复共享 helper 后 top_k 通过，部门顺序仍失败。

gold patch 涉及两个文件。

```text
src/recordkit/keys.py      移除 reverse=True
src/recordkit/grouping.py  部门顺序改为调用 order_records
```

验证结果。

```text
T20_multi_key_sort: OK
  note: files=6 lines=264 buggy=2 failed, 14 passed gold=16 passed
```

## 变体检查

`harness/check_variants.py` 已扩展为支持多文件编辑。T14 与 T20 的等价修复需要同时修改两个文件，错误修复保留至少一处缺陷。

```text
T14_shipping_fee: alternative passed, wrong failed, OK
T20_multi_key_sort: alternative passed, wrong failed, OK
```

## Pilot

用 minimax-m3.1-flash-free 与 mimo-v2.6-flash-free 运行 T01、T05、T14、T20。

```text
MiniMax-M3.1-Flash   4 passed  0 failed  失败率 0%
MiMo-V2.6-Flash      4 passed  0 failed  失败率 0%
```

两个模型在 T14 与 T20 上均完成两处修改，补丁与 gold patch 一致。详细数据见 `../RECORD/pilot/v4/summary.md`。

## 结论

多缺陷设计仍未产生首轮失败。任务对当前模型代际饱和，需要从预算、可见测试或研究设计层面进一步调整。

## 状态

未执行 git commit。
