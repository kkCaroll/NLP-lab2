# 任务人工复核

本目录存放全部 24 道题的复核表。自动核验与盲解部分由 `harness/validate_tasks.py`、`harness/check_variants.py`、`harness/blind_solve.py` 与 `harness/make_review.py` 产生。人工复核需要检查 issue 表述、测试语义、来源许可与盲解差异，并在每题末尾填写结论、复核人与日期。

| 题号 | 名称 | 难度 | 复核表 | 盲解 | 签字 |
|---|---|---|---|---|---|
| T01 | next_palindrome | 标准 | [T01_review.md](T01_review.md) | 通过 | 未签字 |
| T02 | parse_range | 标准 | [T02_review.md](T02_review.md) | 通过 | 未签字 |
| T03 | apply_discount | 标准 | [T03_review.md](T03_review.md) | 通过 | 未签字 |
| T04 | next_permutation | 标准 | [T04_review.md](T04_review.md) | 通过 | 未签字 |
| T05 | email_regex | 标准 | [T05_review.md](T05_review.md) | 通过 | 未签字 |
| T06 | version_scan | 标准 | [T06_review.md](T06_review.md) | 通过 | 未签字 |
| T07 | group_counts | 标准 | [T07_review.md](T07_review.md) | 通过 | 未签字 |
| T08 | inventory_summary | 标准 | [T08_review.md](T08_review.md) | 通过 | 未签字 |
| T09 | safe_int | 标准 | [T09_review.md](T09_review.md) | 通过 | 未签字 |
| T10 | top_k | 标准 | [T10_review.md](T10_review.md) | 通过 | 未签字 |
| T11 | sort_items | 标准 | [T11_review.md](T11_review.md) | 通过 | 未签字 |
| T12 | format_datetime | 标准 | [T12_review.md](T12_review.md) | 通过 | 未签字 |
| T13 | paginate | 困难 | [T13_review.md](T13_review.md) | 通过 | 未签字 |
| T14 | shipping_fee | 困难 | [T14_review.md](T14_review.md) | 通过 | 未签字 |
| T15 | slugify | 困难 | [T15_review.md](T15_review.md) | 通过 | 未签字 |
| T16 | sales_aggregation | 困难 | [T16_review.md](T16_review.md) | 通过 | 未签字 |
| T17 | merge_records | 困难 | [T17_review.md](T17_review.md) | 通过 | 未签字 |
| T18 | parse_bool | 困难 | [T18_review.md](T18_review.md) | 通过 | 未签字 |
| T19 | to_decimal | 困难 | [T19_review.md](T19_review.md) | 通过 | 未签字 |
| T20 | multi_key_sort | 困难 | [T20_review.md](T20_review.md) | 通过 | 未签字 |
| T21 | first_duplicate | 困难 | [T21_review.md](T21_review.md) | 通过 | 未签字 |
| T22 | json_dumps | 困难 | [T22_review.md](T22_review.md) | 通过 | 未签字 |
| T23 | parse_flags | 困难 | [T23_review.md](T23_review.md) | 通过 | 未签字 |
| T24 | join_path | 困难 | [T24_review.md](T24_review.md) | 通过 | 未签字 |

盲解统一使用 DeepSeek-V4-Pro，经 OpenCode 1.18.25 在隔离配置下运行。模型只看 issue、初始测试日志与 buggy 仓库副本，不看 meta.json、gold.patch 或任务来源说明。

人工复核签字后，题目才视为冻结。签字前不得根据 evaluator 模型结果改题。
