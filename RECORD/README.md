# RECORD 目录

本目录存放实验取得的结果。建议按以下子目录组织。

| 子目录 | 内容 |
|---|---|
| runs/ | OpenCode 逐次运行的原始事件、提示词、补丁与测试输出 |
| pilot/ | 模型筛选阶段的小规模试运行记录 |
| smoke/ | harness 端到端流程验证记录 |
| calibration/ | pilot 盲解事件、补丁、汇总与人工复核表 |
| tables/ | 主实验逐题指标、条件聚合表与统计检验所需数据 |
| analysis/ | 统计检验与图表数据 |
| report/ | 最终报告与演示文稿 |

runs 目录体积较大，已由 .gitignore 排除。tables、analysis 与 report 已纳入版本管理。
