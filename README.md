# 负面反馈对代码智能体修复行为与过度修改的影响

本仓库是自然语言处理实验一的项目目录。实验题目见 [REQUIRE.md](REQUIRE.md) 问题 20。研究问题是第一轮修复失败后，用户的负面反馈会使代码智能体更谨慎地定位缺陷，还是导致过度修改与回归错误。

## 目录

| 目录 | 内容 |
|---|---|
| [PLAN/](PLAN/) | 实验方案、任务来源评估、造题评估、候选池与模型信息 |
| [LOG/](LOG/) | 按日期记录的操作日志 |
| [RECORD/](RECORD/) | 实验运行结果、汇总数据与最终报告 |
| [NOTES/](NOTES/) | 实验过程中积累的知识笔记 |
| [harness/](harness/) | 实验运行、验证、评分与分析代码 |
| [tasks/](tasks/) | 来源快照与已构造的代码修复任务 |

## 当前进度

- 完成来源下载与 53 题候选池
- 完成 T01、T05、T16、T21 四道 pilot 题的构造与 buggy 及 gold 双态验证
- 完成 T02 `parse_range`、T03 `apply_discount`、T14 `shipping_fee` 与 T20 `multi_key_sort`，任务集累计 8 题
- 完成 `harness/validate_tasks.py`，八道题均通过结构、泄漏、双态、补丁范围、测试哈希与五轮确定性检查
- 完成 `harness/check_variants.py`，八道题均通过 G10 等价修复与错误修复检查
- 完成四道 pilot 题的 DeepSeek-V4-Pro 盲解，四题全部通过，无测试篡改
- 完成 DeepSeek-V4.1-Flash 与 GLM-5.3-Flash 的四题 pilot，首轮失败率均为 0%，低于预注册区间
- 按预注册规则以 T14 与 T20 替换 T16 与 T21，pilot 题集改为 T01、T05、T14、T20
- 完成替换后的 pilot，两道模型仍为首轮 4 题通过，失败率 0%，结果见 `RECORD/pilot/v2/summary.md`
- 筛选六个免费模型，五个可用模型在 T14 与 T20 上首轮通过
- 将 T14 与 T20 改造为多缺陷题，用 minimax 与 mimo 重跑 pilot，首轮失败率仍为 0%，结果见 `RECORD/pilot/v4/summary.md`
- 将第一轮工具调用上限收紧至 10 次，两个免费模型各为 2 通过 2 失败，合计失败率 50%，进入预注册区间，结果见 `RECORD/pilot/v5/summary.md`
- 人工复核表已生成，位于 `RECORD/calibration/review/`，随后完成签字
- 完成主实验 harness，单题第一轮、五分支与第二轮端到端跑通，分支继承状态一致，结果见 `RECORD/smoke/2026-10-21_e2e.md`
- 完成 T04、T06、T07、T08 与 T09、T10、T11、T12 八道标准题，标准题达到 12 道
- 完成 T13、T15、T17、T18、T19、T22、T23、T24 八道困难题，困难题达到 12 道，任务集累计 24 题，全部通过五轮确定性检查与 G10 变体检查
- 完成 24 题的 DeepSeek-V4-Pro 盲解，全部通过且无测试篡改，结果见 `RECORD/calibration/summary.md`
- 复核表已更新至 24 题，位于 `RECORD/calibration/review/`，随后完成签字
- 完成主实验 2026-10-21_main，两个模型各 24 题，48 个第一轮 episode 与 100 个分支 episode，无缺失与超时，结果见 `RECORD/tables/summary.md`
- 完成主实验核查，发现条件顺序未随机化、回归错误率零方差、失败以未编辑为主等问题，记录见 `LOG/2026-10-21_main_run_audit.md`
- 补充运行与分析方案见 `PLAN/04_post_run_analysis.md`
- 24 份人工复核表已签字，任务集已冻结，清单见 `RECORD/analysis/main_manifest.json`
- 完成回归敏感性诊断，24 题覆盖率 0.916，六题变异得分 0.787，结果见 `RECORD/analysis/regression_sensitivity.md`
- 完成随机顺序复跑 harness 修正与主实验统计分析首版，结果见 `RECORD/analysis/main_results.md`
- 完成随机顺序复跑 `2026-10-21_reliability`，六题两模型共 35 个分支 episode，审计通过，结果见 `RECORD/analysis/reliability/README.md`
- 复跑中 MiniMax 的 negative 与 negative_guidance 修复成功率均为 0.600，低于 pure_continue 的 0.800，与主实验 negative_guidance 最高的方向相反，说明固定条件顺序与条件共线
- 完成无测试消融 `2026-10-21_ablation`，八题两模型共 50 个分支 episode，审计通过，无成功 Bash 执行，结果见 `RECORD/analysis/ablation/README.md`
- 消融中 MiniMax 的 negative 仍为五条件最低，通过 4/8，negative_guidance 为 6/8，pure_continue 为 8/8
- 完成主实验统计分析与报告用图，结果见 `RECORD/analysis/main_results.md` 与 `RECORD/analysis/figures/`
- 完成最终报告与演示文稿 v0，见 `RECORD/report/report_v0/report_v0.md` 与 `RECORD/report/slides_v0/`
- 完成三十一条样本的系统编码、二次编码与编码一致性分析，结果见 `RECORD/analysis/deepening/coding_summary.md` 与 `RECORD/analysis/deepening/coding_reliability.md`
- 完成预算核算、十六例双倍预算补跑、过程指标、功效分析与敏感性分析，结果见 `RECORD/analysis/deepening/README.md`
- 完成报告 v1 与演示 v1，演示含十五页与十分钟提示稿，见 `RECORD/report/report_v1/report_v1.md` 与 `RECORD/report/slides_v1/`
