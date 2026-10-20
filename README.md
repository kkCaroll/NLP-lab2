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
- 完成 T02 `parse_range` 与 T03 `apply_discount` 两道标准题，任务集累计 6 题
- 完成 `harness/validate_tasks.py`，六道题均通过结构、泄漏、双态、补丁范围、测试哈希与五轮确定性检查
- 完成 `harness/check_variants.py`，六道题均通过 G10 等价修复与错误修复检查
- 完成四道 pilot 题的 DeepSeek-V4-Pro 盲解，四题全部通过，无测试篡改
- 人工复核表已生成，位于 `RECORD/calibration/review/`，尚待复核人签字
- 下一步由复核人签字冻结 pilot，再用两道被测模型运行 pilot 并校准首轮失败率
