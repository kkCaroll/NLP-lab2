# 主实验统计分析

配对分析仅使用第一轮失败任务的分支子集。全样本表包含第一轮通过任务在五条件中复用的终态。

## 分支子集描述统计

| 模型 | 条件 | n | PassRate | RepairSuccess | RegressionRate | EditSize 中位数 | EditRatio 中位数 | OverEditRate | 无编辑失败率 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MiMo | pure_continue | 6 | 1.000 | 1.000 | 0.000 | 4.000 | 1.000 | 0.000 | NA |
| MiMo | neutral | 6 | 0.833 | 0.833 | 0.000 | 3.500 | 0.800 | 0.000 | NA |
| MiMo | method_guidance | 6 | 1.000 | 1.000 | 0.000 | 4.000 | 1.000 | 0.000 | NA |
| MiMo | negative | 6 | 0.833 | 0.833 | 0.000 | 3.000 | 1.000 | 0.167 | NA |
| MiMo | negative_guidance | 6 | 1.000 | 1.000 | 0.000 | 3.500 | 1.000 | 0.000 | NA |
| MiniMax | pure_continue | 14 | 0.857 | 0.857 | 0.000 | 2.000 | 1.000 | 0.071 | NA |
| MiniMax | neutral | 14 | 0.643 | 0.643 | 0.000 | 2.000 | 1.000 | 0.071 | NA |
| MiniMax | method_guidance | 14 | 0.786 | 0.786 | 0.000 | 2.000 | 1.000 | 0.000 | NA |
| MiniMax | negative | 14 | 0.643 | 0.643 | 0.000 | 2.000 | 1.000 | 0.071 | NA |
| MiniMax | negative_guidance | 14 | 0.929 | 0.929 | 0.000 | 2.000 | 1.000 | 0.000 | NA |

## 全样本描述统计

| 模型 | 条件 | n | PassRate | RepairSuccess | EditSize 中位数 | EditRatio 中位数 |
|---|---|---:|---:|---:|---:|---:|
| MiMo | pure_continue | 24 | 1.000 | 1.000 | 2.000 | 1.000 |
| MiMo | neutral | 24 | 0.958 | 0.833 | 2.000 | 1.000 |
| MiMo | method_guidance | 24 | 1.000 | 1.000 | 2.000 | 1.000 |
| MiMo | negative | 24 | 0.958 | 0.833 | 2.000 | 1.000 |
| MiMo | negative_guidance | 24 | 1.000 | 1.000 | 2.000 | 1.000 |
| MiniMax | pure_continue | 24 | 0.917 | 0.857 | 2.000 | 1.000 |
| MiniMax | neutral | 24 | 0.792 | 0.643 | 2.000 | 1.000 |
| MiniMax | method_guidance | 24 | 0.875 | 0.786 | 2.000 | 1.000 |
| MiniMax | negative | 24 | 0.792 | 0.643 | 2.000 | 1.000 |
| MiniMax | negative_guidance | 24 | 0.958 | 0.929 | 2.000 | 1.000 |

## 配对检验

### MiMo

all_passed 整体检验 cochran_q 统计量 3.000 p 0.5578，完整任务 6。

| 条件 A | 条件 B | 效应量 | 95% CI | p | Holm p |
|---|---|---|---:|---:|---:|
| pure_continue | neutral | RD 0.167 | NA | 1.0000 | 1.0000 |
| pure_continue | method_guidance | RD 0.000 | NA | 1.0000 | 1.0000 |
| pure_continue | negative | RD 0.167 | NA | 1.0000 | 1.0000 |
| pure_continue | negative_guidance | RD 0.000 | NA | 1.0000 | 1.0000 |
| neutral | method_guidance | RD -0.167 | NA | 1.0000 | 1.0000 |
| neutral | negative | RD 0.000 | NA | 1.0000 | 1.0000 |
| neutral | negative_guidance | RD -0.167 | NA | 1.0000 | 1.0000 |
| method_guidance | negative | RD 0.167 | NA | 1.0000 | 1.0000 |
| method_guidance | negative_guidance | RD 0.000 | NA | 1.0000 | 1.0000 |
| negative | negative_guidance | RD -0.167 | NA | 1.0000 | 1.0000 |

edit_lines 整体检验 friedman 统计量 2.933 p 0.5690，完整任务 6。

| 条件 A | 条件 B | 效应量 | 95% CI | p | Holm p |
|---|---|---|---:|---:|---:|
| pure_continue | neutral | delta 0.139 | [0.000, 0.444] | 0.5000 | 1.0000 |
| pure_continue | method_guidance | delta -0.083 | [-0.417, 0.000] | 1.0000 | 1.0000 |
| pure_continue | negative | delta 0.167 | [-0.389, 0.750] | 0.7500 | 1.0000 |
| pure_continue | negative_guidance | delta 0.083 | [0.000, 0.333] | 1.0000 | 1.0000 |
| neutral | method_guidance | delta -0.194 | [-0.583, 0.000] | 0.5000 | 1.0000 |
| neutral | negative | delta 0.028 | [-0.556, 0.694] | 1.0000 | 1.0000 |
| neutral | negative_guidance | delta -0.056 | [-0.333, 0.000] | 1.0000 | 1.0000 |
| method_guidance | negative | delta 0.222 | [-0.389, 0.806] | 0.5000 | 1.0000 |
| method_guidance | negative_guidance | delta 0.139 | [0.000, 0.583] | 1.0000 | 1.0000 |
| negative | negative_guidance | delta -0.139 | [-0.694, 0.417] | 0.7500 | 1.0000 |

edit_ratio 整体检验 friedman 统计量 2.933 p 0.5690，完整任务 6。

| 条件 A | 条件 B | 效应量 | 95% CI | p | Holm p |
|---|---|---|---:|---:|---:|
| pure_continue | neutral | delta 0.250 | [0.000, 0.694] | 0.5000 | 1.0000 |
| pure_continue | method_guidance | delta -0.139 | [-0.500, 0.000] | 1.0000 | 1.0000 |
| pure_continue | negative | delta 0.000 | [-0.389, 0.444] | 1.0000 | 1.0000 |
| pure_continue | negative_guidance | delta 0.028 | [0.000, 0.250] | 1.0000 | 1.0000 |
| neutral | method_guidance | delta -0.333 | [-0.722, 0.000] | 0.5000 | 1.0000 |
| neutral | negative | delta -0.167 | [-0.722, 0.444] | 1.0000 | 1.0000 |
| neutral | negative_guidance | delta -0.222 | [-0.667, 0.000] | 1.0000 | 1.0000 |
| method_guidance | negative | delta 0.083 | [-0.389, 0.611] | 1.0000 | 1.0000 |
| method_guidance | negative_guidance | delta 0.139 | [0.000, 0.500] | 1.0000 | 1.0000 |
| negative | negative_guidance | delta 0.000 | [-0.444, 0.389] | 1.0000 | 1.0000 |

### MiniMax

all_passed 整体检验 cochran_q 统计量 7.111 p 0.1301，完整任务 14。

| 条件 A | 条件 B | 效应量 | 95% CI | p | Holm p |
|---|---|---|---:|---:|---:|
| pure_continue | neutral | RD 0.214 | NA | 0.3750 | 1.0000 |
| pure_continue | method_guidance | RD 0.071 | NA | 1.0000 | 1.0000 |
| pure_continue | negative | RD 0.214 | NA | 0.3750 | 1.0000 |
| pure_continue | negative_guidance | RD -0.071 | NA | 1.0000 | 1.0000 |
| neutral | method_guidance | RD -0.143 | NA | 0.6250 | 1.0000 |
| neutral | negative | RD 0.000 | NA | 1.0000 | 1.0000 |
| neutral | negative_guidance | RD -0.286 | NA | 0.1250 | 1.0000 |
| method_guidance | negative | RD 0.143 | NA | 0.5000 | 1.0000 |
| method_guidance | negative_guidance | RD -0.143 | NA | 0.6250 | 1.0000 |
| negative | negative_guidance | RD -0.286 | NA | 0.1250 | 1.0000 |

edit_lines 整体检验 friedman 统计量 3.219 p 0.5219，完整任务 14。

| 条件 A | 条件 B | 效应量 | 95% CI | p | Holm p |
|---|---|---|---:|---:|---:|
| pure_continue | neutral | delta 0.153 | [-0.255, 0.541] | 0.5212 | 1.0000 |
| pure_continue | method_guidance | delta 0.199 | [-0.102, 0.515] | 0.6504 | 1.0000 |
| pure_continue | negative | delta 0.276 | [-0.102, 0.628] | 0.3082 | 1.0000 |
| pure_continue | negative_guidance | delta -0.036 | [-0.367, 0.245] | 0.7218 | 1.0000 |
| neutral | method_guidance | delta 0.025 | [-0.296, 0.352] | 0.6297 | 1.0000 |
| neutral | negative | delta 0.112 | [-0.184, 0.423] | 0.6504 | 1.0000 |
| neutral | negative_guidance | delta -0.194 | [-0.510, 0.107] | 0.3003 | 1.0000 |
| method_guidance | negative | delta 0.102 | [-0.138, 0.367] | 0.4711 | 1.0000 |
| method_guidance | negative_guidance | delta -0.255 | [-0.587, 0.087] | 0.5601 | 1.0000 |
| negative | negative_guidance | delta -0.327 | [-0.663, 0.051] | 0.2711 | 1.0000 |

edit_ratio 整体检验 friedman 统计量 3.219 p 0.5219，完整任务 14。

| 条件 A | 条件 B | 效应量 | 95% CI | p | Holm p |
|---|---|---|---:|---:|---:|
| pure_continue | neutral | delta 0.194 | [-0.122, 0.510] | 0.5004 | 1.0000 |
| pure_continue | method_guidance | delta 0.128 | [-0.199, 0.449] | 0.6504 | 1.0000 |
| pure_continue | negative | delta 0.204 | [-0.133, 0.541] | 0.3555 | 1.0000 |
| pure_continue | negative_guidance | delta 0.092 | [-0.260, 0.434] | 0.6975 | 1.0000 |
| neutral | method_guidance | delta -0.071 | [-0.362, 0.199] | 0.5854 | 1.0000 |
| neutral | negative | delta 0.025 | [-0.214, 0.270] | 0.7461 | 1.0000 |
| neutral | negative_guidance | delta -0.133 | [-0.408, 0.112] | 0.3003 | 1.0000 |
| method_guidance | negative | delta 0.087 | [-0.112, 0.306] | 0.4713 | 1.0000 |
| method_guidance | negative_guidance | delta -0.046 | [-0.357, 0.250] | 0.6502 | 1.0000 |
| negative | negative_guidance | delta -0.138 | [-0.408, 0.102] | 0.3003 | 1.0000 |

## 复跑一致性

同一题同一条件在主运行与随机顺序复跑之间的结果一致性。覆盖仅限两轮均进入分支的 episode。

| 模型 | n | 通过一致率 | Cohen kappa | ICC(2,1) EditSize | Spearman rho | 平均绝对修改差 |
|---|---:|---:|---:|---:|---:|---:|
| MiMo | 10 | 0.900 | 0.000 | 0.166 | 0.401 | 1.700 |
| MiniMax | 25 | 0.680 | 0.324 | -0.178 | 0.011 | 3.920 |

按条件一致率如下。每格样本量为五或更少，仅作描述。

| 模型 | 条件 | n | 通过一致率 | Cohen kappa |
|---|---|---:|---:|---:|
| MiMo | method_guidance | 2 | 1.000 | NA |
| MiMo | negative | 2 | 0.500 | 0.000 |
| MiMo | negative_guidance | 2 | 1.000 | NA |
| MiMo | neutral | 2 | 1.000 | NA |
| MiMo | pure_continue | 2 | 1.000 | NA |
| MiniMax | method_guidance | 5 | 0.800 | 0.545 |
| MiniMax | negative | 5 | 0.600 | 0.286 |
| MiniMax | negative_guidance | 5 | 0.800 | 0.545 |
| MiniMax | neutral | 5 | 0.600 | 0.286 |
| MiniMax | pure_continue | 5 | 0.600 | -0.250 |

## 无测试消融

同一题同一条件在主运行与无测试消融之间的配对差异。
该表仅使用两次运行均进入分支的 episode。MiMo 消融六题第一轮通过，交集仅两题，因此 n 为十，不代表八题全样本。
全样本比较见 `RECORD/analysis/ablation/README.md`。

| 模型 | n | 主运行 PassRate | 消融 PassRate | 主减消融 | 主运行 EditSize 中位数 | 消融 EditSize 中位数 | Cliff delta | 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| MiMo | 10 | 0.900 | 1.000 | -0.100 | 2.000 | 3.000 | -0.190 | [-0.510, 0.000] |
| MiniMax | 40 | 0.725 | 0.825 | -0.100 | 2.000 | 2.000 | -0.178 | [-0.389, 0.045] |

## 图

![分支修复成功率](figures/repair_success.png)

![分支 EditSize 分布](figures/edit_size.png)

## 解释约束

主实验条件顺序固定，条件与任务内位置完全共线，配对检验只能作为探索性描述。
McNemar 检验在 MiniMax 十四对与 MiMo 六对失败任务下功效很低，不显著不能解释为无效应。
回归测试零方差，不进行显著性检验，另见回归敏感性诊断。
