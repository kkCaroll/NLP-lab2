# 双倍预算补跑设计

> 状态：已执行，结果见 `RECORD/analysis/deepening/budget_rerun.md`
> 制定日期：2026-10-22
> 执行时间：2026-10-22 21:15 至 21:58
> 上位计划：[05_deepening.md](05_deepening.md) 与 [06_four_day_schedule.md](06_four_day_schedule.md)
> 性质：事后分析，结论单列，不并入主结果

## 1 目的

主实验 38 个失败中有 36 个在名义预算处被截断，其中 35 个从未编辑。补充核算显示有效预算因权限拒绝而低于名义预算，见 `RECORD/analysis/deepening/budget_accounting.md`。

本次补跑检验一个问题。预算是否为这 16 个分支失败的直接原因。

## 2 对象

16 个预算截断的分支失败，全部属于 MiniMax。按条件分布为 negative 5，neutral 5，method_guidance 3，pure_continue 2，negative_guidance 1。

| 任务 | 条件 | 原有效调用 | 原拒绝次数 |
|---|---|---:|---:|
| T14_shipping_fee | negative | 12 | 3 |
| T14_shipping_fee | neutral | 13 | 2 |
| T15_slugify | neutral | 14 | 1 |
| T15_slugify | pure_continue | 13 | 2 |
| T18_parse_bool | method_guidance | 13 | 2 |
| T18_parse_bool | negative | 13 | 2 |
| T18_parse_bool | pure_continue | 13 | 2 |
| T19_to_decimal | negative | 13 | 2 |
| T19_to_decimal | negative_guidance | 13 | 2 |
| T19_to_decimal | neutral | 13 | 2 |
| T23_parse_flags | method_guidance | 13 | 2 |
| T23_parse_flags | negative | 14 | 1 |
| T23_parse_flags | neutral | 13 | 2 |
| T24_join_path | method_guidance | 13 | 2 |
| T24_join_path | negative | 14 | 1 |
| T24_join_path | neutral | 13 | 2 |

另外两个未耗尽预算的失败不纳入，它们属于模型自主停止。

## 3 设计

同一批 16 个案例，两个臂。

| 臂 | 工具调用上限 | episode 数 | 作用 |
|---|---:|---:|---|
| A 对照 | 15 | 16 | 复现原条件，估计运行间波动 |
| B 处理 | 30 | 16 | 检验预算放宽后的恢复情况 |

两个臂各运行一次，共 32 个 episode。臂内顺序按固定种子随机化，种子写入运行记录。

保留 300 秒超时与 8 次编辑上限。原分支 episode 的时长中位数为 50 秒，最大为 185 秒，翻倍后仍在超时之内，因此不改超时以保持与主实验可比。

## 4 起始状态重建

主实验 20 个产生分支的任务模型对中，第一轮 delta 补丁全部为空。因此分支的起始状态等于任务原始仓库。

重建步骤。

1. 复制 `tasks/<task>/repo` 到临时工作区。
2. 初始化 git，提交并打 `baseline` 与 `round1` 两个标签，两者指向同一提交。
3. 直接复用原运行中 `branches/<condition>/prompt.txt` 的字节内容，不重新拼接提示词。
4. 校验提示词哈希与 `summary.json` 中的 `prompt_sha256` 一致。
5. 校验任务源目录树哈希与 `main_manifest.json` 一致。

任何一项校验失败即停止，不运行该案例。

## 5 指标

主指标为两个臂的恢复率，即通过数除以 16。

配对分析使用精确 McNemar 检验，报告风险差与精确 95% 区间。同时报告每个 episode 的有效调用、拒绝次数、首次编辑位置与截断状态。

## 6 停止规则

出现以下任一情况即停止并检查。

1. 超时。
2. 非预算原因的非零退出。
3. 提示词哈希不一致。
4. 任务源哈希不一致。
5. 编辑超过上限。

## 7 判读

| 结果模式 | 解释 |
|---|---|
| B 臂多数恢复，A 臂多数仍失败 | 预算为直接原因，主结果的失败解释需限定 |
| 两臂接近 | 原失败主要来自运行间波动，与预算关系弱 |
| 两臂多数仍失败 | 失败为稳定的探索型行为模式，放宽预算无效 |

三种结果都写入报告，不因结果方向调整表述。

## 8 输出

1. `RECORD/runs/2026-10-22_budget_rerun/` 原始 episode。
2. `RECORD/analysis/deepening/budget_rerun.md` 分析与判读。
3. `RECORD/analysis/deepening/budget_rerun.csv` 逐案例汇总。

## 9 成本与风险

32 个 episode，按中位时长估计约 1 小时，含重试约 1.5 小时。

风险有三项。其一，事后设计未预注册，结论只能作为探索性证据。其二，仅覆盖 MiniMax 与 16 个案例，不能外推到 MiMo。其三，单次重复仍不能完全分离预算效应与随机波动，A 臂只提供一个粗略的波动参照。

## 10 执行方式

写 `harness/rerun_branches.py`，接受来源运行目录、运行编号、案例清单与两个预算值。脚本逐个案例重建、运行、评分并按主实验格式落盘，完成后调用现有聚合脚本。

执行前需要用户确认两点。第一，是否保留 A 对照臂，32 个 episode；或只做 B 臂，16 个 episode。第二，补跑安排在报告初稿之前还是之后。
