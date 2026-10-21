# 替换后 pilot 首轮结果

## 目的

用 T14 与 T20 替换 T16 与 T21 后，重新检查两道被测模型的首轮失败率是否进入预注册的 40% 到 80% 区间。

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
| T01 next_palindrome | 标准 | 15 passed | 7 | 15 passed | 5 |
| T05 email_regex | 标准 | 14 passed | 10 | 14 passed | 10 |
| T14 shipping_fee | 困难 | 16 passed | 9 | 16 passed | 9 |
| T20 multi_key_sort | 困难 | 16 passed | 10 | 16 passed | 10 |

## 汇总

| 模型 | 首轮通过 | 首轮失败 | 首轮失败率 | 总费用 |
|---|---|---|---|---|
| DeepSeek-V4.1-Flash | 4 | 0 | 0% | 0.008050 美元 |
| GLM-5.3-Flash | 4 | 0 | 0% | 0 美元 |

八次运行均未超时，均未修改测试，均只修改允许的源码文件。八次运行的补丁均与 gold patch 完全一致，改动均为 2 个 diff 行，编辑次数均为 1。

## 结论

替换为共享 helper 题后，两道模型仍在首轮全部通过，失败率保持 0%。模型能够直接沿调用链定位共享层，T14 与 T20 的耦合设计没有提高首轮失败率。现有 pilot 题集无法产生反馈分支所需的首轮失败样本。

## 待决策

在调整 pilot 或实验设计前，不进入主实验。备选方案见 LOG 中的记录。
