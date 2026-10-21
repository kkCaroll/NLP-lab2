# 无测试消融

## 设置

run_id 为 `2026-10-21_ablation`。任务为 T05、T06、T13、T14、T18、T19、T20、T24，两模型五条件。第一轮工具调用十次，第二轮十五次，编辑上限八次，超时三百秒。条件顺序在任务内由 run_id、模型与任务名派生的种子随机化，并写入每题的 `task_summary.json` 与 `run_config.json`。

执行配置为 `harness/configs/ablation/opencode.json`，所有 Bash 调用被拒绝。第一轮提示词把可以运行测试的句子替换为当前环境不允许运行测试，第二轮提示词基底与主实验相同，仍提供第一轮失败日志。配置哈希为 `56b4136398460cdfe99d56815228fdb112b33cdcd659fba688da5af15d5c6a22`。

MiniMax 八题第一轮全部失败，进入四十个分支 episode。MiMo 八题中六题第一轮通过，仅 T13 与 T14 进入分支，共十个分支 episode。两模型合计十六份 task summary 与五十个分支 episode。

## 完整性

`harness/audit_run.py` 检查通过，记录数为 16，分支数为 50，无缺失 summary、无缺失分支、无超时、无分支继承不一致、无提示词公共前缀差异。测试篡改计数为零。

无测试执行核验基于原始事件流。六十六个 episode 中二十五个出现 Bash 尝试，共二十六次，二十六次均返回工具不可用，成功完成零次，权限拒绝零次。二十六次尝试同时计为无效工具调用。该结果表明消融期间没有任何测试被执行。

批清单的 `config` 字段初次写入时沿用了主配置路径，与逐题 `run_config.json` 不一致。已按逐题记录与消融配置哈希更正批清单，实际执行配置为消融配置，主配置哈希未参与本次运行。

## 结果

下表为同一批八题的全样本比较。每格给出通过题数与通过率，样本量均为八。主运行与消融的差异以消融减主运行表示。MiMo 的多数条件行为由第一轮通过任务复用，条件差异只来自 T13 与 T14 两个分支题。

| 模型 | 条件 | 主运行通过 | 消融通过 | 差值 | 主运行 EditSize | 消融 EditSize |
|---|---|---:|---:|---:|---:|---:|
| MiniMax | pure_continue | 7/8 0.875 | 8/8 1.000 | +0.125 | 2.5 | 4.0 |
| MiniMax | neutral | 5/8 0.625 | 7/8 0.875 | +0.250 | 2.0 | 2.0 |
| MiniMax | method_guidance | 6/8 0.750 | 8/8 1.000 | +0.250 | 2.0 | 3.0 |
| MiniMax | negative | 4/8 0.500 | 4/8 0.500 | 0.000 | 1.0 | 2.0 |
| MiniMax | negative_guidance | 7/8 0.875 | 6/8 0.750 | -0.125 | 2.5 | 2.5 |
| MiMo | pure_continue | 8/8 1.000 | 8/8 1.000 | 0.000 | 3.0 | 3.0 |
| MiMo | neutral | 7/8 0.875 | 8/8 1.000 | +0.125 | 2.5 | 3.0 |
| MiMo | method_guidance | 8/8 1.000 | 8/8 1.000 | 0.000 | 3.0 | 3.0 |
| MiMo | negative | 7/8 0.875 | 8/8 1.000 | +0.125 | 2.0 | 3.0 |
| MiMo | negative_guidance | 8/8 1.000 | 8/8 1.000 | 0.000 | 2.5 | 3.0 |

MiniMax 合计由 29/40 升至 33/40，通过率由 0.725 升至 0.825。MiMo 合计由 38/40 升至 40/40，通过率由 0.950 升至 1.000。MiniMax 的增益集中在 pure_continue、neutral 与 method_guidance，negative 没有变化，negative_guidance 下降一题。

第一轮失败集合发生变化。MiniMax 主运行与消融均为零题通过。MiMo 主运行两题通过，消融六题通过，因此消融的分支题由六题降为两题。两轮均进入分支的交集仅有十对 MiMo episode 与四十对 MiniMax episode，该交集的配对差值只作描述，不能代替全样本比较。

## 失败机制

MiniMax 分支子集的失败以未编辑为主。negative 失败四题，其中 T13、T19、T24 未产生编辑，T20 编辑两行仍未通过。negative_guidance 失败两题，T13 与 T19 均未编辑。neutral 失败一题，T18 未编辑。method_guidance 与 pure_continue 无失败。

| 条件 | 通过 | 未编辑失败 | 预算耗尽 | 工具调用中位数 | EditSize 中位数 |
|---|---:|---:|---:|---:|---:|
| pure_continue | 8/8 | 0 | 5/8 | 15 | 4.0 |
| neutral | 7/8 | 1 | 6/8 | 15 | 2.0 |
| method_guidance | 8/8 | 0 | 6/8 | 15 | 3.0 |
| negative | 4/8 | 3 | 7/8 | 15 | 2.0 |
| negative_guidance | 6/8 | 2 | 8/8 | 15 | 2.5 |

negative 与 negative_guidance 的预算耗尽比例最高。两条件在第二轮多表现为继续读取与搜索，未形成编辑即耗尽十五次调用。negative 的 EditSize 中位数低于 pure_continue，但该差异来自未编辑与失败，不应解释为修改更精确。

MiMo 的两个分支题在五条件中全部通过，EditSize 中位数为三至四行，无法估计条件差异。

## 解释

1. 在移除测试执行并随机化条件顺序后，MiniMax 的 negative 仍为五条件最低，pure_continue 与 method_guidance 最高。负面反馈与较低修复成功率的关联不依赖测试执行，也不依赖主实验的固定条件顺序。
2. negative_guidance 未恢复到 pure_continue 水平，且在消融中低于主运行。结合随机顺序复跑中负面条件低于纯继续的结果，现有数据不支持负面加方法指引能够稳定缓解负面反馈的假设。
3. 无测试环境整体通过率更高，但增益集中在原本通过率较高的条件，negative 没有改善。一种解释是主实验中允许的测试调用消耗了有限的工具预算，另一种解释是单次运行的随机波动。当前设计不能区分二者。
4. MiMo 第一轮通过数由两题升至六题，说明无测试提示可能改变第一轮探索与编辑策略。该差异只基于一次运行，且 MiMo 在分支阶段出现天花板，不能据此推断测试对修复的普遍作用。
5. 所有条件的 RegressionRate 为零，且测试篡改计数为零。回归测试敏感性诊断的总体变异得分为 0.787，T13 为 0.375，T20 为 0.625，因此零回归不能作为无回归的强证据。无测试消融也没有提供关于测试驱动回归防护的证据。

## 限制

消融同时改变了测试可用性、第一轮提示词与条件顺序。主运行条件顺序固定，消融顺序随机，二者并非只差测试权限，因此全样本差值不能直接归因于测试执行。条件内样本量为八，MiMo 的有效分支样本为二，所有比较均为探索性。单次运行无法区分条件效应与运行间波动。

## 产物

- `RECORD/analysis/ablation/summary.md`
- `RECORD/analysis/ablation/episode_level.csv`
- `RECORD/analysis/ablation/summary.json`
- `RECORD/analysis/tool_attempts_2026-10-21_ablation.csv`
- `RECORD/analysis/audit_2026-10-21_ablation.json`
- `RECORD/analysis/statistics.json`
