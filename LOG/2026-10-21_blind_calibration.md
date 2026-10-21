# 2026-10-21 盲解校准与复核表

## 提交

困难题批次提交为 `db30b77`，提交信息为“新增八道困难题并补齐任务集”，已推送至 `origin main`。

## 盲解运行

对尚未校准的 20 道题运行 DeepSeek-V4-Pro 盲解，命令如下。

```text
python harness/blind_solve.py --max-tool-calls 15 T02_parse_range T03_apply_discount \
  T04_next_permutation T06_version_scan T07_group_counts T08_inventory_summary \
  T09_safe_int T10_top_k T11_sort_items T12_format_datetime T13_paginate \
  T14_shipping_fee T15_slugify T17_merge_records T18_parse_bool T19_to_decimal \
  T20_multi_key_sort T22_json_dumps T23_parse_flags T24_join_path
```

工具调用上限设为 15，与四道 pilot 题的盲解预算一致，用于判断题目可解性，不用于预测主实验通过率。

## 异常与处理

首次运行在 T22 崩溃，原因为 `tasks/T22_json_dumps/initial_test_log.txt` 以 GBK 编码保存，`harness/blind_solve.py` 以 UTF-8 读取时触发 `UnicodeDecodeError`。

处理方式如下。

1. 在 buggy 仓库中设置 `PYTHONIOENCODING=utf-8` 重新运行 pytest，以 UTF-8 重写该日志，计数保持 2 failed 与 9 passed。
2. 已完成的 17 题结果保存在各自目录的 `summary.json`，按目录合并重建总表，没有重复运行。
3. 重新运行 T22、T23 与 T24，三题均通过。

该问题只影响任务日志编码，不影响 buggy 仓库、测试或 gold 补丁。

## 结果

24 道题全部通过，无测试篡改，无超时。工具调用 6 至 15 次，修改行数 1 至 7，修改文件均在 `allowed_files` 内。合计费用 0.227416 美元。逐题结果见 `RECORD/calibration/summary.md`。

困难题在步数上与标准题接近，仅工具调用略多。该现象作为难度分层的风险记录，最终以两个被测模型的失败率为准。

## 复核表

新增 `harness/make_review.py`，从 `meta.json`、盲解 `summary.json` 与 `events.jsonl` 生成 24 份复核表，内容包含基本信息、issue、自动核验、盲解记录与签字栏。复核表位于 `RECORD/calibration/review/`，索引同步更新至 24 题。

复核表的结论、复核人与日期均为空，等待复核人填写。未代替复核人签字。

## 后续

1. 复核人逐题检查并签字。
2. 签字完成后冻结任务集。
3. 实现批量运行、指标聚合与统计分析。
