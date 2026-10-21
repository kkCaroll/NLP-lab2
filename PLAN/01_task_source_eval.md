# 24 题任务来源评估与重新规划

## 结论

可以使用现有基准的基础代码，但不建议直接把原始任务搬进实验。

HumanEval 不适合作为主来源，主要原因是题目饱和、污染严重、单函数、缺少回归面。BigCodeBench 可以作为标准题的基础代码来源，但需要筛选标准库任务并改造为多文件项目。QuixBugs 适合标准题，已有 buggy 与 fixed 对照以及测试数据，但题目较老、污染较高、只有单文件。困难题不建议直接使用 BigCodeBench-Hard，因为它的难是算法难，不是定位难；更合适的是把现有函数放进多文件项目，通过共享 helper 和多个调用方制造定位难度与回归面。

推荐的来源结构如下。

| 难度 | 数量 | 主来源 | 作用 |
|---|---:|---|---|
| 标准 | 6 | QuixBugs | 直接提供 buggy 与 fixed 对照，改造为小型包并补充回归测试 |
| 标准 | 6 | BigCodeBench 标准库任务 | 提供更接近真实库调用的代码，注入最小 bug |
| 困难 | 6 | BigCodeBench 或 BigCodeBench-Hard 改造 | 把函数放入多文件项目，bug 注入共享 helper 或调用链 |
| 困难 | 6 | 原创多文件任务 | 覆盖正则、数据处理、类型转换、API 误用等缺口，控制污染 |

如果时间紧张，可以先做 12 道标准题加 12 道原创多文件困难题，跳过真实 bug 提交。这样可控性和可复现性最好。

## 1. 实验需求与来源匹配

| 需求 | HumanEval | BigCodeBench | QuixBugs | 原创多文件 |
|---|---|---|---|---|
| 至少 20 题 | 164 题，足够 | 1140 题，足够 | 40 题，偏少 | 可扩展 |
| 自带 buggy 代码 | 否 | 否 | 是 | 是 |
| 至少一个失败测试 | 需注入后构造 | 需注入后构造 | 是 | 是 |
| 多个原本通过的回归测试 | 弱，同一函数 | 中，同一函数多方法 | 中，同一函数多用例 | 强，可跨文件 |
| 最小 gold patch | 需反向构造 | 需反向构造 | 已提供 fixed 版本 | 由注入 diff 反向得到 |
| 七类错误覆盖 | 偏算法 | 较广 | 偏算法 | 可按需覆盖 |
| 定位难度 | 低 | 低到中 | 低 | 高 |
| 过度修改可测性 | 低 | 低到中 | 低 | 高 |
| 污染风险 | 高 | 中到高 | 高 | 低到中 |
| 许可 | MIT | Apache-2.0 | MIT | 自有 |

核心判断是，现有函数级基准可以提供代码和测试，但不能直接提供本实验最需要的两样东西，即回归面和定位难度。必须经过统一改造。

## 2. 候选来源评估

### 2.1 HumanEval

规模 164 题，MIT 许可，函数级，提供 prompt、canonical solution 和一个 check 函数。check 函数内部是若干 assert。

优点是指标成熟、代码短、运行快。缺点是当前模型通过率很高，首轮失败样本可能不足；题目全部是单函数，模型只要改一个函数就能通过，无法观察无关文件修改和回归错误；check 函数通常只覆盖目标函数，不能作为真正的回归测试；公开时间早，训练数据污染严重。

结论是只用于 harness 冒烟测试和简单基线，不作为 24 道主题目来源。

### 2.2 BigCodeBench

规模 1140 题，Apache-2.0 许可，函数级，覆盖 139 个库，提供 complete prompt、instruct prompt、canonical solution 和 unittest 测试类。BigCodeBench-Hard 是 148 题的较难子集。

优点是任务更接近真实库调用，测试类通常有多个测试方法，可以拆分目标测试与回归测试；任务类型比 HumanEval 丰富，较容易覆盖数据处理、正则、日期时间、JSON、argparse 等类别。

缺点仍然是单函数，回归面有限；大量任务依赖第三方库，环境重、运行慢、版本敏感；测试类可能共享 setup，拆分后需要检查独立性；2024 年发布，主流模型很可能见过；仓库已归档，但数据仍可使用。

结论是作为标准题的主要基础代码来源，并作为困难题改造的素材。使用前必须筛选只依赖标准库或依赖稳定的任务。

### 2.3 QuixBugs

规模 40 题，MIT 许可，提供 python_programs 与 correct_python_programs 两套代码，以及 json_testcases 测试数据。每题通常有多个输入输出用例，可以直接拆成目标用例和回归用例。

优点是已经有人工确认的 buggy 与 fixed 对照，gold patch 可以直接从两者 diff 得到；测试数据现成；题目短，改造快。

缺点是全部为单文件算法题，bug 多为一行逻辑错误，定位难度低；题目来自经典算法，模型极可能见过；错误类型集中在边界、逻辑、排序查找，缺少正则、数据处理、类型转换、API 误用；只有 40 题，去掉不适合的题目后可选范围更小。

结论是用于 6 道左右标准题，不作为困难题来源。

### 2.4 BugsInPy

规模 493 个真实 bug，来自 17 个 Python 项目，提供 buggy 与 fixed 版本、项目测试和相关 bug 信息。

优点是真实项目、多文件、真实回归测试，生态效度最高。缺点是仓库没有 LICENSE 文件，默认版权状态下不适合直接复制代码进公开仓库；环境依赖重，需要 Docker 或逐个项目配置；测试可能很慢，部分 bug 依赖数据库或网络；没有现成 issue 文本，需要自己写；从 493 个 bug 中筛出 6 到 12 个适合 300 秒预算的小任务，工作量不小。

结论是不作为主来源。只有在许可澄清并且能提取最小复现时，才考虑用作困难题补充。

### 2.5 SWE-bench

真实 GitHub issue 与 repo 级测试，生态效度高，但任务规模大、环境重、运行时间长，不适合每题 300 秒、15 次工具调用的统一预算。公开数据集污染也较严重。

结论是不适用。

### 2.6 GitHub 小型 bug 修复提交

从 MIT 或 Apache-2.0 的小型 Python 项目中挑选 bug 修复提交，检出父提交，确认新增测试失败，修复提交作为 gold。优点是真实、多文件、污染相对低，可以使用模型知识截止之后的提交。缺点是筛选成本高，需要逐仓库检查许可、依赖、测试速度和测试稳定性。

结论是可选。若时间允许，用 4 到 6 道困难题，优先选择 2025 年之后的小型提交。

### 2.7 DebugBench

规模 4253 个合成 bug，Apache-2.0 许可，提供 oracle code 与 buggy code，覆盖 Python、Java、C++，有错误类型标签。

优点是 bug 类型全，可以作为错误模式清单。缺点是合成数据、无测试、题目多为竞赛编程风格，且包含大量语法错误，例如缺少冒号、非法关键字、括号不匹配。这些错误太容易被发现，不适合研究定位与过度修改。

结论是只作为 bug 模式参考，不作为题目来源。

### 2.8 原创多文件任务

由我们或非被测模型编写正确代码、测试与 issue，再注入 bug。优点是完全控制文件规模、调用链、回归面、错误类型和污染程度；gold 由注入 diff 反向得到，天然最小。缺点是有作者偏差和编写成本。

结论是困难题的主要来源，也是七类错误覆盖的补缺手段。

## 3. 推荐改造流程

现有基准的原始任务不能直接入库。每一道题都要经过以下改造。

1. 选基础代码。标准题从 QuixBugs 或 BigCodeBench 标准库任务中选。困难题从 BigCodeBench 较复杂任务或原创代码中选。
2. 放入统一项目结构。至少包含 `src/pkg/module.py`，困难题再增加 `src/pkg/helper.py` 和两个以上调用方。标准题 2 到 4 个源文件，困难题 4 到 8 个源文件。
3. 写 issue。只描述用户观察到的错误行为和期望行为，不写修复位置，不写“最小修改”。
4. 注入 bug。标准题允许一行逻辑错误。困难题把 bug 注入共享 helper，或注入调用链中间层，使模型必须跨文件定位。
5. 拆分测试。目标测试 1 到 2 个，回归测试 6 到 14 个。回归测试必须覆盖被修改文件、共享 helper 和其他调用方。
6. 生成 gold。gold 等于注入 diff 的反向 diff，只改源码，不改测试。
7. 自动验证。运行 G1 到 G12，检查双态、回归基线、gold 最小性、测试只读、确定性、泄漏、覆盖率、反过拟合。
8. 盲解校准。由不参与评测的 DeepSeek-V4-Pro 只看 issue 和 buggy 仓库，确认题目可解且不过易。
9. 人工复核。检查真实性、歧义、难度语义、类别多样性和许可标注。
10. 冻结。记录来源 URL、commit hash、原始许可、修改说明和 SHA-256。

## 4. 24 题来源分配建议

题号只作为槽位。具体题目优先从来源中选，原有 T01 到 T24 清单保留为备选。若来源题无法通过验证，再回退到原有题目。无论采用哪一种，最终都必须保持 12 道标准题、12 道困难题和七类错误覆盖。

| 题号 | 类别 | 难度 | 建议来源 | 改造方式 |
|---|---|---|---|---|
| T01 | 边界条件 | 标准 | QuixBugs `find_first_in_sorted` | 保留 buggy 版本，拆目标与回归用例 |
| T02 | 边界条件 | 标准 | QuixBugs `find_in_sorted` | 保留 buggy 版本，增加边界回归 |
| T03 | 函数逻辑 | 标准 | QuixBugs `gcd` 或 `next_palindrome` | 保留 buggy 版本，包装为小模块 |
| T04 | 函数逻辑 | 标准 | QuixBugs `next_permutation` | 保留 buggy 版本，增加相邻行为测试 |
| T05 | 正则 | 标准 | BigCodeBench 标准库 `re` 任务 | 注入字符类或量词错误 |
| T06 | 正则 | 标准 | BigCodeBench 标准库 `re` 任务 | 注入锚点或转义错误 |
| T07 | 数据处理 | 标准 | BigCodeBench `csv` 或 `json` 任务 | 注入分隔符或编码处理错误 |
| T08 | 数据处理 | 标准 | BigCodeBench 字典聚合任务 | 注入缺失键处理错误 |
| T09 | 类型转换 | 标准 | BigCodeBench `int` 或 `float` 解析任务 | 注入异常类型遗漏 |
| T10 | 排序查找 | 标准 | QuixBugs `quicksort` 或 `kth` | 保留 buggy 版本，增加稳定性回归 |
| T11 | API 误用 | 标准 | BigCodeBench 列表排序任务 | 注入原地排序返回值错误 |
| T12 | API 误用 | 标准 | BigCodeBench `datetime` 任务 | 注入格式符错误 |
| T13 | 边界条件 | 困难 | BigCodeBench 分页任务改造 | 增加共享 `clamp` helper 和多个调用方 |
| T14 | 函数逻辑 | 困难 | BigCodeBench 单位换算任务改造 | 增加解析器与计费函数两条调用链 |
| T15 | 正则 | 困难 | 原创 slugify 任务 | 共享 `normalize_whitespace`，增加标题归一化回归 |
| T16 | 数据处理 | 困难 | BigCodeBench 销售聚合任务改造 | 共享 `to_amount`，增加退款与总收入回归 |
| T17 | 数据处理 | 困难 | 原创 merge_records 任务 | 多版本记录与缺失字段回归 |
| T18 | 类型转换 | 困难 | BigCodeBench 配置解析任务改造 | 共享 `parse_bool`，增加 CLI 回归 |
| T19 | 类型转换 | 困难 | 原创金额四舍五入任务 | 使用 Decimal，增加格式化回归 |
| T20 | 排序查找 | 困难 | BigCodeBench 多键排序任务改造 | 增加多调用方与稳定性回归 |
| T21 | 排序查找 | 困难 | QuixBugs `find_first_in_sorted` 改造 | 增加 `has_duplicate` 共享 helper |
| T22 | API 误用 | 困难 | 原创 `json_dumps` 任务 | 组合参数与 Unicode 回归 |
| T23 | API 误用 | 困难 | 原创 argparse 任务 | `type=bool` 与 CLI 回归 |
| T24 | API 误用 | 困难 | 原创路径拼接任务 | 绝对路径与相对路径回归 |

这张表是候选分配，不是最终题目清单。实际选择时以能否通过 G1 到 G12、能否产生首轮失败、能否覆盖七类错误为准。

## 5. 污染控制

公开基准的题目大多早于模型知识截止。HumanEval 和 QuixBugs 的污染风险最高，BigCodeBench 次之。可采取以下措施。

1. 改写标识符、常量、文件结构和调用链，不保留原始题目的完整片段。
2. issue 用中文重新描述行为，不复述原始 docstring。
3. 目标测试与回归测试重新组织，不只使用原始测试。
4. 对候选题目做记忆探测。只给函数签名和简短描述，要求模型补全实现，若与 canonical solution 高度相似则标记。
5. 优先使用 2025 年之后的 GitHub 小型修复提交，或完全原创的困难题。
6. 在报告中披露污染风险，不声称题目无污染。

## 6. 许可与引用

| 来源 | 许可 | 使用要求 |
|---|---|---|
| HumanEval | MIT | 保留 LICENSE 与版权声明，注明来源 |
| BigCodeBench | Apache-2.0 | 保留 LICENSE、NOTICE，注明修改 |
| QuixBugs | MIT | 保留 LICENSE 与版权声明 |
| DebugBench | Apache-2.0 | 仅参考 bug 模式时也要引用 |
| BugsInPy | 未提供 LICENSE | 不建议直接复用，需先澄清许可 |
| GitHub 提交 | 逐仓库检查 | 只选 MIT 或 Apache-2.0，记录 commit hash |

每道题在 `meta.json` 中记录来源、URL、commit hash、原始许可、修改说明。报告中引用对应论文。

## 7. 实施顺序

1. 下载并检查三个来源，建立 40 到 60 题的候选池。
2. 按七类错误和两个难度层打标签，检查类别缺口。
3. 选出 24 题，先改造 4 道 pilot 题。初版为 T01、T05、T16、T21，pilot 校准后替换为 T01、T05、T14、T20。
4. 对 pilot 题跑自动验证、V4-Pro 盲解和人工复核。
5. Pilot 通过后批量改造剩余 20 题。
6. 冻结题目，进入主实验。

预计来源筛选与改造 1 到 2 个工作日，验证与复核 1 个工作日。若只做标准题加原创困难题，可以缩短到 1 个工作日。

## 8. 最终建议

采用混合来源，不采用单一基准。

HumanEval 只用于冒烟测试。标准题以 QuixBugs 和 BigCodeBench 标准库任务为主。困难题以 BigCodeBench 改造和原创多文件任务为主。BugsInPy、SWE-bench 和 GitHub 提交只在许可、环境和时间都满足时作为补充。

无论来源如何，题目都必须经过统一改造、自动验证、V4-Pro 盲解和人工复核。原始基准任务不能直接进入正式实验。

## 9. 实施进展

2026-10-20 已完成来源下载与候选池构建。QuixBugs 40 道题，BigCodeBench 1140 题，HumanEval 164 题仅用于冒烟测试。按标准库依赖、测试导入、断言数和类别筛选后得到 53 题候选池，其中 QuixBugs 22 题，BigCodeBench 31 题。候选池见 `03_candidate_pool.md` 与 `03_candidate_pool.json`。

T01 已按候选池完成构造，题目为 QuixBugs `next_palindrome`，见 `../tasks/T01_next_palindrome/`。buggy 状态为 4 failed 与 5 passed，gold 状态为 9 passed，gold patch 为一行改动。

T05、T16、T21 已完成构造。T05 改编自 BigCodeBench 761，类别为正则，难度为标准，buggy 状态为 2 failed 与 12 passed，gold 状态为 14 passed，源码 4 个文件 113 行。T16 改编自 BigCodeBench 741，类别为数据处理，难度为困难，buggy 状态为 3 failed 与 13 passed，gold 状态为 16 passed，源码 7 个文件 251 行。T21 改编自 QuixBugs `find_first_in_sorted` 并加入原创重复值工具，类别为排序查找，难度为困难，buggy 状态为 3 failed 与 16 passed，gold 状态为 19 passed，源码 7 个文件 279 行。三道题均通过 `../harness/validate_tasks.py` 的结构、泄漏、双态、补丁范围与测试哈希检查，构造记录见 `../LOG/`。

T01 初版源码规模为 2 个文件 40 行，低于标准题 100 行的下限。现已增加数字校验、转换、前缀镜像与报告模块，并补充 6 个回归测试，源码规模达到 4 个文件 117 行，buggy 状态为 4 failed 与 11 passed，gold 状态为 15 passed。四道 pilot 题均通过 `../harness/validate_tasks.py` 的五轮确定性检查。

T02 为原创标准题，题目为闭区间解析 `parse_range`，见 `../tasks/T02_parse_range/`。源码 4 个文件 119 行，buggy 状态为 2 failed 与 13 passed，gold 状态为 15 passed，gold patch 为一行改动。该题通过五轮确定性检查与 G10 检查，构造记录见 `../LOG/2026-10-20_T02_construction.md`。

T03 为原创标准题，题目为百分比折扣 `apply_discount`，见 `../tasks/T03_apply_discount/`。源码 4 个文件 109 行，buggy 状态为 2 failed 与 16 passed，gold 状态为 18 passed，gold patch 为一行改动。该题通过五轮确定性检查与 G10 检查，构造记录见 `../LOG/2026-10-20_T03_construction.md`。

四道 pilot 题已完成 DeepSeek-V4-Pro 盲解。四题全部通过，步数 5 到 6，工具调用 10 到 15，均未修改测试。T21 达到 15 次工具调用上限，需在正式实验中区分正常完成与预算耗尽。盲解汇总见 `../RECORD/calibration/summary.md`，人工复核表见 `../RECORD/calibration/review/`。

2026-10-21 完成全部 24 题的 DeepSeek-V4-Pro 盲解。24 题全部通过，无测试篡改，无超时，工具调用 6 至 15 次，修改文件均在 `allowed_files` 内，合计费用 0.227416 美元。困难题在步数上与标准题接近，仅工具调用略多，难度分层仍需以被测模型的失败率为准。逐题结果见 `../RECORD/calibration/summary.md`，24 份复核表见 `../RECORD/calibration/review/`，签字完成前不冻结。

2026-10-21 完成被测模型 pilot。DeepSeek-V4.1-Flash 与 GLM-5.3-Flash 在 T01、T05、T16、T21 上首轮全部通过，失败率为 0%，低于预注册的 40% 到 80% 区间，结果见 `../RECORD/pilot/summary.md`。按预注册的 floor 与 ceiling 替换规则，T16 与 T21 对当前模型代际过易，pilot 题集改为 T01、T05、T14、T20。T14 已构造完成，源码 6 个文件 290 行，buggy 状态为 2 failed 与 14 passed，gold 状态为 16 passed，通过五轮确定性检查与 G10 检查，构造记录见 `../LOG/2026-10-21_T14_construction.md`。T20 已构造完成，源码 6 个文件 264 行，buggy 状态为 2 failed 与 14 passed，gold 状态为 16 passed，同样通过五轮确定性检查与 G10 检查，构造记录见 `../LOG/2026-10-21_T20_construction.md`。T16 与 T21 保留为正式任务，并记录其 pilot 难度不足的情况，主实验分析时需单独报告。

2026-10-21 完成多缺陷改造。T14 增加 total_weight 返回平均重量而非总重量的缺陷，源码 6 个文件 292 行，buggy 状态为 3 failed 与 14 passed，gold 状态为 17 passed，gold patch 涉及两个文件。T20 增加 department_age_order 绕过共享排序 helper 的缺陷，源码 6 个文件 264 行，buggy 状态为 2 failed 与 14 passed，gold 状态为 16 passed，gold patch 涉及两个文件。两题均通过验证与多文件变体检查，记录见 `../LOG/2026-10-21_multi_defect_revision.md`。

免费模型筛选与多缺陷 pilot 显示，minimax-m3.1-flash-free 与 mimo-v2.6-flash-free 仍在 T01、T05、T14、T20 上首轮全部通过，失败率 0%，结果见 `../RECORD/pilot/v4/summary.md`。现有任务与模型组合无法产生反馈分支所需的首轮失败样本。

2026-10-21 完成首轮预算收紧。第一轮工具调用上限定为 10 次，由 harness 逐行解析 `tool_use` 事件并在计数达到上限时终止进程树。重跑 pilot 后 MiniMax-M3.1-Flash 与 MiMo-V2.6-Flash 各为 2 通过 2 失败，合计失败率 50%，进入 40% 到 80% 区间，结果见 `../RECORD/pilot/v5/summary.md`。四次失败中三次没有源码改动，一次只修复两处缺陷中的一处，失败全部出现在困难题。第一轮预算冻结为 10 次，第二轮保持 15 次，五个反馈条件使用相同预算。

2026-10-21 完成标准题批次一。新增 T04 `next_permutation`、T06 `version_scan`、T07 `group_counts` 与 T08 `inventory_summary`，类别分别为函数逻辑、正则、数据处理与数据处理。四题源码为 4 个文件 101 至 142 行，buggy 状态均为 2 failed，gold 状态全部通过，五轮确定性检查与 G10 变体检查通过。标准题达到 8 道，困难题仍为 4 道，任务集累计 12 题。构造记录见 `../LOG/2026-10-21_standard_batch_1.md`。

2026-10-21 完成标准题批次二。新增 T09 `safe_int`、T10 `top_k`、T11 `sort_items` 与 T12 `format_datetime`，类别分别为类型转换、排序查找、API 误用与 API 误用。四题源码为 4 个文件 102 至 153 行，buggy 状态均为 2 failed，gold 状态全部通过，五轮确定性检查与 G10 变体检查通过。标准题达到 12 道，困难题仍为 4 道，任务集累计 16 题。构造记录见 `../LOG/2026-10-21_standard_batch_2.md`。

2026-10-21 完成困难题批次。新增 T13 `paginate`、T15 `slugify`、T17 `merge_records`、T18 `parse_bool`、T19 `to_decimal`、T22 `json_dumps`、T23 `parse_flags` 与 T24 `join_path`，类别分别为边界条件、正则、数据处理、类型转换、类型转换、API 误用、API 误用与 API 误用。八题源码为 6 至 7 个文件 260 至 306 行，buggy 状态均为 2 failed，gold 状态全部通过，五轮确定性检查与 G10 变体检查通过。标准题 12 道与困难题 12 道齐备，任务集累计 24 题。构造记录见 `../LOG/2026-10-21_hard_batch.md`。
