# 主实验聚合 2026-10-21_reliability

有效任务记录 60 行，缺失 0 项。

| 模型 | 条件 | 有效题数 | 第一轮通过 | 修复成功 | PassRate | RepairSuccess | RegressionRate | EditSize 中位数 | EditRatio 中位数 | OverEditRate |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| opencode/minimax-m3.1-flash-free | pure_continue | 6 | 1 | 4 | 0.833 | 0.800 | 0.000 | 3.000 | 1.000 | 0.167 |
| opencode/minimax-m3.1-flash-free | neutral | 6 | 1 | 4 | 0.833 | 0.800 | 0.000 | 3.000 | 1.000 | 0.167 |
| opencode/minimax-m3.1-flash-free | method_guidance | 6 | 1 | 4 | 0.833 | 0.800 | 0.000 | 2.000 | 1.000 | 0.000 |
| opencode/minimax-m3.1-flash-free | negative | 6 | 1 | 3 | 0.667 | 0.600 | 0.000 | 2.000 | 0.700 | 0.000 |
| opencode/minimax-m3.1-flash-free | negative_guidance | 6 | 1 | 3 | 0.667 | 0.600 | 0.000 | 2.000 | 0.500 | 0.000 |
| opencode/mimo-v2.6-flash-free | pure_continue | 6 | 4 | 2 | 1.000 | 1.000 | 0.000 | 2.500 | 1.000 | 0.000 |
| opencode/mimo-v2.6-flash-free | neutral | 6 | 4 | 2 | 1.000 | 1.000 | 0.000 | 2.500 | 1.000 | 0.000 |
| opencode/mimo-v2.6-flash-free | method_guidance | 6 | 4 | 2 | 1.000 | 1.000 | 0.000 | 3.500 | 1.000 | 0.000 |
| opencode/mimo-v2.6-flash-free | negative | 6 | 4 | 2 | 1.000 | 1.000 | 0.000 | 3.000 | 1.000 | 0.000 |
| opencode/mimo-v2.6-flash-free | negative_guidance | 6 | 4 | 2 | 1.000 | 1.000 | 0.000 | 2.000 | 1.000 | 0.000 |

## 分支子集

第一轮失败任务的第二轮分支，不含第一轮通过任务在五条件中复用的终态。

| 模型 | 条件 | 有效题数 | 第一轮通过 | 修复成功 | PassRate | RepairSuccess | RegressionRate | EditSize 中位数 | EditRatio 中位数 | OverEditRate |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| opencode/minimax-m3.1-flash-free | pure_continue | 5 | 0 | 4 | 0.800 | 0.800 | 0.000 | 4 | 1.000 | 0.200 |
| opencode/minimax-m3.1-flash-free | neutral | 5 | 0 | 4 | 0.800 | 0.800 | 0.000 | 4 | 1.000 | 0.200 |
| opencode/minimax-m3.1-flash-free | method_guidance | 5 | 0 | 4 | 0.800 | 0.800 | 0.000 | 2 | 1.000 | 0.000 |
| opencode/minimax-m3.1-flash-free | negative | 5 | 0 | 3 | 0.600 | 0.600 | 0.000 | 2 | 0.400 | 0.000 |
| opencode/minimax-m3.1-flash-free | negative_guidance | 5 | 0 | 3 | 0.600 | 0.600 | 0.000 | 2 | 0.400 | 0.000 |
| opencode/mimo-v2.6-flash-free | pure_continue | 2 | 0 | 2 | 1.000 | 1.000 | 0.000 | 3.500 | 0.500 | 0.000 |
| opencode/mimo-v2.6-flash-free | neutral | 2 | 0 | 2 | 1.000 | 1.000 | 0.000 | 4.500 | 0.600 | 0.000 |
| opencode/mimo-v2.6-flash-free | method_guidance | 2 | 0 | 2 | 1.000 | 1.000 | 0.000 | 5.500 | 0.800 | 0.000 |
| opencode/mimo-v2.6-flash-free | negative | 2 | 0 | 2 | 1.000 | 1.000 | 0.000 | 4.500 | 0.700 | 0.000 |
| opencode/mimo-v2.6-flash-free | negative_guidance | 2 | 0 | 2 | 1.000 | 1.000 | 0.000 | 3.500 | 0.400 | 0.000 |
