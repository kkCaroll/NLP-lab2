# tasks 目录

本目录存放任务源快照与已构造的代码修复任务。

| 目录 | 内容 |
|---|---|
| _sources/ | QuixBugs、BigCodeBench 与 HumanEval 的来源快照及许可信息 |
| T01_next_palindrome/ | 边界条件标准题，含 buggy 仓库、目标测试、回归测试、gold patch 与元数据 |
| T02_parse_range/ | 边界条件标准题，含闭区间解析、合并、格式化与校验 |
| T03_apply_discount/ | 函数逻辑标准题，含十进制金额、折扣与购物车合计 |
| T05_email_regex/ | 正则标准题，含邮箱识别、归一化、域名统计与替换 |
| T14_shipping_fee/ | 函数逻辑困难题，含共享重量换算与总重量两处缺陷 |
| T16_sales_aggregation/ | 数据处理困难题，含金额转换、退款聚合、筛选、指标与报告 |
| T20_multi_key_sort/ | 排序查找困难题，含共享排序键与部门排序两处缺陷 |
| T21_first_duplicate/ | 排序查找困难题，含重复值定位、计数、位置分析与连续段分析 |

每道新题使用 `T<编号>_<短名>/` 目录，保持相同的目录结构。meta.json 记录类别、难度、来源、许可、目标测试、回归测试与 gold 行数。
