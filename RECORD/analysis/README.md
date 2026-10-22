# ANALYSIS 目录

本目录存放主实验之后生成的核查、敏感性与统计分析结果。

| 文件或目录 | 内容 |
|---|---|
| `main_manifest.json` | 主实验表文件哈希、任务集哈希与复核签字状态 |
| `tasks_manifest.json` | 24 题任务文件逐文件 SHA-256 |
| `audit_2026-10-21_main.json` | 主实验完整性与提示词审计输出 |
| `audit_2026-10-21_reliability.json` | 随机顺序复跑完整性审计输出 |
| `audit_2026-10-21_ablation.json` | 无测试消融完整性审计输出 |
| `regression_sensitivity.md` | 回归测试覆盖率与变异诊断说明 |
| `regression_coverage.csv` | 24 题回归测试源码覆盖率 |
| `regression_mutation.csv` | 6 题逐变异体明细 |
| `reliability/` | 六题两模型随机顺序复跑的一致性结果 |
| `ablation/` | 八题两模型无测试消融的聚合与说明 |
| `tool_attempts_*.csv` | 主实验、复跑与消融逐 episode 的工具尝试计数 |
| `qualitative/` | 质性抽样名单与编码表 |
| `deepening/` | 深入研究阶段的盲化材料、编码表与过程指标 |
| `main_results.csv` | 主实验描述统计长表，含分支子集与全样本 |
| `main_results.md` | 描述统计、配对检验与解释约束 |
| `statistics.json` | 配对检验、效应量、复跑一致性与消融结果 |
| `figures/` | 报告用图 |

统计结果可由 `harness/analyze.py`、`harness/make_figures.py`、`harness/regression_sensitivity.py` 与 `RECORD/tables/episode_level.csv` 重建。审计与工具计数分别由 `harness/audit_run.py` 与 `harness/count_tool_attempts.py` 生成。随机种子固定为 20261021，bootstrap 重采样 10000 次。
