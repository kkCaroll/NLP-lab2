# 2026-10-21 评估模型免费状态核查

## 目的

确认主实验使用的两个模型是否长期免费，避免运行中途开始计费。

## 来源

```text
OpenCode Zen 官方文档  https://opencode.ai/docs/zen/
OpenCode Zen 实时目录  https://opencode.ai/zen/v1/models
核查日期               2026-10-21
```

## 结果

实时目录返回两个标识，均存在。官方文档的模型表把输入、输出与缓存读取三项全部标为 Free。

| 模型 | 标识 | 免费期限 | 数据条款 |
|---|---|---|---|
| MiniMax-M3.1-Flash Free | `minimax-m3.1-flash-free` | 限时免费，未公布结束日期 | 零保留，不用于训练 |
| MiMo-V2.6-Flash Free | `mimo-v2.6-flash-free` | 限时免费，未公布结束日期 | 免费期内数据可能用于改进模型 |

官方原文对两者均使用 free on OpenCode for a limited time，没有给出截止日期。因此两个模型都不是长期免费，不能假设整个实验周期内保持免费。

## 影响

- 当前计费为零，现有 pilot 与冒烟运行的成本记录有效。
- 供应商可在不预先通知的情况下移除免费标识或调整价格，正式运行前需要复查实时目录。
- MiMo 的数据条款允许免费期数据用于模型改进。实验使用自建题目与代码，不含个人信息或敏感数据，风险可接受，报告中需注明该差异。
- 若运行期间标识消失或开始计费，暂停实验并记录变更时间，报告中的运行窗口按实际免费时段描述。

## 状态

已更新 `PLAN/models/models.json` 与 `PLAN/models/MODELS.md`。未执行 git commit。
