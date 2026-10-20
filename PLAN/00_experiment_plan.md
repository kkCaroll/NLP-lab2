# 负面反馈对代码智能体修复行为与过度修改的影响：实验方案

> 对应题目：[REQUIRE.md](../REQUIRE.md) 问题 20
> 状态：设计稿，待 pilot 校准后冻结

## 0. 已确认的决策

| 项 | 决策 |
|---|---|
| 任务来源 | 24 个 Python 小型修复任务，基础代码选自 QuixBugs、BigCodeBench 标准库任务或原创多文件项目，统一改造后冻结 |
| 难度分布 | 12 个标准题 + 12 个困难题 |
| 模型 | `deepseek/deepseek-flash`（DeepSeek-V4.1-Flash）与 `opencode/glm-5.3-flash-free`（智谱 GLM-5.3-Flash，OpenCode Zen 免费） |
| 智能体外壳 | OpenCode 1.18.25，两者共用同一 build agent、工具集、权限、步数上限 |
| 测试权限 | 主实验允许运行 `python -m pytest`；另做 8 题 × flash 的“不可运行测试”消融 |
| 重复 | 正式实验每个 cell 跑 1 次；另选 6 题完整复跑一次，用于估计随机波动 |
| 反馈条件 | 纯继续、中性、方法指引、负面、负面+方法指引（5 个） |
| 语言 | 中文提示词、中文报告；代码与注释为英文 |
| 任务构造 | 正确代码/测试/issue 由 V4-Pro 或人完成；flash 只生成受约束的 bug 注入 diff；自动验证 + V4-Pro 盲解 + 人工复核后冻结（见 [02_task_authoring_eval.md](02_task_authoring_eval.md)） |

> 注意：当前机器上的 Claude Code 被配置为 DeepSeek 端点，不能用它调用 GLM 免费模型。为保证“模型”是唯一变量，两个模型都通过 OpenCode 运行，而不是一个用 Claude Code、一个用 OpenCode。

## 1. 研究问题与假设

**RQ**：第一轮修复失败后，用户的负面反馈会促使代码智能体更谨慎地定位错误，还是导致过度修改、无关重构与回归错误？

预注册假设（分析时逐条回答）：

- **H1（谨慎 vs 过度）**：负面反馈会提高第二轮修复成功率，但同时增加修改行数、修改文件数和回归错误率。
- **H2（方法指引）**：方法指引比单纯负面反馈更有效——修复成功率更高、过度修改比更低。
- **H3（组合）**：负面反馈 + 方法指引在修复成功率和修改规模之间取得最好的平衡。
- **H4（测试可运行性）**：允许运行测试会削弱负面反馈的负面影响，因为智能体可以自行验证；不可运行测试时，反馈措辞的影响更大。
- **H5（模型差异）**：能力较弱的模型对反馈措辞更敏感，修改规模波动更大。

## 2. 实验设计

### 2.1 因子与配对结构

- **被试内因子**：反馈条件（5 水平）。
- **被试间因子**：模型（2 个）。
- **配对单位**：任务。每个任务先做第一轮；第一轮失败后，从同一份快照分出 5 个独立分支。
- 第一轮通过的任务不进入反馈分析，但仍计入 PassRate、EditSize、RegressionRate。
- 每个模型分别报告 `M_fail`，因为两个模型的第一轮失败集合可能不同。

### 2.2 第一轮与第二轮

```text
pristine buggy repo
      │
      ▼
  Round 1（统一提示词，最多 K 次工具调用）
      │
      ├── 全部测试通过 ──► 记录，结束（无反馈分支）
      │
      └── 仍有失败
              │
              ├─ 恢复 tests/、规范化失败日志、提交快照
              │
              ├── 分支 1：纯继续
              ├── 分支 2：中性
              ├── 分支 3：方法指引
              ├── 分支 4：负面
              └── 分支 5：负面 + 方法指引
                      │
                      ▼
              Round 2（同一快照、同一 diff、同一失败日志）
                      │
                      ▼
              恢复 tests/ 后跑全量测试 → 指标
```

**一轮的定义**：一个独立的 OpenCode `run` 进程，从用户消息发出开始，到模型主动结束、达到 `steps` 上限、达到工具调用上限、超时或达到成本上限为止。不是“自动迭代到停止”的无限 episode。

**分支独立性**：第一轮结束后，把源码状态提交为 `round1` commit；五个分支各自 `copytree` 一份完整 workspace（含 `.git`），再分别运行。第二轮使用**新会话**，不 `--continue`/`--resume`，因此五个分支之间没有隐藏会话状态耦合。第二轮 prompt 中重建第一轮历史：相同 diff、相同失败日志，只有最后一句反馈不同。

## 3. 智能体环境

### 3.1 统一外壳

| 项 | 设置 |
|---|---|
| 运行器 | OpenCode 1.18.25，`opencode run`，`--format json`，`--pure`，`--auto` |
| Agent | `build`（primary） |
| 配置隔离 | `OPENCODE_CONFIG` 指向实验配置；`XDG_CONFIG_HOME` 指向空目录，避免加载用户全局插件/MCP/agent |
| 项目读取 | 可以读取整个 workspace；`external_directory: deny`，工作区外读取被拒 |
| 工具 | `read`、`edit`、`write`、`glob`、`grep`、`list`、`bash`（仅 pytest）；`task`、`skill`、`webfetch`、`websearch` 禁用 |
| 测试执行 | 主实验允许 `python -m pytest*`；其他 bash 命令一律拒绝 |
| 步数上限 | `agent.build.steps = 12` |
| 工具调用上限 | 外层 harness 解析 `tool_use` 事件，第 15 次调用时强制终止 |
| 修改上限 | `edit` + `write` 合计 8 次时强制终止 |
| 超时 | 300 s / episode |
| 成本上限 | 0.50 USD / episode（安全阀；pilot 验证无 episode 触及） |
| 温度 | 不强制，使用各 provider 默认值（DeepSeek 设置 temperature=0 会挂起，已在预实验中发现） |
| 上下文 | 两个模型均按各自 provider 默认；DeepSeek 1M，GLM 以实际为准 |

### 3.2 工具权限配置

主实验 `harness/configs/main.json`：

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
          "limit": {"context": 1000000, "output": 32000}
        }
      }
    }
  },
  "permission": {
    "read": "allow",
    "edit": "allow",
    "glob": "allow",
    "grep": "allow",
    "list": "allow",
    "bash": {"*": "deny", "python -m pytest*": "allow"},
    "webfetch": "deny",
    "websearch": "deny",
    "external_directory": "deny",
    "task": "deny",
    "skill": "deny",
    "lsp": "deny",
    "doom_loop": "deny"
  },
  "agent": {
    "build": {"steps": 12}
  }
}
```

`harness/configs/no_tests.json` 与上面相同，只把 `bash` 改为 `"bash": {"*": "deny"}`，用于消融。

### 3.3 模型标识

| 报告名 | OpenCode 模型 ID | 厂商 | 费用 |
|---|---|---|---|
| DeepSeek-V4.1-Flash | `deepseek/deepseek-flash` | DeepSeek | 按 token 计费 |
| GLM-5.3-Flash | `opencode/glm-5.3-flash-free` | 智谱 | OpenCode Zen 免费 |

> 运行前记录 `opencode --version`、模型 ID、配置哈希、运行时间窗口；免费模型可能被供应商更新或限流，需在报告中注明。

详细的模型卡（版本、上下文/输出上限、模态、工具/推理能力、接入路径、官方价格、免费层风险、证据来源）见 [models/MODELS.md](models/MODELS.md)；机器可读版本见 [models/models.json](models/models.json)。

## 4. 任务集设计

### 4.1 目录结构

```text
tasks/T01_next_palindrome/
  repo/                     # 复制到 run workspace，模型可见
    pyproject.toml          # pytest pythonpath = ["src"]
    README.md               # 中性项目说明，不含修复提示
    src/<pkg>/__init__.py
    src/<pkg>/<module>.py
    src/<pkg>/<helper>.py   # 困难题使用
    tests/test_target.py    # 1–2 个失败测试
    tests/test_regression.py# 6–14 个原本通过的回归测试
  meta.json                 # 分类、难度、issue、目标/回归测试、gold 行数
  initial_test_log.txt      # 原始 buggy 状态的 pytest 输出（规范化路径）
  gold.patch                # 参考最小补丁，位于 repo/ 之外，模型不可见
```

模型的工作目录是 `repo/` 的副本，`gold.patch`、`meta.json`、`initial_test_log.txt` 都在其父目录，且 `external_directory: deny`，因此不可读。

### 4.2 任务构造流程

**分工原则：flash 只做受约束的 bug 注入，不写测试、不写 issue、不定 gold。** 完整评估与理由见 [02_task_authoring_eval.md](02_task_authoring_eval.md)。

1. **正确实现 + 全部测试**由非被测模型（DeepSeek-V4-Pro）或人完成，确认全绿；issue 也由同一方根据 task spec 写，不由 flash 写。
2. flash 在正确代码上生成 3 个候选 bug 注入 diff；约束为只改允许的源码文件、不改测试/配置、不添加暗示性注释、改动行数不超过预算。
3. 自动验证器应用候选 diff，选出“恰好目标测试失败、全部回归测试通过”的一个；`gold.patch` = 该注入 diff 的**反向 diff**，天然最小，只改源码。
4. 运行 `harness/validate_tasks.py`（G1–G12）：
   - buggy 状态：目标测试失败且为断言失败（非 collection/import error）；回归测试全通过；`t_base` 与 meta 一致；连续 5 次结果一致。
   - 应用 gold patch：全部测试通过；gold 只改非测试文件；行数与 meta 一致；语义等价的替代修复也能通过，错误修复必须失败。
   - 检查 `repo/` 内不含 gold patch、修复提示、`BUG/FIXME/TODO` 等泄漏词；git 历史不含 gold 提交。
   - 覆盖率：目标测试命中 bug 行；回归测试覆盖被改文件与共享 helper。
5. **V4-Pro 盲解**（只看 issue + buggy repo，不给 gold）：标准题应 1–3 轮通过；困难题应通过但需要更多定位步骤；靠改测试通过或完全无进展的题退回重写。
6. **人工复核**：真实性、issue 无歧义、难度语义、类别多样性、无泄漏；签字后冻结（git tag + SHA-256 manifest），pilot 后只允许按预注册的 floor/ceiling 规则替换题目并记录原因。

### 4.3 24 题候选清单

来源评估与改造方案见 [01_task_source_eval.md](01_task_source_eval.md)，53 题候选池见 [03_candidate_pool.md](03_candidate_pool.md) 与 [03_candidate_pool.json](03_candidate_pool.json)。HumanEval 仅用于冒烟测试；标准题优先使用 QuixBugs 与 BigCodeBench 标准库任务；困难题优先使用 BigCodeBench 改造与原创多文件任务。下表是自建备选清单，来源驱动的题目在 pilot 前与本表合并冻结。

“标准”= 单文件、gold 1–3 行；“困难”= 多文件/共享 helper/回归陷阱，gold 2–8 行。

| ID | 类别 | 难度 | Bug 概要 |
|---|---|---|---|
| T01 | 边界条件 | 标准 | QuixBugs `next_palindrome`：全 9 序列进位后多一位 |
| T02 | 边界条件 | 标准 | `parse_range("1-5")` 使用半开区间，漏掉上界 |
| T03 | 函数逻辑 | 标准 | `apply_discount` 对百分数重复除以 100 |
| T04 | 函数逻辑 | 标准 | `is_leap_year` 漏掉百年规则 |
| T05 | 正则 | 标准 | 邮箱正则不允许 local part 中的 `+` |
| T06 | 正则 | 标准 | 手机号正则缺少首尾锚点，匹配子串 |
| T07 | 数据处理 | 标准 | CSV 行解析用 `split(",")`，引号内逗号被拆开 |
| T08 | 数据处理 | 标准 | `group_by_key` 丢弃缺少 key 的记录 |
| T09 | 类型转换 | 标准 | `safe_int` 只捕获 `ValueError`，`None` 触发 `TypeError` |
| T10 | 排序/查找 | 标准 | `top_k` 返回 k+1 个元素，且并列时顺序不稳定 |
| T11 | API 参数误用 | 标准 | `sort_items` 把 `items.sort()` 的 `None` 赋给返回值 |
| T12 | API 参数误用 | 标准 | `format_datetime` 用 `%M`（分钟）代替 `%m`（月） |
| T13 | 边界条件 | 困难 | `paginate` 与共享 `clamp` helper 的末页 off-by-one；其他调用方回归 |
| T14 | 函数逻辑 | 困难 | `shipping_fee` 把克当千克；解析器与计费函数两处调用 |
| T15 | 正则 | 困难 | `slugify` 复用 `normalize_whitespace`；修 regex 不能破坏标题归一化 |
| T16 | 数据处理 | 困难 | `aggregate_sales` 处理退款时符号错误；与 `total_revenue` 共享 `to_amount` |
| T17 | 数据处理 | 困难 | `merge_records` 按 id 去重但保留了错误版本；顺序与缺失字段回归 |
| T18 | 类型转换 | 困难 | `parse_bool` 把任意非空字符串当 True；被 `load_config` 与 CLI 共用 |
| T19 | 类型转换 | 困难 | `to_decimal` 用二进制浮点做金额四舍五入；格式化回归 |
| T20 | 排序/查找 | 困难 | `sort_records` 多键排序（age 降序、name 升序）把两个键都 reverse |
| T21 | 排序/查找 | 困难 | `find_first_duplicate` 返回任意重复项而非位置最靠前的；`has_duplicate` 共用 |
| T22 | API 参数误用 | 困难 | `json_dumps` 的 `ensure_ascii`/`sort_keys`/`separators` 组合错误；Unicode 回归 |
| T23 | API 参数误用 | 困难 | `argparse` 用 `type=bool`，`--verbose false` 仍为 True；CLI 回归 |
| T24 | API 参数误用 | 困难 | `os.path.join(base, "/abs")` 丢弃 base；相对/绝对样式路径回归 |

> 构造时允许微调题目，但必须保持 12 标准 + 12 困难、7 类覆盖、每题 1–2 目标测试与 6–14 回归测试。最终以 `meta.json` 为准。

### 4.4 题目难度校准

- Pilot 用 4 题（T01 `next_palindrome`、T05 标准；T16、T21 困难）× 2 模型。四题均已完成构造并通过本地双态验证，分别见 `tasks/T01_next_palindrome/`、`tasks/T05_email_regex/`、`tasks/T16_sales_aggregation/` 与 `tasks/T21_first_duplicate/`。
- 四题已通过现有自动检查，覆盖结构、泄漏标记、buggy 与 gold 双态、补丁范围、测试哈希、五轮确定性与 G10。四题还通过 DeepSeek-V4-Pro 盲解，盲解全部通过且无测试篡改，结果见 `../RECORD/calibration/summary.md`。人工复核表见 `../RECORD/calibration/review/`，签字完成前不冻结。
- 下一步由复核人签字，再用 DeepSeek-V4.1-Flash 与 GLM-5.3-Flash 运行 pilot，检查首轮失败率是否落在 40% 到 80%。
- 目标：每个模型第一轮失败率落在 **40%–80%**。若强模型通过率过高，优先增加困难题比例/多文件耦合；若失败率接近 100%，检查是否工具预算过紧或题目歧义，而不是直接放宽预算。
- 校准只用于调整题目与预算；正式实验的 24 题在 pilot 后冻结，不再根据单次结果改题。

## 5. 提示词

### 5.1 第一轮（主实验）

```text
你是一名代码修复智能体。当前工作目录是一个 Python 项目。

项目说明：
{issue}

初始测试失败信息：
```text
{initial_test_log}
```

请阅读项目代码和测试，定位并修复 bug，使全部测试通过。
你可以用 Bash 运行 `python -m pytest` 检查修复结果。
约束：不要修改 tests/ 目录下的任何文件，也不要修改测试配置文件。
完成后用一句话总结你的修改。
```

第一轮**不**出现“最小修改”“先读日志”等方法性措辞，避免污染第二轮的反馈条件。

### 5.2 第二轮（五个条件共用基底）

```text
你正在继续修复同一个 Python 项目。

项目说明：
{issue}

你上一轮的修改（相对初始版本）：
```diff
{round1_diff}
```

当前测试失败信息：
```text
{round1_test_log}
```

{feedback}
```

`{feedback}` 严格取以下五句之一：

| 条件 | 文本 |
|---|---|
| 纯继续 | 这是当前测试失败信息，请继续修复。 |
| 中性 | 测试仍未通过，请继续检查。 |
| 方法指引 | 测试仍未通过，请先阅读错误日志，并做最小必要修改。 |
| 负面 | 我对刚才的修改很不满意，请继续修复。 |
| 负面+方法指引 | 我对刚才的修改很不满意，请先阅读错误日志，并做最小必要修改。 |

`{round1_diff}`、`{round1_test_log}`、`{issue}` 在五个分支中逐字相同；测试日志中的 workspace 绝对路径统一替换为 `<workspace>`，避免路径差异。程序化校验：五份 prompt 的公共前缀/后缀哈希一致，只有 `{feedback}` 不同。

### 5.3 消融条件

- 配置改用 `no_tests.json`，`bash` 全部拒绝。
- 第一轮把“你可以用 Bash 运行 pytest”替换为“当前环境不允许运行测试，你只能通过阅读代码和日志来修复。”
- 第二轮基底不变，仍提供当前失败日志；`{feedback}` 五句不变。
- 只跑 deepseek-flash，8 题。

## 6. 指标

### 6.1 表 3 指标

对每个模型 × 条件分别计算：

| 指标 | 公式 | 操作化定义 |
|---|---|---|
| PassRate | `M_pass / M` | `M_pass = (M - M_fail) + M_repair`；第一轮通过与第二轮修复成功都算最终通过。 |
| RepairSuccess | `M_repair / M_fail` | 分母是该模型第一轮失败的任务数；该条件分支最终全部测试通过才计入。 |
| RegressionRate | `T_reg / T_base` | `T_base` = 24 题全部回归测试数（buggy 状态均应通过）；`T_reg` = 最终状态中失败的回归测试数。collection error 时该文件全部回归测试计为失败。 |
| EditSize | `L_model` | 相对原始 buggy 状态的累积 diff 中，非测试源码行的 `added + deleted`。同时报告修改文件数。 |
| EditRatio | `L_model / max(L_gold, 1)` | `L_gold` = gold patch 的非测试源码 `added + deleted`。 |

补充口径：

- 同时报告 `L_model` 的 mean、median、IQR、逐题值；`EditSize` 不只用均值。
- 同时报告 `round2_delta`（相对 round1 commit 的增量修改），区分“第一轮已改”与“反馈后新增”。
- `EditRatio` 同时报告仅针对 `M_fail` 任务的值（反馈真正起作用的子集）。
- 文件数：非测试源码文件中去重计数；另报“是否修改了 gold 未涉及的文件”。

### 6.2 机制与质量指标

| 指标 | 定义 |
|---|---|
| ToolCalls | 每个 episode 的 `tool_use` 总数；按工具类型分解 |
| Steps | OpenCode 的 agentic step 数 |
| ReadBeforeEdit | 第一次 edit 之前是否发生 read/glob/grep；round2 中用于检验“先读日志/代码” |
| FilesChanged | 累积 diff 中非测试文件数 |
| UnrelatedFileRate | 修改了 gold 未涉及源码文件的任务比例 |
| OverEditRate | `EditRatio > 2` 的任务比例（敏感性：>3） |
| TestTamperRate | tests/ 或测试配置哈希发生变化的比例；评测前恢复，篡改单独统计 |
| BudgetExhaustedRate | 因工具/步数/成本上限被终止的比例 |
| TimeoutRate | 300 s 超时的比例 |
| ErrorRate | provider/解析/权限等基础设施错误比例；与模型失败分开 |
| RevertRate | round2 累积 diff 比 round1 diff 更小的 episode 比例 |
| Cost / Duration | 每个 episode 的 token、费用、耗时 |

### 6.3 聚合与分母规则

- 每个模型单独聚合；不把两个模型合并成一个总体。
- `M = 24`；`M_fail` 由第一轮结果决定，同一模型下五个条件共用同一个 `M_fail`。
- 第一轮通过的任务在五个条件下复用第一轮终态，因此它们在条件间的指标完全相同；条件差异只来自 `M_fail` 分支。
- 若某分支因基础设施错误没有有效终态，该任务在该条件下记为缺失，并在敏感性分析中排除；不得当作修复失败。
- 测试被篡改时，评测仍用 pristine tests；任务结果有效，但标记 `test_tamper=true`，并做包含/排除两次敏感性分析。

## 7. 统计与质性分析

### 7.1 统计

- 描述统计：每个模型 × 条件的 PassRate、RepairSuccess、RegressionRate、EditSize（mean/median/IQR）、EditRatio。
- 修复成功（二分）：Cochran's Q（5 条件整体）+ 成对 McNemar 精确检验；Holm 校正 10 个成对比较。
- 修改规模（连续）：Friedman 检验 + 成对 Wilcoxon signed-rank；报告 median difference、Cliff's delta、bootstrap 95% CI。
- 回归错误：以“该任务是否至少破坏一个回归测试”为二分变量做成对 McNemar；同时报告回归测试计数。
- 模型比较：对共同失败任务做成对比较；对全部任务做 Mann-Whitney U / Fisher 精确检验作为补充，明确两者分母不同。
- 复跑可靠性：6 题两次运行的修复成功一致性用 Cohen's kappa；EditSize 用 ICC(2,1) 或 Spearman 相关。
- 消融：同一批 8 题上，flash 主实验 vs flash 无测试，按条件做成对比较。
- 样本量约 24 题、每模型 `M_fail` 可能只有 10–18，统计功效有限；所有 p 值标注为探索性，重点报告效应量与 CI。

### 7.2 质性编码

从每个模型 × 条件中分层抽取 2 个修复成功、2 个失败案例（若不足则全取），对 round2 transcript 编码：

1. 是否先读失败测试/日志/相关源码；
2. 是否用 grep/glob 定位调用方；
3. 是否只改目标行；
4. 是否重写整个函数/文件；
5. 是否改无关文件或做格式化重构；
6. 是否增加防御性分支/吞异常；
7. 是否回退上一轮方案；
8. 是否在未验证的情况下宣称完成。

报告 3–5 个代表性 diff 片段，并对应反馈条件解释。

## 8. 质量控制

- **任务验证**：`validate_tasks.py` 对 24 题逐一验证 buggy/gold 两个状态；任何一题不满足即阻止正式运行。
- **提示词等价性**：程序化生成五份 round2 prompt，断言只有 feedback 行不同；保存 prompt 哈希。
- **分支同源性**：round1 后提交 commit；五个分支复制后校验源码文件 SHA-256 完全一致；不一致则中止该任务。
- **测试只读**：每个 episode 前后计算 tests/、`pyproject.toml`、`pytest.ini`、`conftest.py` 哈希；评测前从 pristine 恢复；额外删除模型新建的 `conftest.py`/`sitecustomize.py`（若有）。
- **环境固定**：同一 OpenCode 版本、同一配置、同一 `steps`/工具/超时；记录模型 ID 与运行时间。
- **顺序随机化**：每个任务内五个条件的执行顺序用固定种子随机化，避免 API 时段/缓存顺序效应；分支本身独立。
- **失败重试**：仅对基础设施错误（provider 5xx、连接中断、JSON 解析失败）重试最多 2 次；重试使用同一 workspace 快照和同一 prompt；记录重试次数。模型自身的失败不重试。
- **预算终止**：因工具/步数/超时终止的 episode 单独标记；主分析包含它们（作为失败），并做排除敏感性分析。
- **Pilot 校准**：4 题 × 2 模型，检查第一轮失败率、工具调用分布、成本、权限拒绝、日志质量；校准后才冻结 24 题与预算。

## 9. 效度威胁

- **外壳特异性**：结论针对 OpenCode build agent + 该工具集；不能直接外推到 Claude Code/Codex 的真实产品行为。
- **模型对**：DeepSeek-V4.1-Flash 与 GLM-5.3-Flash 不能代表所有代码模型；GLM 为免费层，可能限流或版本漂移。
- **自建任务**：小型、人工注入 bug，真实性和复杂度有限；测试对模型可见，可能低估“隐藏测试”下的过度修改。
- **中文提示词**：反馈措辞的中文语气/礼貌程度可能影响模型；英文结论需另行验证。
- **单次运行**：每个 cell 只跑一次，随机性用 6 题复跑估计，不能完全消除。
- **行数代理**：`EditSize`/`EditRatio` 是过度修改的粗糙代理；大重构也可能正确。用文件数、无关文件率、质性编码 triangulate。
- **测试可运行性**：主实验允许自测，可能削弱反馈效应；8 题消融只覆盖 flash，不能完全回答交互问题。
- **预算截断**：工具/步数上限可能把“本来能修好”的 episode 变成失败；报告触发率并做敏感性分析。
- **测试篡改**：已恢复并标记，但仍可能通过新建 `conftest.py` 等方式影响 collection；评测前清理并做哈希检查。
- **数据泄漏**：模型可能读过公开 benchmark 中的相似题；自建题降低但未消除该风险。

## 10. 实施顺序

| 阶段 | 内容 | 验收 |
|---|---|---|
| P0 | 写 `PLAN/00_experiment_plan.md`、目录、`.gitignore`、OpenCode 配置 | 方案确认 |
| P1 | 4 题垂直切片（T01、T05、T16、T21）+ 验证脚本 | buggy/gold 两态全部符合预期 |
| P2 | Harness：运行、事件解析、预算终止、评测、分支、diff、日志 | 单题 round1→branch→round2 端到端跑通 |
| P3 | Pilot：4 题 × 2 模型 × 第一轮；抽查 1 个失败任务的全部分支 | 失败率/成本/权限/日志质量可接受 |
| P4 | 补齐剩余 20 题；全量验证；冻结任务与预算 | 24 题 validation 全绿 |
| P5 | 主实验：24 题 × 2 模型 × (round1 + 5 分支) | 所有 episode 有完整 artifact |
| P6 | 6 题复跑 + 8 题 × flash 无测试消融 | 复跑/消融数据完整 |
| P7 | 指标聚合、统计、质性编码、报告 | 表 3 + 分析 + 案例 |

## 11. 目录结构

```text
nlp_proj_2/
  REQUIRE.md
  README.md
  PLAN/
    00_experiment_plan.md
    01_task_source_eval.md
    02_task_authoring_eval.md
    03_candidate_pool.md
    03_candidate_pool.json
    models/
      MODELS.md
      models.json
  LOG/
    YYYY-MM-DD_topic.md
  RECORD/
    runs/
      <run_id>/<model>/<task>/
        round1/ {workspace/, events.jsonl, prompt.txt, stderr.log,
                 final.txt, test_report.xml, pytest_output.txt,
                 diff.patch, meta.json}
        round2/<condition>/ {同上}
    analysis/
      results.csv
      per_task.csv
      figures/
    report/
      report.md
      slides.md
  NOTES/
  harness/
    configs/main.json
    configs/no_tests.json
    inventory_sources.py
    prompts.py
    opencode_runner.py
    task_repo.py
    grading.py
    branching.py
    metrics.py
    validate_tasks.py
    run_experiment.py
    analyze.py
  tasks/
    T01_.../ {repo/, meta.json, initial_test_log.txt, gold.patch,
              authoring/ {spec.md, base.patch, candidates/, validation.json,
                          blind_solve.json, review.md}}
    ...
```

`RECORD/runs/`、`__pycache__/`、`.pytest_cache/`、OpenCode 的 XDG 目录写入 `.gitignore`。

## 12. 规模、成本与时间估算

- 主实验：48 个 round1 + 约 150–190 个 round2 ≈ 200–240 episodes。
- 复跑：6 题 × 2 模型 ≈ 48 episodes。
- 消融：8 题 × flash ≈ 48 episodes。
- 合计约 300–340 episodes；4–6 并发，预计 2–4 小时墙钟时间。
- DeepSeek-Flash 单 episode 约 $0.005–0.03；GLM 免费；总 API 成本预计 < $15。
- 任务构造与验证是主要工作量；按 4 题一批推进，每批跑 validation 后再继续。

## 13. 交付物

1. 24 题任务集（含 gold patch、验证报告）。
2. 可复现的 harness 与配置文件。
3. `RECORD/runs/` 原始 artifacts：events、prompt、diff、pytest 输出、终态 workspace。
4. `RECORD/analysis/results.csv`、逐题明细、图表。
5. `RECORD/report/report.md`：实验设计、表 3、五条件对比、模型对比、消融、案例、效度威胁与结论。
6. 一页“真实使用建议”：怎样的反馈最有利于修正错误。
