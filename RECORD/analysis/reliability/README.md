# 随机顺序复跑

## 设置

run_id 为 `2026-10-21_reliability`。任务为 T05、T09、T14、T18、T19、T24，两模型五条件。第一轮工具调用十次，第二轮十五次，编辑上限八次，超时三百秒。条件顺序在任务内由 run_id、模型与任务名派生的种子随机化，并写入 `task_summary.json` 与 `run_config.json`。

## 完整性

十二份 task summary 完整，三十五个分支 episode。`harness/audit_run.py` 检查通过，无缺失、无超时、无分支继承不一致、无提示词公共前缀差异。MiMo T24 negative 分支修改了测试文件，评分前已还原，作为结果保留并记录。

## 结果

| 模型 | 分支 episode | PassRate 主运行 | PassRate 复跑 | 通过一致率 | Cohen kappa | ICC(2,1) EditSize | Spearman rho |
|---|---:|---:|---:|---:|---:|---:|---:|
| MiniMax | 25 | 0.680 | 0.720 | 0.680 | 0.324 | -0.178 | 0.011 |
| MiMo | 10 | 1.000 | 1.000 | 0.900 | 0.000 | 0.166 | 0.401 |

主运行 PassRate 与复跑 PassRate 均按两轮均进入分支的 episode 计算，因此与主实验全样本表不同。

## 解释

MiniMax 的通过一致率为 0.680，EditSize 的 ICC 为负，说明主实验中条件之间的差异在复跑中没有稳定重现。复跑中 negative 与 negative_guidance 的 RepairSuccess 均为 0.600，低于 pure_continue 的 0.800，方向与主实验 negative_guidance 最高相反。

MiMo 仅有两题进入复跑分支，通过一致率 0.900 但 kappa 为零，原因是边际分布退化。该结果不能作为稳定性的强证据。

条件顺序随机化后结果方向改变，说明主实验的固定顺序与条件完全共线，主实验的条件差异不能解释为因果效应。报告应以复跑结果作为顺序敏感性证据，并降低因果表述强度。
