# 深入研究材料

本目录存放路线 A 的质性编码材料与后续机制分析结果。编码规则见 `PLAN/05a_coding_manual.md`。

## 文件

| 文件或目录 | 内容 |
|---|---|
| `blinded/S01` 至 `blinded/S31` | 盲化 episode，含事件流、diff、最终文本与脱敏 summary |
| `coding_sheet.csv` | 三十一条质性编码表，含证据与备注 |
| `blinding_manifest.csv` | 匿名编号与模型、任务、条件的对应关系 |
| `coding_memo.md` | 编码过程、定义执行、分布、观察与限制 |
| `casebook.md` | 六条可追溯案例 |
| `process_metrics.csv` | 148 个 episode 的过程指标，由事件流重算 |
| `budget_accounting.md` | 预算口径补充核算，说明被拒调用与有效预算 |
| `process_metrics.md` | 过程指标描述与条件间对比 |
| `coding_consistency_check.md` | 同日十条一致性检查，不作为信度证据 |
| `coding_machine_check.csv` | 三项可机械化编码的逐项判定，93 行 |
| `coding_machine_check.md` | 机械化判定核查，性质为一致性核查 |
| `coding_reliability.md` | 间隔二十四小时后的正式重编码，后续生成 |
| `coding_second_coder.csv` | 第二编码者原始编码表，十行，未改动 |
| `coding_second_coder_notes.md` | 第二编码者过程说明，原文 |
| `coding_interrater.csv` | 编码者间逐项一致率与分歧条目 |
| `coding_interrater.md` | 编码者间一致率结果与解释边界 |
| `budget_rerun.csv` | 十六个案例两臂结果的配对汇总 |
| `budget_rerun.md` | 双倍预算补跑结果与解释边界 |
| `power_analysis.md` | 功效分析，后续生成 |

## 盲化规则

1. `blinded/` 中不含模型名、条件名、任务名、用户名与本机绝对路径。
2. 不向编码者提供 `prompt.txt`，避免反馈措辞直接暴露分组。
3. 编码完成前不要打开 `blinding_manifest.csv`。
4. 编码完成后按 `sample_id` 回查分组，再做条件汇总。

## 生成

```bash
python harness/prepare_qualitative.py
```

脚本按种子 20261022 打乱三十一条样本，编号固定。若编码表已有内容，脚本默认拒绝覆盖，确需重建时加 `--force`。

## 状态

首轮三十一条编码已完成，编码表、编码记录与案例集均已写入。S01 与 S02 在编码前误见分组映射，已在编码记录中说明。

一致性证据分三份，性质不同，不得混用。

1. `coding_machine_check.md`，三项可机械化编码与源数据的一致性核查，不提供信度信息。
2. `coding_interrater.md`，第二编码者对十例的独立判断，编码者间一致率 0.989，kappa 0.981。第二编码者为语言模型，且与首轮编码者同源。
3. `coding_reliability.md`，编码者内在间隔二十四小时后的重编码，2026-10-23 生成。

编码表需经用户复核后才能进入报告。S01 的 `rewrites_function` 存在一项分歧，见 `coding_interrater.md` 第 5 节，待用户决定取值。
