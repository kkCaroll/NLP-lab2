# RECORD 目录

本目录存放实验取得的结果。

| 子目录 | 内容 |
|---|---|
| `runs/` | 逐次运行的原始事件、提示词、补丁与测试输出，体积较大，未纳入版本管理 |
| `pilot/` | 模型筛选与预注册阶段的小规模试运行记录 |
| `smoke/` | harness 端到端流程验证记录 |
| `calibration/` | 盲解、模型筛选与人工复核材料 |
| `tables/` | 主实验逐题指标与条件聚合表 |
| `analysis/` | 统计检验、补充诊断与插图数据，深入分析见 `analysis/deepening/` |
| `report/` | 最终报告与演示文稿，按版本分目录 |

`runs/` 与 `calibration/` 下的运行时缓存不纳入版本管理，可由对应脚本重新生成。`tables/`、`analysis/` 与 `report/` 纳入版本管理。
