# 对比模型信息卡

> 核对日期：2026-10-20
> 本文件记录问题 20 实验中两个被评估代码模型的实际接入方式与参数。实验运行时以本文件 + `models.json` 为准；若厂商在实验期间变更模型版本或价格，应在结果中注明抓取日期与版本号。

## 0. 一句话结论

| 角色 | 模型 | OpenCode 模型 ID | 本实验中的实际成本 |
|---|---|---|---|
| 模型 A | DeepSeek-V4.1-Flash | `deepseek/deepseek-flash` | 按 DeepSeek 官方人民币价目计费 |
| 模型 B | GLM-5.3-Flash | `opencode/glm-5.3-flash-free` | $0（OpenCode Zen 免费层） |

两个模型使用**完全相同的 OpenCode 1.18.25 脚手架、build agent、工具权限、步数上限和提示词**；唯一差异是模型本身及其厂商服务。

---

## 1. 模型 A：DeepSeek-V4.1-Flash

### 1.1 身份与版本

| 项 | 值 |
|---|---|
| 报告/展示名 | DeepSeek-V4.1-Flash |
| OpenCode 模型 ID | `deepseek/deepseek-flash` |
| API `model` 字段 | `deepseek-flash` |
| 实际服务版本 | `DeepSeek-V4.1-Flash-1017`（官方 `/models` 返回） |
| 厂商 | DeepSeek（深度求索） |
| 模型类型 | 文本 + 图像输入，文本输出；支持工具调用、推理/思考模式 |
| 发布日期 | 2026-09-10（models.dev 记录）；版本号 `1017` |
| 知识截止 | 2025-05（models.dev 记录） |
| 开源权重 | models.dev 标注 `open_weights: true`（以官方发布为准） |

### 1.2 能力与限制

| 项 | 值 |
|---|---|
| 上下文窗口 | 1,048,576 tokens（1M） |
| 最大输出 | 393,216 tokens（API `/models`）；官方文档写 384K |
| 输入模态 | 文本、图像 |
| 输出模态 | 文本 |
| 工具调用（function calling） | 支持 |
| JSON 输出 | 支持 |
| 思考模式 | 支持；有 `low / high / max` 三档，默认 `high`；默认开启思考 |
| 温度参数 | 支持（但 OpenCode 中显式设 `temperature: 0` 会导致请求挂起，本实验不强制温度） |
| Anthropic 兼容 API | 支持（`https://api.deepseek.com/anthropic`） |
| 并发限制 | 2500（官方文档） |

### 1.3 接入方式

本实验通过 OpenCode 的自定义 provider 接入，使用 OpenAI 兼容协议：

```json
{
  "provider": {
    "deepseek": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "DeepSeek",
      "options": {
        "baseURL": "https://api.deepseek.com/v1",
        "apiKey": "{env:ANTHROPIC_AUTH_TOKEN}"
      },
      "models": {
        "deepseek-flash": {
          "name": "DeepSeek V4.1 Flash",
          "tool_call": true,
          "reasoning": true,
          "limit": { "context": 1000000, "output": 32000 }
        }
      }
    }
  }
}
```

说明：

- `apiKey` 从环境变量读取，不写入仓库。
- Anthropic 兼容端点（`https://api.deepseek.com/anthropic`）也可用，但本实验统一走 OpenAI 兼容端点，避免不同协议下的工具调用差异。
- 实际运行命令形如：
  ```bash
  XDG_CONFIG_HOME=<isolated-config> opencode run \
    --model deepseek/deepseek-flash \
    --agent build --format json --pure --auto "<prompt>"
  ```

### 1.4 官方价格（人民币，每 100 万 tokens）

来源：DeepSeek 官方价格页 `https://api-docs.deepseek.com/zh-cn/quick_start/pricing`，核对于 2026-10-20。

| 项目 | 空闲时段 | 高峰时段 |
|---|---:|---:|
| 输入（缓存命中） | ¥0.02 | ¥0.04 |
| 输入（缓存未命中） | ¥1 | ¥2 |
| 输出 | ¥4 | ¥8 |

- **高峰时段**：北京时间周一至周五 9:00–12:00、14:00–18:00（法定节假日除外）。
- **空闲时段**：其余所有时间，价格为高峰的一半。
- 本实验的 24 题 × 多条件规模很小，预计总成本在 **¥10–¥30** 量级（含重跑与消融），远低于预算上限；实际成本以 API 账单为准。
- 不启用联网搜索/网页抓取（OpenCode 权限已 deny），因此不涉及搜索计费。

### 1.5 使用注意

- 官方 `/models` 返回的服务版本是 `DeepSeek-V4.1-Flash-1017`，但厂商可能在不改模型名的前提下滚动更新；报告中应固定写“实验于 2026-10-20 使用 `deepseek-flash`，当日服务版本为 `DeepSeek-V4.1-Flash-1017`”。
- 思考模式默认开启，会消耗额外输出 tokens；本实验不关闭思考，以保持两个模型都使用默认推理行为。若做敏感性分析，可另跑一组 `reasoning_effort=low`，但不属于主实验。
- 旧模型名（如 `deepseek-chat`）在 2026-10-20 会映射到 V4.1-Flash，因此本实验显式使用 `deepseek-flash`，避免歧义。

---

## 2. 模型 B：GLM-5.3-Flash

### 2.1 身份与版本

| 项 | 值 |
|---|---|
| 报告/展示名 | GLM-5.3-Flash |
| OpenCode 模型 ID | `opencode/glm-5.3-flash-free` |
| 目录规范 ID | `zhipuai/glm-5.3-flash` |
| 厂商 | 智谱 AI（Zhipu AI） |
| 模型类型 | 原生多模态；文本/图像/视频/PDF 输入，文本输出；支持工具调用与推理 |
| 发布日期/更新 | 2026-08-26（models.dev） |
| 开源权重 | models.dev 标注 `open_weights: true` |

### 2.2 能力与限制

| 项 | 值 |
|---|---|
| 上下文窗口 | 1,000,000 tokens |
| 最大输出 | 131,072 tokens |
| 输入模态 | 文本、图像、视频、PDF |
| 输出模态 | 文本 |
| 工具调用 | 支持 |
| 推理/思考 | 支持（`low / high / max`，默认 `high`） |
| 温度参数 | 支持 |
| 结构化输出 | 支持 |
| 接入路径 | OpenCode Zen 免费层（`opencode/glm-5.3-flash-free`） |

### 2.3 接入方式

```bash
XDG_CONFIG_HOME=<isolated-config> opencode run \
  --model opencode/glm-5.3-flash-free \
  --agent build --format json --pure --auto "<prompt>"
```

- 该模型由 OpenCode Zen 提供，免费层无需额外 API key；实际可用性、限流和模型版本由 OpenCode 控制。
- 本实验在 2026-10-20 的冒烟测试中确认：该 ID 可以完成“读文件 → 编辑 → 运行 `python -m pytest`”的完整工具链。

### 2.4 价格

| 口径 | 数值 |
|---|---|
| 本实验实际计费 | **$0**（OpenCode Zen 免费层） |
| models.dev 目录参考价（`opencode-go/glm-5.3-flash`，非本实验接入路径） | 输入 $0.15 / 输出 $0.50 / 缓存读 $0.03 每 100 万 tokens |
| 官方 API 价格 | 以智谱官方价目为准；本实验未使用官方付费 API，报告中不应把目录参考价当作实际支出 |

注意：

- 免费层的**速率限制、并发上限、是否会在高峰期排队**均未公开；必须在预实验中记录失败率与延迟。如果免费层在正式实验期间出现大量 429/5xx，应改为固定时段重跑，或换用同一模型的付费端点（并在报告中说明）。
- `glm-5.3-flash-free` 与付费的 `glm-5.3-flash` 是否完全同一权重/量化版本，OpenCode 未明确承诺；报告中应写“通过 OpenCode Zen 免费层访问的 GLM-5.3-Flash”，不要写成“智谱官方 API 的 GLM-5.3-Flash”。

---

## 3. 两模型对照表

| 维度 | DeepSeek-V4.1-Flash | GLM-5.3-Flash |
|---|---|---|
| 厂商 | DeepSeek | 智谱 AI |
| 接入 | DeepSeek 官方 API（OpenAI 兼容） | OpenCode Zen 免费层 |
| 服务版本 | V4.1-Flash-1017 | GLM-5.3-Flash（免费层） |
| 上下文 | 1,048,576 | 1,000,000 |
| 最大输出 | 393,216（API）/ 384K（文档） | 131,072 |
| 工具调用 | 支持 | 支持 |
| 思考模式 | 支持，默认 high | 支持，默认 high |
| 输入模态 | 文本、图像 | 文本、图像、视频、PDF |
| 开源权重 | 是（models.dev） | 是（models.dev） |
| 实际成本 | 按官方人民币价目 | $0 |
| 主要风险 | 版本滚动、思考 token 成本 | 免费层限流、版本/量化不透明 |

**可比性说明**：两者不是同一参数规模/同一价格档的模型，本实验比较的是“在相同 agent 脚手架下，两个可实际获得的低成本代码模型对负反馈的反应差异”，而不是严格的同预算同规模对照。报告中应明确这一点，避免把结论外推为“厂商 A 优于厂商 B”。

---

## 4. 固定不变的实验条件

以下条件对两个模型完全一致，写入 `PLAN/00_experiment_plan.md` 并在每次运行前由 harness 校验：

| 条件 | 值 |
|---|---|
| Agent 脚手架 | OpenCode 1.18.25 |
| Agent | `build` |
| 工具权限 | read/edit/glob/grep/list allow；bash 仅 `python -m pytest*`；webfetch/websearch/task/skill/lsp/external_directory/doom_loop deny |
| 最大 agent 步数 | 12 |
| 外部硬上限 | 15 次工具调用 / 8 次编辑 / 300 秒 / $0.50 安全上限 |
| 测试执行 | 允许运行 `python -m pytest`；测试文件只读，运行后恢复并校验哈希 |
| 提示词 | 两模型逐字相同，仅模型 ID 不同 |
| 轮次定义 | 一轮 = 一个 OpenCode 进程；不自动迭代 |
| 温度 | 不强制，使用提供方默认 |
| 工作目录 | 每题独立 git 仓库快照，路径归一化为 `<workspace>` |

---

## 5. 证据来源

| 信息 | 来源 | 核对日期 |
|---|---|---|
| DeepSeek 模型 ID、上下文、输出、模态、工具/推理 | `GET https://api.deepseek.com/models` | 2026-10-20 |
| DeepSeek 官方人民币价格、峰谷时段、并发 | `https://api-docs.deepseek.com/zh-cn/quick_start/pricing` | 2026-10-20 |
| DeepSeek 版本号、发布日、知识截止、开源权重 | models.dev `https://models.dev/api.json` | 2026-10-20 |
| GLM 上下文、输出、模态、工具/推理、发布日、开源权重、目录价 | models.dev `https://models.dev/api.json`（`opencode-go/glm-5.3-flash`） | 2026-10-20 |
| GLM 免费层可用性 | OpenCode Zen `GET /zen/v1/models` + 本地冒烟测试 | 2026-10-20 |
| OpenCode 版本与权限行为 | 本地 `opencode --version` + 冒烟测试 | 2026-10-20 |

> 价格和模型版本会变。正式报告应附一张“实验运行时间窗 + 当日模型版本 + 当日价格”的小表，而不是只引用本文档。
