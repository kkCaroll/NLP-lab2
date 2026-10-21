# 对比模型信息卡

> 核对日期：2026-10-21
> 本文件记录问题 20 实验中两个被评估代码模型的实际接入方式与参数。实验运行时以本文件与 `models.json` 为准。免费层的模型标识、路由与权重可能随时变更，报告中须注明运行窗口。

## 0. 一句话结论

| 角色 | 模型 | OpenCode 模型 ID | 本实验中的实际成本 |
|---|---|---|---|
| 模型 A | MiniMax-M3.1-Flash | `opencode/minimax-m3.1-flash-free` | $0，OpenCode Zen 免费层 |
| 模型 B | MiMo-V2.6-Flash | `opencode/mimo-v2.6-flash-free` | $0，OpenCode Zen 免费层 |

两个模型使用完全相同的 OpenCode 1.18.25 脚手架、build agent、工具权限、预算与提示词。唯一差异是模型本身及其厂商服务。

## 1. 模型选择过程

初版评估模型为 DeepSeek-V4.1-Flash 与 GLM-5.3-Flash。两模型在四道 pilot 题上首轮全部通过，失败率 0%，无法为反馈条件提供样本。

随后筛选六个免费模型。五个可用模型在 T14 与 T20 上均首轮通过，见第 5 节。按用户决定，评估模型替换为导航稳定且免费的 MiniMax-M3.1-Flash 与 MiMo-V2.6-Flash，同时将 T14 与 T20 改造为多缺陷题。

替换后首轮失败率仍为 0%。按用户决定，第一轮工具调用上限收紧至 10 次，重跑 pilot 后两个模型各为 2 通过 2 失败，合计失败率 50%，进入预注册区间。详细记录见 `../../LOG/2026-10-21_model_screen.md`、`../../LOG/2026-10-21_multi_defect_revision.md`、`../../LOG/2026-10-21_budget_tightening.md` 与 `../../RECORD/pilot/v5/summary.md`。

## 2. 模型 A：MiniMax-M3.1-Flash

### 2.1 身份与版本

| 项 | 值 |
|---|---|
| 报告名 | MiniMax-M3.1-Flash，OpenCode Zen 免费层 |
| OpenCode 模型 ID | `opencode/minimax-m3.1-flash-free` |
| 厂商 | MiniMax |
| 发布日期 | 2026-10-19，models.dev 记录 |
| 开源权重 | 否，models.dev 标注 |

### 2.2 能力与限制

| 项 | 值 |
|---|---|
| 上下文窗口 | 1,000,000 tokens |
| 最大输出 | 512,000 tokens |
| 输入模态 | 文本、图像、视频 |
| 输出模态 | 文本 |
| 工具调用 | 支持 |
| 推理模式 | 支持 |
| 温度参数 | 支持，实验不强制，使用 provider 默认值 |

### 2.3 接入方式与价格

通过 OpenCode Zen 免费层接入，无独立 API key。实际边际成本为 0。付费路径的目录价仅作参考，不作为实际支出报告。

| 项目 | 值 |
|---|---|
| 目录参考来源 | models.dev 的 merge-gateway 与 zenmux 条目，MiniMax M3.1 Flash |
| 输入 | 0.15 USD / 1M tokens |
| 输出 | 0.60 USD / 1M tokens |
| 缓存读取 | 0.015 USD / 1M tokens |

## 3. 模型 B：MiMo-V2.6-Flash

### 3.1 身份与版本

| 项 | 值 |
|---|---|
| 报告名 | MiMo-V2.6-Flash，OpenCode Zen 免费层 |
| OpenCode 模型 ID | `opencode/mimo-v2.6-flash-free` |
| 厂商 | 小米 |
| 发布日期 | 2026-09-22，models.dev 记录 |
| 开源权重 | 是，models.dev 标注 |

### 3.2 能力与限制

| 项 | 值 |
|---|---|
| 上下文窗口 | 200,000 tokens |
| 最大输出 | 32,000 tokens |
| 输入模态 | 文本、图像、音频、视频 |
| 输出模态 | 文本 |
| 工具调用 | 支持 |
| 推理模式 | 支持 |
| 温度参数 | 支持，实验不强制，使用 provider 默认值 |

免费条目的上下文为 200k，小于付费 MiMo-V2.6-Flash 的 1M。实验题目仓库不足 300 行，该限制不构成约束。

### 3.3 接入方式与价格

通过 OpenCode Zen 免费层接入，无独立 API key。实际边际成本为 0。

| 项目 | 值 |
|---|---|
| 目录参考来源 | models.dev 的 xiaomi/mimo-v2.6-flash 条目 |
| 输入 | 0.14 USD / 1M tokens |
| 输出 | 0.28 USD / 1M tokens |
| 缓存读取 | 0.0028 USD / 1M tokens |

## 4. 两模型对照

| 项目 | MiniMax-M3.1-Flash | MiMo-V2.6-Flash |
|---|---|---|
| 厂商 | MiniMax | 小米 |
| 发布日期 | 2026-10-19 | 2026-09-22 |
| 开源权重 | 否 | 是 |
| 上下文 | 1,000,000 | 200,000 |
| 最大输出 | 512,000 | 32,000 |
| 输入模态 | 文本、图像、视频 | 文本、图像、音频、视频 |
| 成本 | 免费层 | 免费层 |

两个模型属于不同厂商，规模与开放程度不同。实验比较的是同一脚手架与预算下两个实际可用的免费代码模型，不是同规模受控比较。结论不用于厂商排序，反馈效应按模型内部分析，模型间交互单独报告。

## 5. 免费模型筛选记录

筛选在 T14 与 T20 上各运行一次，预算为 15 次工具调用。

| 模型 | 机构 | T14 | T20 | T20 工具调用 |
|---|---|---|---|---|
| mimo-v2.6-flash-free | 小米 | 通过 | 通过 | 10 |
| minimax-m3.1-flash-free | MiniMax | 通过 | 通过 | 12 |
| nemotron-3.5-lightning-free | NVIDIA | 通过 | 通过 | 19 |
| longcat-2.5-preview-free | 美团 | 通过 | 通过 | 11 |
| big-pickle | 未知 | 通过 | 通过 | 8 |
| beam-free | 未知 | 区域不可用 | 未测 | 0 |

nemotron 在完整 pilot 中把工作目录误判为 `/workspace`，三次失败均未产生源码改动，属于环境导航失败，因此未选为评估模型。

## 6. 固定不变的实验条件

| 项目 | 值 |
|---|---|
| 脚手架 | OpenCode 1.18.25，`opencode run`，`--format json`，`--pure`，`--auto` |
| Agent | `build` |
| 工具 | read、edit、write、glob、grep、list、bash 仅允许 `python -m pytest*` |
| 禁用工具 | webfetch、websearch、external_directory、task、skill、lsp、doom_loop |
| 步数上限 | 20 |
| 第一轮工具调用上限 | 10 |
| 第二轮工具调用上限 | 15 |
| 修改上限 | edit 与 write 合计 8 次 |
| 超时 | 300 秒 |
| 成本上限 | 0.50 USD，安全阀，免费层不会触及 |
| 温度 | provider 默认值 |
| 测试处理 | 每次运行后恢复 tests 目录并做哈希校验 |

## 7. 证据来源

- models.dev `api.json`，条目 `opencode/minimax-m3.1-flash-free` 与 `opencode/mimo-v2.6-flash-free`，2026-10-21
- OpenCode Zen 模型列表，2026-10-21
- 本机 OpenCode 1.18.25 运行记录，2026-10-21
