# 主实验聚合 2026-10-21_main

有效任务记录 240 行，缺失 0 项。

| 模型 | 条件 | 有效题数 | 第一轮通过 | 修复成功 | PassRate | RepairSuccess | RegressionRate | EditSize 中位数 | EditRatio 中位数 | OverEditRate |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| opencode/minimax-m3.1-flash-free | pure_continue | 24 | 10 | 12 | 0.917 | 0.857 | 0.000 | 2.000 | 1.000 | 0.083 |
| opencode/minimax-m3.1-flash-free | neutral | 24 | 10 | 9 | 0.792 | 0.643 | 0.000 | 2.000 | 1.000 | 0.083 |
| opencode/minimax-m3.1-flash-free | method_guidance | 24 | 10 | 11 | 0.875 | 0.786 | 0.000 | 2.000 | 1.000 | 0.042 |
| opencode/minimax-m3.1-flash-free | negative | 24 | 10 | 9 | 0.792 | 0.643 | 0.000 | 2.000 | 1.000 | 0.083 |
| opencode/minimax-m3.1-flash-free | negative_guidance | 24 | 10 | 13 | 0.958 | 0.929 | 0.000 | 2.000 | 1.000 | 0.042 |
| opencode/mimo-v2.6-flash-free | pure_continue | 24 | 18 | 6 | 1.000 | 1.000 | 0.000 | 2.000 | 1.000 | 0.000 |
| opencode/mimo-v2.6-flash-free | neutral | 24 | 18 | 5 | 0.958 | 0.833 | 0.000 | 2.000 | 1.000 | 0.000 |
| opencode/mimo-v2.6-flash-free | method_guidance | 24 | 18 | 6 | 1.000 | 1.000 | 0.000 | 2.000 | 1.000 | 0.000 |
| opencode/mimo-v2.6-flash-free | negative | 24 | 18 | 5 | 0.958 | 0.833 | 0.000 | 2.000 | 1.000 | 0.042 |
| opencode/mimo-v2.6-flash-free | negative_guidance | 24 | 18 | 6 | 1.000 | 1.000 | 0.000 | 2.000 | 1.000 | 0.000 |

## 分支子集

第一轮失败任务的第二轮分支，不含第一轮通过任务在五条件中复用的终态。

| 模型 | 条件 | 有效题数 | 第一轮通过 | 修复成功 | PassRate | RepairSuccess | RegressionRate | EditSize 中位数 | EditRatio 中位数 | OverEditRate |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| opencode/minimax-m3.1-flash-free | pure_continue | 14 | 0 | 12 | 0.857 | 0.857 | 0.000 | 2.000 | 1.000 | 0.071 |
| opencode/minimax-m3.1-flash-free | neutral | 14 | 0 | 9 | 0.643 | 0.643 | 0.000 | 2.000 | 1.000 | 0.071 |
| opencode/minimax-m3.1-flash-free | method_guidance | 14 | 0 | 11 | 0.786 | 0.786 | 0.000 | 2.000 | 1.000 | 0.000 |
| opencode/minimax-m3.1-flash-free | negative | 14 | 0 | 9 | 0.643 | 0.643 | 0.000 | 2.000 | 1.000 | 0.071 |
| opencode/minimax-m3.1-flash-free | negative_guidance | 14 | 0 | 13 | 0.929 | 0.929 | 0.000 | 2.000 | 1.000 | 0.000 |
| opencode/mimo-v2.6-flash-free | pure_continue | 6 | 0 | 6 | 1.000 | 1.000 | 0.000 | 4.000 | 1.000 | 0.000 |
| opencode/mimo-v2.6-flash-free | neutral | 6 | 0 | 5 | 0.833 | 0.833 | 0.000 | 3.500 | 0.800 | 0.000 |
| opencode/mimo-v2.6-flash-free | method_guidance | 6 | 0 | 6 | 1.000 | 1.000 | 0.000 | 4.000 | 1.000 | 0.000 |
| opencode/mimo-v2.6-flash-free | negative | 6 | 0 | 5 | 0.833 | 0.833 | 0.000 | 3.000 | 1.000 | 0.167 |
| opencode/mimo-v2.6-flash-free | negative_guidance | 6 | 0 | 6 | 1.000 | 1.000 | 0.000 | 3.500 | 1.000 | 0.000 |
