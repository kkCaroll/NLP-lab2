# harness 目录

本目录存放实验运行与评测代码。

| 文件 | 内容 |
|---|---|
| inventory_sources.py | 静态读取 tasks/_sources 下的来源快照并生成候选池 |
| configs/ | `main/opencode.json` 主实验配置，`ablation/opencode.json` 无测试消融配置，`blind/opencode.json` 盲解配置 |
| prompts.py | 第一轮模板、第二轮公共前缀与五种反馈句 |
| opencode_runner.py | 启动 OpenCode、收集事件、执行工具调用与编辑次数上限 |
| task_repo.py | 任务仓库复制、git 状态固定、测试文件哈希校验与 diff |
| grading.py | pytest JUnit XML 解析与目标测试、回归测试评分 |
| branching.py | 第一轮失败后的五条件分支 |
| metrics.py | episode 指标计算 |
| validate_tasks.py | 结构、泄漏、双态、补丁范围、测试哈希与确定性检查 |
| check_variants.py | G10 等价修复与错误修复检查 |
| blind_solve.py | 在隔离 OpenCode 配置下执行盲解并评分 |
| run_experiment.py | 单题端到端运行，后续扩展为批量、复跑与消融入口 |
| analyze.py | 统计检验与图表生成，后续添加 |

每个脚本只负责一个阶段。运行命令写入 LOG，不写入本文件。
