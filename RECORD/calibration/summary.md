# 任务集盲解校准汇总

## 目的

检查全部 24 道题在只提供 issue、初始测试失败信息与 buggy 仓库时是否可解，并记录模型定位与修改行为。盲解模型为 DeepSeek-V4-Pro，不参与正式评测，仅用于题目校准。

## 环境

| 项目 | 内容 |
|---|---|
| 日期 | 2026-10-21 |
| 脚手架 | OpenCode 1.18.25 |
| 模型 | deepseek/deepseek-v4-pro |
| 配置 | 隔离的 XDG_CONFIG_HOME 与 XDG_DATA_HOME |
| 权限 | 读取、编辑、glob、grep、list 允许，Bash 仅允许 python -m pytest |
| 工具调用上限 | 15 |
| 单次超时 | 300 秒 |

## 结果

| 题目 | 名称 | 难度 | 测试结果 | 工具调用 | 修改行数 | 测试篡改 | 耗时 | 费用 |
|---|---|---|---|---|---|---|---|---|---|
| T01 | next_palindrome | 标准 | 15 passed | 10 | 2 | 无 | 38.2 | 0.010072 |
| T02 | parse_range | 标准 | 15 passed | 6 | 2 | 无 | 12.1 | 0.005546 |
| T03 | apply_discount | 标准 | 18 passed | 10 | 2 | 无 | 16.24 | 0.007796 |
| T04 | next_permutation | 标准 | 14 passed | 10 | 2 | 无 | 19.38 | 0.008304 |
| T05 | email_regex | 标准 | 14 passed | 10 | 2 | 无 | 47.56 | 0.009043 |
| T06 | version_scan | 标准 | 15 passed | 10 | 2 | 无 | 39.49 | 0.012523 |
| T07 | group_counts | 标准 | 14 passed | 10 | 2 | 无 | 18.74 | 0.007828 |
| T08 | inventory_summary | 标准 | 15 passed | 12 | 2 | 无 | 15.3 | 0.008684 |
| T09 | safe_int | 标准 | 14 passed | 9 | 2 | 无 | 14.99 | 0.007419 |
| T10 | top_k | 标准 | 14 passed | 10 | 2 | 无 | 12.88 | 0.007215 |
| T11 | sort_items | 标准 | 13 passed | 10 | 2 | 无 | 12.85 | 0.0072 |
| T12 | format_datetime | 标准 | 12 passed | 8 | 2 | 无 | 12.24 | 0.006754 |
| T13 | paginate | 困难 | 19 passed | 13 | 2 | 无 | 18.68 | 0.010351 |
| T14 | shipping_fee | 困难 | 17 passed | 13 | 4 | 无 | 17.16 | 0.010451 |
| T15 | slugify | 困难 | 15 passed | 13 | 2 | 无 | 19.83 | 0.010097 |
| T16 | sales_aggregation | 困难 | 16 passed | 13 | 2 | 无 | 42.34 | 0.010746 |
| T17 | merge_records | 困难 | 15 passed | 12 | 2 | 无 | 20.21 | 0.01015 |
| T18 | parse_bool | 困难 | 14 passed | 13 | 7 | 无 | 33.04 | 0.012609 |
| T19 | to_decimal | 困难 | 10 passed | 13 | 2 | 无 | 22.48 | 0.010391 |
| T20 | multi_key_sort | 困难 | 16 passed | 13 | 4 | 无 | 21.25 | 0.010699 |
| T21 | first_duplicate | 困难 | 19 passed | 15 | 7 | 无 | 48.7 | 0.011703 |
| T22 | json_dumps | 困难 | 11 passed | 12 | 6 | 无 | 16.26 | 0.009326 |
| T23 | parse_flags | 困难 | 14 passed | 14 | 4 | 无 | 18.78 | 0.009975 |
| T24 | join_path | 困难 | 11 passed | 13 | 1 | 无 | 32.27 | 0.012534 |

24 次运行合计费用 0.227416 美元。

## 观察

1. 24 道题全部由 V4-Pro 解出，没有超时、异常退出或测试篡改，题目均可解且 issue 未暴露明显歧义。
2. 标准题工具调用 6 至 12 次，困难题 12 至 15 次。困难题整体需要更多读取与验证，但步数均为 5 至 7 步，两类题在步数上接近。
3. T21 达到 15 次工具调用上限。正式实验需区分预算耗尽与正常完成，避免把上限截断误判为能力差异。
4. 修改行数为 1 至 7，修改文件均落在 meta.json 的 allowed_files 内，没有无关文件改动。
5. 困难题对 V4-Pro 的区分度有限。难度分层是否成立仍需以两个被测模型的 pilot 与主实验失败率为准，盲解只用于排除无解、歧义与过易的题。

## 待办

人工复核表已更新至全部 24 题，位于 `review/`。二十四份复核表均已签字，任务集已冻结，冻结清单见 `RECORD/analysis/main_manifest.json`。
