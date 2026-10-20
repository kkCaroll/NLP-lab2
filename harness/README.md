# harness 目录

本目录存放实验运行与评测代码。

| 文件 | 内容 |
|---|---|
| inventory_sources.py | 静态读取 tasks/_sources 下的来源快照并生成候选池 |
| configs/ | 主实验与消融实验的 OpenCode 配置，后续添加 |
| prompts.py | 五种反馈条件的提示词模板，后续添加 |
| opencode_runner.py | 启动 OpenCode、收集事件与执行预算控制，后续添加 |
| task_repo.py | 任务仓库复制、测试文件哈希校验与补丁应用，后续添加 |
| grading.py | pytest JUnit XML 解析与指标计算，后续添加 |
| branching.py | 第一轮失败后的五条件分支，后续添加 |
| metrics.py | 指标定义与聚合，后续添加 |
| validate_tasks.py | 结构、泄漏、双态、补丁范围、测试哈希与确定性检查 |
| check_variants.py | G10 等价修复与错误修复检查 |
| blind_solve.py | 用 V4-Pro 在隔离 OpenCode 配置下执行盲解并评分 |
| run_experiment.py | 主实验、复跑与消融的统一入口，后续添加 |
| analyze.py | 统计检验与图表生成，后续添加 |

每个脚本只负责一个阶段。运行命令写入 LOG，不写入本文件。
