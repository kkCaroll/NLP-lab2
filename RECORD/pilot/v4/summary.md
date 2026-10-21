# 多缺陷 pilot 首轮结果

## 目的

将 T14 与 T20 改造为多缺陷题，并换用 minimax-m3.1-flash-free 与 mimo-v2.6-flash-free，检查首轮失败率。

## 环境

| 项目 | 内容 |
|---|---|
| 日期 | 2026-10-21 |
| 脚手架 | OpenCode 1.18.25 |
| 模型 A | opencode/minimax-m3.1-flash-free |
| 模型 B | opencode/mimo-v2.6-flash-free |
| 费用 | 两个模型均为免费层，费用 0 |
| 提示词 | 主实验第一轮提示词 |
| 步数上限 | 12 |
| 单次超时 | 420 秒 |

## 题目

T14 包含两处独立缺陷。第一处位于共享换算 helper，克分支未换算为千克。第二处位于 total_weight，返回平均重量而非总重量。混合单位目标测试需要同时修复两处。

T20 包含两处独立缺陷。第一处位于共享排序 helper，reverse 与降序键叠加。第二处位于 department_age_order，绕过共享 helper 直接返回输入顺序。部门顺序目标测试需要同时修复两处。

## 结果

| 题目 | Minimax | 工具调用 | MiMo | 工具调用 |
|---|---|---|---|---|
| T01 next_palindrome | 15 passed | 13 | 15 passed | 8 |
| T05 email_regex | 14 passed | 18 | 14 passed | 10 |
| T14 shipping_fee | 17 passed | 13 | 17 passed | 12 |
| T20 multi_key_sort | 16 passed | 16 | 16 passed | 11 |

## 汇总

| 模型 | 首轮通过 | 首轮失败 | 首轮失败率 |
|---|---|---|---|
| MiniMax-M3.1-Flash | 4 | 0 | 0% |
| MiMo-V2.6-Flash | 4 | 0 | 0% |

八次运行均未超时，均未修改测试，均只修改允许的源码文件。两个模型在 T14 与 T20 上都完成了两处修改，补丁与 gold patch 一致，改动为 4 个 diff 行。

## 预算观察

Minimax 在 T05 使用 18 次工具调用，在 T20 使用 16 次，超过主实验的 15 次工具调用上限。MiMo 全部运行在 12 次以内。

若严格执行 15 次工具调用上限，Minimax 的两次运行可能被判定为预算耗尽。该判定依赖终止时机，不能仅根据事后计数确定，需要在主实验 harness 中实际执行上限后再统计。

## 结论

多缺陷设计仍未产生首轮失败。两个模型都能读取全部目标测试，识别两处独立缺陷并完成修复。首轮失败率保持 0%，现有任务与模型组合仍无法为反馈条件提供样本。
