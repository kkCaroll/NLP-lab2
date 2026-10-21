# 主实验聚合 2026-10-21_main

有效任务记录 240 行，缺失 27 项。

| 模型 | 条件 | 有效题数 | 第一轮通过 | 修复成功 | PassRate | RepairSuccess | RegressionRate | EditSize 中位数 | EditRatio 中位数 | OverEditRate |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| opencode/minimax-m3.1-flash-free | pure_continue | 20 | 9 | 9 | 0.900 | 0.818 | 0.000 | 2.000 | 1.000 | 0.000 |
| opencode/minimax-m3.1-flash-free | neutral | 20 | 9 | 8 | 0.850 | 0.727 | 0.000 | 2.000 | 1.000 | 0.050 |
| opencode/minimax-m3.1-flash-free | method_guidance | 20 | 9 | 10 | 0.950 | 0.909 | 0.000 | 2.000 | 1.000 | 0.000 |
| opencode/minimax-m3.1-flash-free | negative | 20 | 9 | 8 | 0.850 | 0.727 | 0.000 | 2.000 | 1.000 | 0.050 |
| opencode/minimax-m3.1-flash-free | negative_guidance | 20 | 9 | 10 | 0.950 | 0.909 | 0.000 | 2.000 | 1.000 | 0.000 |
| opencode/mimo-v2.6-flash-free | pure_continue | 1 | 1 | 0 | 1.000 | NA | 0.000 | 2 | 1.000 | 0.000 |
| opencode/mimo-v2.6-flash-free | neutral | 1 | 1 | 0 | 1.000 | NA | 0.000 | 2 | 1.000 | 0.000 |
| opencode/mimo-v2.6-flash-free | method_guidance | 1 | 1 | 0 | 1.000 | NA | 0.000 | 2 | 1.000 | 0.000 |
| opencode/mimo-v2.6-flash-free | negative | 1 | 1 | 0 | 1.000 | NA | 0.000 | 2 | 1.000 | 0.000 |
| opencode/mimo-v2.6-flash-free | negative_guidance | 1 | 1 | 0 | 1.000 | NA | 0.000 | 2 | 1.000 | 0.000 |

## 缺失

- T21_first_duplicate: summary missing for opencode/minimax-m3.1-flash-free
- T22_json_dumps: summary missing for opencode/minimax-m3.1-flash-free
- T23_parse_flags: summary missing for opencode/minimax-m3.1-flash-free
- T24_join_path: summary missing for opencode/minimax-m3.1-flash-free
- T02_parse_range: summary missing for opencode/mimo-v2.6-flash-free
- T03_apply_discount: summary missing for opencode/mimo-v2.6-flash-free
- T04_next_permutation: summary missing for opencode/mimo-v2.6-flash-free
- T05_email_regex: summary missing for opencode/mimo-v2.6-flash-free
- T06_version_scan: summary missing for opencode/mimo-v2.6-flash-free
- T07_group_counts: summary missing for opencode/mimo-v2.6-flash-free
- T08_inventory_summary: summary missing for opencode/mimo-v2.6-flash-free
- T09_safe_int: summary missing for opencode/mimo-v2.6-flash-free
- T10_top_k: summary missing for opencode/mimo-v2.6-flash-free
- T11_sort_items: summary missing for opencode/mimo-v2.6-flash-free
- T12_format_datetime: summary missing for opencode/mimo-v2.6-flash-free
- T13_paginate: summary missing for opencode/mimo-v2.6-flash-free
- T14_shipping_fee: summary missing for opencode/mimo-v2.6-flash-free
- T15_slugify: summary missing for opencode/mimo-v2.6-flash-free
- T16_sales_aggregation: summary missing for opencode/mimo-v2.6-flash-free
- T17_merge_records: summary missing for opencode/mimo-v2.6-flash-free
- T18_parse_bool: summary missing for opencode/mimo-v2.6-flash-free
- T19_to_decimal: summary missing for opencode/mimo-v2.6-flash-free
- T20_multi_key_sort: summary missing for opencode/mimo-v2.6-flash-free
- T21_first_duplicate: summary missing for opencode/mimo-v2.6-flash-free
- T22_json_dumps: summary missing for opencode/mimo-v2.6-flash-free
- T23_parse_flags: summary missing for opencode/mimo-v2.6-flash-free
- T24_join_path: summary missing for opencode/mimo-v2.6-flash-free
