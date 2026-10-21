# 2026-10-21 主实验运行完成

## 运行概况

| 项目 | 内容 |
|---|---|
| 运行编号 | 2026-10-21_main |
| 开始时间 | 2026-10-21 16:49:17 |
| 结束时间 | 2026-10-21 18:58:59 |
| 模型 | opencode/minimax-m3.1-flash-free 与 opencode/mimo-v2.6-flash-free |
| 任务 | 24 题 |
| 条件 | pure_continue、neutral、method_guidance、negative、negative_guidance |
| 完成记录 | 48 条，每模型 24 题 |
| 缺失 | 0 |
| OpenCode | 1.18.25 |
| 配置哈希 | 74aebb2171ac553e2ba07d2cd53daa15d73cd7a18b8b9505606b29136c165d38 |

批次以退出码 0 结束。聚合结果写入 `RECORD/tables/`，包括 `episode_level.csv`、`summary.json` 与 `summary.md`。

## 运行完整性

- 无超时 episode，无非预算原因的非零退出。
- 测试完整性检查触发 7 次，均为模型在 `tests/` 下新建临时自测文件。还原后使用原始测试评分，记录保留 `test_tampered=true`。
- T05 在 MiniMax negative 分支的测试篡改发生在停止规则调整之前，manifest 中该条记录仍为 `anomaly`，属于历史状态，批次随后恢复并完成。
- 分支继承检查未发现不一致。

## 第一轮结果

| 模型 | 第一轮通过 | 第一轮失败 | 首轮失败率 |
|---|---:|---:|---:|
| MiniMax-M3.1-Flash | 10 | 14 | 0.583 |
| MiMo-V2.6-Flash | 18 | 6 | 0.250 |

## 条件聚合

| 模型 | 条件 | 修复成功 | PassRate | RepairSuccess | RegressionRate | EditSize 中位数 | EditRatio 中位数 | OverEditRate |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| MiniMax | pure_continue | 12/14 | 0.917 | 0.857 | 0.000 | 2 | 1.000 | 0.083 |
| MiniMax | neutral | 9/14 | 0.792 | 0.643 | 0.000 | 2 | 1.000 | 0.083 |
| MiniMax | method_guidance | 11/14 | 0.875 | 0.786 | 0.000 | 2 | 1.000 | 0.042 |
| MiniMax | negative | 9/14 | 0.792 | 0.643 | 0.000 | 2 | 1.000 | 0.083 |
| MiniMax | negative_guidance | 13/14 | 0.958 | 0.929 | 0.000 | 2 | 1.000 | 0.042 |
| MiMo | pure_continue | 6/6 | 1.000 | 1.000 | 0.000 | 2 | 1.000 | 0.000 |
| MiMo | neutral | 5/6 | 0.958 | 0.833 | 0.000 | 2 | 1.000 | 0.000 |
| MiMo | method_guidance | 6/6 | 1.000 | 1.000 | 0.000 | 2 | 1.000 | 0.000 |
| MiMo | negative | 5/6 | 0.958 | 0.833 | 0.000 | 2 | 1.000 | 0.042 |
| MiMo | negative_guidance | 6/6 | 1.000 | 1.000 | 0.000 | 2 | 1.000 | 0.000 |

有效题数为每个条件 24。第一轮通过的题在所有条件下复用第一轮终态，修复成功比的分母为实际第一轮失败题数。

## 数据质量观察

1. 回归测试在两个模型的全部条件中共计 297 项每条件，失败数为 0。RegressionRate 在当前任务集上没有方差，无法区分条件。该指标仍按预注册定义报告，分析时需说明其退化。
2. MiniMax 的 16 次分支失败中有 15 次未发生任何编辑，MiMo 的 2 次分支失败均未编辑。失败主要表现为在工具预算内反复探查而未提交修改，不是修改错误或过度修改。
3. 编辑规模中位数为 2 行，EditRatio 中位数为 1.0，无越界文件。OverEditRate 介于 0 与 0.083。
4. 工具预算耗尽率 MiniMax 为 0.75 至 0.958，MiMo 为 0.208 至 0.25。两模型的预算压力差异明显，比较条件效应时需控制该差异。
5. T06 在 MiniMax 的五个分支中有四个触发测试完整性检查，方法指引条件未触发。该题的分支结果需结合 TestTamperRate 解读。

## 后续

1. 对 6 题进行完整重跑，评估结果稳定性。
2. 对 8 题执行无测试消融，确认测试可见性对修复行为的影响。
3. 进行配对统计检验与效应量估计。
4. 补办 24 题复核表签字并冻结任务集。

运行后核查发现条件顺序未随机化、回归错误率零方差、分支失败以未编辑为主、Bash 权限拒绝消耗预算四项问题，详见 [2026-10-21_main_run_audit.md](2026-10-21_main_run_audit.md)。补充运行与分析安排见 [PLAN/04_post_run_analysis.md](../PLAN/04_post_run_analysis.md)。
