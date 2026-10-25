# 报告 v1 插图

本目录存放报告 v1 与演示使用的六张图，由 `harness/make_figures_v1.py` 生成，版式与配色沿用 v0，模型色仍为蓝 `#2a78d6` 与橙 `#eb6834`。

| 文件 | 内容 | 数据来源 | 正文位置 |
|---|---|---|---|
| `repair_success.png` | 分支子集五条件修复成功率，两模型 | `RECORD/analysis/main_results.csv` | 第 4 节 |
| `first_round.png` | 第一轮通过题数按难度分层，两模型 | `RECORD/tables/episode_level.csv` | 演示第 7 页 |
| `pass_rate.png` | 全样本五条件通过率，两模型 | `RECORD/analysis/main_results.csv` | 演示第 8 页 |
| `coding_distribution.png` | 九项质性编码的取值分布，共三十一条 | `RECORD/analysis/deepening/coding_summary.csv` | 第 10.2 节 |
| `power_required_units.png` | 达到百分之八十功效所需的配对单位数 | `RECORD/analysis/deepening/power_analysis_required.csv` | 第 13.3 节 |
| `difficulty_split.png` | 标准题与困难题分面的条件通过率 | `RECORD/analysis/deepening/sensitivity.csv` | 第 14 节 |

第 4 节的 EditSize 图仍引用 `RECORD/analysis/figures/edit_size.png`，本次未重绘。

重新生成。

```bash
python harness/make_figures_v1.py
```

脚本只读取现有分析表，不重算任何数字。
