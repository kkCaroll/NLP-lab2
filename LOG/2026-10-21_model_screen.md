# 2026-10-21 免费模型筛选与隔离修复

## 目的

按用户决定，筛选价格为零且能力较弱的可用模型，替换现有两道被测模型。

## 候选模型

OpenCode 当前可用的免费模型如下。

| 模型 | 机构 | T14 结果 | T20 结果 | T20 工具调用 |
|---|---|---|---|---|
| mimo-v2.6-flash-free | 小米 | 通过 | 通过 | 10 |
| minimax-m3.1-flash-free | MiniMax | 通过 | 通过 | 12 |
| nemotron-3.5-lightning-free | NVIDIA | 通过 | 通过 | 19 |
| longcat-2.5-preview-free | 美团 | 通过 | 通过 | 11 |
| big-pickle | 未知 | 通过 | 通过 | 8 |
| beam-free | 未知 | 区域不可用 | 未测 | 0 |

所有可用模型在 T14 与 T20 上均首轮通过，补丁与 gold patch 一致。nemotron-3.5-lightning-free 的 T20 运行使用 19 次工具调用与 284 秒，接近或超过主实验的 15 次工具调用上限。

## 隔离问题与修复

首轮 T20 筛选时，nemotron-3.5-lightning-free 修改了原始题目目录 `tasks/T20_multi_key_sort/repo/src/recordkit/keys.py`，没有修改工作副本，导致题目仓库被改成 gold 状态。随后 longcat 与 big-pickle 在 gold 状态上运行，结果为假通过。nemotron 当时的失败补丁也是由该问题造成。

已采取两项修复。

1. 从 git 恢复 T20 题目仓库，并确认 buggy 状态为 2 failed 与 14 passed。
2. `harness/blind_solve.py` 改为在系统临时目录中创建工作副本，运行前后对原始题目仓库做全量哈希校验，若被修改则从快照恢复。补丁基线改用运行前快照。

修复后重新筛选，五个可用模型在 T20 上均通过，原始题目仓库哈希保持不变。此前无效的筛选结果已删除。

## 完整 pilot 试探

用 nemotron-3.5-lightning-free 运行 T01、T05、T14、T20。

| 题目 | 结果 | 工具调用 | 编辑次数 |
|---|---|---|---|
| T01 next_palindrome | 通过 | 9 | 1 |
| T05 email_regex | 失败 | 21 | 1 |
| T14 shipping_fee | 失败 | 13 | 0 |
| T20 multi_key_sort | 失败 | 14 | 0 |

三次失败均未产生源码改动。事件显示模型把工作目录理解为 `/workspace` 或 `/repo`，在 Windows 临时目录中反复执行无效路径命令，最终未定位或修改源码。这是环境导航失败，不是修复失败，不能作为反馈实验的有效样本。

## 结论

模型替换不能单独解决首轮失败率为零的问题。可用的免费模型在能够正常导航时都能解决现有单行缺陷任务。能力较弱的模型还会把预算消耗在路径与环境探测上，产生无进展失败。

若继续更换模型，建议同时调整任务设计，使失败来自修复判断而不是环境导航。候选组合为 minimax-m3.1-flash-free 与 mimo-v2.6-flash-free，两者导航稳定且免费。任务侧建议采用多缺陷设计。

## 状态

未执行 git commit。`harness/blind_solve.py` 的隔离修复尚未提交。
