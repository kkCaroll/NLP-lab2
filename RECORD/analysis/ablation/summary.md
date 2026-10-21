# 主实验聚合 2026-10-21_ablation

有效任务记录 80 行，缺失 0 项。

| 模型 | 条件 | 有效题数 | 第一轮通过 | 修复成功 | PassRate | RepairSuccess | RegressionRate | EditSize 中位数 | EditRatio 中位数 | OverEditRate |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| opencode/minimax-m3.1-flash-free | pure_continue | 8 | 0 | 8 | 1.000 | 1.000 | 0.000 | 4.000 | 1.000 | 0.250 |
| opencode/minimax-m3.1-flash-free | neutral | 8 | 0 | 7 | 0.875 | 0.875 | 0.000 | 2.000 | 1.000 | 0.000 |
| opencode/minimax-m3.1-flash-free | method_guidance | 8 | 0 | 8 | 1.000 | 1.000 | 0.000 | 3.000 | 1.000 | 0.000 |
| opencode/minimax-m3.1-flash-free | negative | 8 | 0 | 4 | 0.500 | 0.500 | 0.000 | 2.000 | 0.450 | 0.125 |
| opencode/minimax-m3.1-flash-free | negative_guidance | 8 | 0 | 6 | 0.750 | 0.750 | 0.000 | 2.500 | 0.800 | 0.000 |
| opencode/mimo-v2.6-flash-free | pure_continue | 8 | 6 | 2 | 1.000 | 1.000 | 0.000 | 3.000 | 1.000 | 0.000 |
| opencode/mimo-v2.6-flash-free | neutral | 8 | 6 | 2 | 1.000 | 1.000 | 0.000 | 3.000 | 1.000 | 0.000 |
| opencode/mimo-v2.6-flash-free | method_guidance | 8 | 6 | 2 | 1.000 | 1.000 | 0.000 | 3.000 | 1.000 | 0.000 |
| opencode/mimo-v2.6-flash-free | negative | 8 | 6 | 2 | 1.000 | 1.000 | 0.000 | 3.000 | 1.000 | 0.000 |
| opencode/mimo-v2.6-flash-free | negative_guidance | 8 | 6 | 2 | 1.000 | 1.000 | 0.000 | 3.000 | 1.000 | 0.000 |

## 分支子集

第一轮失败任务的第二轮分支，不含第一轮通过任务在五条件中复用的终态。

| 模型 | 条件 | 有效题数 | 第一轮通过 | 修复成功 | PassRate | RepairSuccess | RegressionRate | EditSize 中位数 | EditRatio 中位数 | OverEditRate |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| opencode/minimax-m3.1-flash-free | pure_continue | 8 | 0 | 8 | 1.000 | 1.000 | 0.000 | 4.000 | 1.000 | 0.250 |
| opencode/minimax-m3.1-flash-free | neutral | 8 | 0 | 7 | 0.875 | 0.875 | 0.000 | 2.000 | 1.000 | 0.000 |
| opencode/minimax-m3.1-flash-free | method_guidance | 8 | 0 | 8 | 1.000 | 1.000 | 0.000 | 3.000 | 1.000 | 0.000 |
| opencode/minimax-m3.1-flash-free | negative | 8 | 0 | 4 | 0.500 | 0.500 | 0.000 | 2.000 | 0.450 | 0.125 |
| opencode/minimax-m3.1-flash-free | negative_guidance | 8 | 0 | 6 | 0.750 | 0.750 | 0.000 | 2.500 | 0.800 | 0.000 |
| opencode/mimo-v2.6-flash-free | pure_continue | 2 | 0 | 2 | 1.000 | 1.000 | 0.000 | 3.000 | 0.700 | 0.000 |
| opencode/mimo-v2.6-flash-free | neutral | 2 | 0 | 2 | 1.000 | 1.000 | 0.000 | 3.000 | 0.700 | 0.000 |
| opencode/mimo-v2.6-flash-free | method_guidance | 2 | 0 | 2 | 1.000 | 1.000 | 0.000 | 3.000 | 0.700 | 0.000 |
| opencode/mimo-v2.6-flash-free | negative | 2 | 0 | 2 | 1.000 | 1.000 | 0.000 | 4.000 | 0.800 | 0.000 |
| opencode/mimo-v2.6-flash-free | negative_guidance | 2 | 0 | 2 | 1.000 | 1.000 | 0.000 | 3.000 | 0.700 | 0.000 |
