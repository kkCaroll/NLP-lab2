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
- 人工复核表已生成，位于 `RECORD/calibration/review/`，尚待复核人签字
- 完成主实验 harness，单题第一轮、五分支与第二轮端到端跑通，分支继承状态一致，结果见 `RECORD/smoke/2026-10-21_e2e.md`
- 下一步补齐任务集到 24 题，并实现批量运行、指标聚合与统计分析
