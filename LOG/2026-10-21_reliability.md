# 随机顺序复跑记录

## 设置

run_id 为 `2026-10-21_reliability`，两模型六题，五条件。条件顺序按任务随机化，种子由 run_id、模型与任务名派生。第一轮十次工具调用，第二轮十五次，编辑上限八次，超时三百秒。配置与主实验相同。

## 完整性

十二份 task summary，三十五个分支 episode。审计无缺失、无超时、无分支继承不一致、无提示词公共前缀差异。MiMo T24 negative 修改测试文件，评分前已还原，保留为结果。

## 结果

MiniMax 分支子集第一轮失败五题。pure_continue 修复成功 0.800，neutral 0.800，method_guidance 0.800，negative 0.600，negative_guidance 0.600。主实验对应值为 0.857、0.643、0.786、0.643、0.929。

MiMo 分支子集仅两题。五条件修复成功均为 1.000。

主运行与复跑的分支 episode 通过一致率 MiniMax 0.680，MiMo 0.900。Cohen kappa 分别为 0.324 与 0.000。EditSize 的 ICC(2,1) 分别为 -0.178 与 0.166，Spearman rho 分别为 0.011 与 0.401。

## 发现

1. 主实验 negative_guidance 最高的模式未在随机顺序复跑中重现。复跑中负面条件低于纯继续。
2. MiniMax 的通过一致率与 EditSize 一致性均较低，单次运行的 condition 差异包含较大随机波动。
3. 主实验固定顺序与条件完全共线，复跑结果不支持强因果解释。
4. MiMo 复跑分支仅两题，kappa 因边际分布退化而为零，不能作为稳定性的强证据。

## 产物

- `RECORD/analysis/reliability/`
- `RECORD/analysis/audit_2026-10-21_reliability.json`
- `RECORD/analysis/statistics.json`
