# tables 目录

| 文件 | 内容 |
|---|---|
| episode_level.csv | 逐题逐条件记录，供统计检验使用 |
| summary.json | 按模型与条件聚合的全部指标 |
| summary.md | 主结果表的可读版本 |
| _partial_20tasks/ | 批次运行中途的快照，仅用于过程审计，已被主结果取代 |

主结果对应运行编号 2026-10-21_main，由 `harness/aggregate.py` 生成。重新聚合会覆盖本目录顶层文件，不修改 `_partial_20tasks/`。
