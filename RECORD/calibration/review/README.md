# pilot 人工复核

本目录存放四道 pilot 题的复核材料。自动核验部分由 `harness/validate_tasks.py`、`harness/check_variants.py` 与 `harness/blind_solve.py` 产生。人工复核部分需要复核人检查 issue 表述、测试语义、来源许可与盲解差异，并在每题末尾签字。

| 题目 | 复核表 | 自动核验 | 盲解 |
|---|---|---|---|
| T01 | [T01_review.md](T01_review.md) | 通过 | 通过 |
| T05 | [T05_review.md](T05_review.md) | 通过 | 通过 |
| T16 | [T16_review.md](T16_review.md) | 通过 | 通过 |
| T21 | [T21_review.md](T21_review.md) | 通过 | 通过 |

盲解统一使用 DeepSeek-V4-Pro，经 OpenCode 1.18.25 在隔离配置下运行。模型只看 issue、初始测试日志与 buggy 仓库副本，不看 meta.json、gold.patch 或任务来源说明。

人工复核签字后，题目才视为冻结。签字前不得根据 evaluator 模型结果改题。
