# 被测模型 pilot 首轮结果

## 目的

用正式实验的两道被测模型运行四道 pilot 题，检查首轮失败率是否落在预注册的 40% 到 80%。

## 环境

| 项目 | 内容 |
|---|---|
| 日期 | 2026-10-21 |
| 脚手架 | OpenCode 1.18.25 |
| 模型 A | deepseek/deepseek-flash |
| 模型 B | opencode/glm-5.3-flash-free |
| 提示词 | 主实验第一轮提示词 |
| 权限 | 读取、编辑、glob、grep、list 允许，Bash 仅允许 python -m pytest |
| 步数上限 | 12 |
| 单次超时 | 420 秒 |

## 结果

| 题目 | 难度 | DeepSeek Flash | 工具调用 | GLM-5.3-Flash | 工具调用 |
|---|---|---|---|---|---|
| T01 next_palindrome | 标准 | 15 passed | 7 | 15 passed | 7 |
| T05 email_regex | 标准 | 14 passed | 6 | 14 passed | 8 |
| T16 sales_aggregation | 困难 | 16 passed | 12 | 16 passed | 9 |
| T21 first_duplicate | 困难 | 19 passed | 9 | 19 passed | 6 |

## 汇总

| 模型 | 首轮通过 | 首轮失败 | 首轮失败率 | 总费用 |
|---|---|---|---|---|
| DeepSeek-V4.1-Flash | 4 | 0 | 0% | 0.007904 美元 |
| GLM-5.3-Flash | 4 | 0 | 0% | 0 美元 |

八次运行均未超时，均未修改测试，均只修改允许的源码文件。

## 结论

两道被测模型的首轮失败率均为 0%，低于预注册的 40% 到 80% 区间。当前 pilot 题对这一代低成本代码模型过易，不能直接用于检验负面反馈效应。原因主要是缺陷均为单行、目标测试直接指出行为差异，模型读取失败日志后可以快速定位。

## 调整决定

按预注册的 floor 与 ceiling 替换规则，采用方案一，即用共享 helper 与多条调用链的困难题替换 T16 与 T21。

- T14 `shipping_fee` 替换 T16 `sales_aggregation`。
- T20 `sort_records` 替换 T21 `first_duplicate`。
- T16 与 T21 保留为正式任务，不删除，并在结果分析中单独报告其在 pilot 中未产生首轮失败。

T14 与 T20 已于 2026-10-21 构造完成并通过自动验证。下一步用 T01、T05、T14、T20 重新运行两道被测模型的 pilot。在替换后的 pilot 完成前不进入主实验，也不根据单次结果反复调题。
