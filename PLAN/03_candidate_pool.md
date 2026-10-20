# 24 题候选池

> 生成时间：2026-10-20
> 来源快照与许可见 `tasks/_sources/`，候选池只记录元数据，不复制源码。

## 概览

- 候选总数：53
- QuixBugs：22
- BigCodeBench：31
- HumanEval：不进入主候选池，仅用于 harness 冒烟测试。

## QuixBugs 候选

| 编号 | 类别 | 适配难度 | 行数 | 用例数 | buggy | fixed | 备注 |
|---|---|---|---:|---:|---|---|---|
| QB-find_first_in_sorted | 边界条件/排序查找 | 标准 | 35 | 7 | True | True | 二分查找重复元素，适合拆分目标与回归用例 |
| QB-find_in_sorted | 边界条件/排序查找 | 标准 | 31 | 7 | True | True | 二分查找边界，适合半开区间错误 |
| QB-gcd | 函数逻辑 | 标准 | 26 | 6 | True | True | 递归与取模，适合一行逻辑错误 |
| QB-next_palindrome | 函数逻辑 | 标准 | 33 | 5 | True | True | 进位与回文边界，适合边界逻辑 |
| QB-possible_change | 函数逻辑/数据处理 | 标准 | 33 | 10 | True | True | 动态规划零钱问题，测试用例较多 |
| QB-hanoi | 函数逻辑 | 标准 | 35 | 8 | True | True | 递归移动序列，适合步骤与边界 |
| QB-quicksort | 排序查找 | 标准 | 19 | 13 | True | True | 分区与递归，测试用例最多 |
| QB-kth | 排序查找 | 标准 | 32 | 7 | True | True | 选择第 k 小，适合边界与重复值 |
| QB-mergesort | 排序查找 | 标准 | 36 | 14 | True | True | 归并与稳定性，适合回归测试 |
| QB-bucketsort | 排序查找 | 标准 | 27 | 7 | True | True | 桶排序边界与空桶 |
| QB-to_base | 类型转换 | 标准 | 32 | 10 | True | True | 整数转任意进制，适合字符映射 |
| QB-sqrt | 类型转换 | 标准 | 27 | 7 | True | True | 整数平方根与精度边界 |
| QB-rpn_eval | 数据处理 | 标准 | 43 | 6 | True | True | 逆波兰表达式求值，适合栈与错误处理 |
| QB-shunting_yard | 数据处理 | 标准 | 48 | 6 | True | True | 中缀转后缀，适合运算符优先级 |
| QB-flatten | 数据处理 | 标准 | 29 | 7 | True | True | 嵌套列表展平，适合递归与类型判断 |
| QB-wrap | 数据处理 | 标准 | 28 | 5 | True | True | 文本换行，适合边界与空白 |
| QB-max_sublist_sum | 函数逻辑 | 标准 | 31 | 6 | True | True | 最大子数组和，适合负数与空输入 |
| QB-lis | 函数逻辑 | 标准 | 37 | 12 | True | True | 最长递增子序列，适合边界与重复值 |
| QB-levenshtein | 函数逻辑 | 标准 | 32 | 7 | True | True | 编辑距离，适合动态规划边界 |
| QB-knapsack | 函数逻辑 | 标准 | 37 | 10 | True | True | 背包问题，适合容量与物品边界 |
| QB-bitcount | 函数逻辑 | 标准 | 26 | 9 | True | True | 位计数，适合负数与零边界 |
| QB-get_factors | 函数逻辑 | 标准 | 35 | 11 | True | True | 因子分解，适合完全平方与素数 |

## BigCodeBench 候选

| 编号 | 类别 | 适配难度 | 依赖 | 解法行数 | 断言数 | 测试方法数 | 测试第三方依赖 | 备注 |
|---|---|---|---|---:|---:|---:|---|---|
| BCB-25 | 数据处理/API 参数误用 | 标准 | zlib, base64, json | 3 | 10 | 5 | 无 | JSON 序列化、zlib 压缩、base64 编码链 |
| BCB-178 | 数据处理/正则 | 标准 | re, json | 11 | 5 | 5 | 无 | 从 JSON 响应中提取 IP，正则与 JSON 组合 |
| BCB-202 | 数据处理/正则 | 标准 | collections, re, json | 18 | 6 | 5 | 无 | 从 JSON 字符串中提取 URL，适合数据清洗 |
| BCB-254 | 类型转换 | 标准 | math, json | 7 | 5 | 5 | 无 | 小数平方根与 JSON 编码，适合精度与类型 |
| BCB-270 | 正则/数据处理 | 标准 | collections, re | 4 | 6 | 6 | faker | 词频统计，测试依赖 faker，需重写 |
| BCB-433 | API 参数误用 | 标准 | base64, hashlib, hmac, binascii | 3 | 8 | 8 | 无 | HMAC 签名校验，API 参数与编码组合 |
| BCB-464 | 类型转换/API 参数误用 | 标准 | decimal, datetime, json | 8 | 10 | 7 | pytz | JSON 编码 Decimal 与 datetime，测试依赖 pytz，需重写 |
| BCB-466 | API 参数误用 | 标准 | enum, json | 6 | 8 | 7 | 无 | JSON 编码 Enum，适合自定义 encoder |
| BCB-667 | 排序查找 | 标准 | collections, heapq | 4 | 5 | 5 | 无 | heapq 取前 n 个高频字母 |
| BCB-682 | 数据处理 | 标准 | math, collections | 7 | 5 | 5 | 无 | 嵌套字典聚合与 Counter |
| BCB-709 | 正则/数据处理 | 标准 | html, base64, re, textwrap | 14 | 5 | 5 | 无 | base64、HTML 实体、空白归一化 |
| BCB-733 | 正则/函数逻辑 | 标准 | string, re | 23 | 8 | 8 | 无 | 停用词计数，正则分词 |
| BCB-741 | 数据处理 | 标准 | operator, itertools | 5 | 5 | 5 | 无 | 按首字符分组求和，groupby |
| BCB-747 | 正则/类型转换 | 标准 | math, re | 4 | 10 | 5 | 无 | 提取数字并求平方根和 |
| BCB-761 | 数据处理/正则 | 标准 | collections, re, json | 15 | 5 | 5 | 无 | JSON 清洗、邮箱替换、值频次 |
| BCB-766 | 正则 | 标准 | collections, re | 18 | 11 | 7 | 无 | 多模式计数，适合正则边界 |
| BCB-769 | 数据处理/排序查找 | 标准 | operator, collections, itertools | 5 | 5 | 5 | 无 | 嵌套列表展平与众数 |
| BCB-775 | 正则/数据处理 | 标准 | collections, string, re | 16 | 5 | 5 | 无 | 按最后一个连字符切分并统计字母 |
| BCB-851 | 正则/数据处理 | 标准 | re, textwrap | 10 | 5 | 5 | 无 | textwrap 与整词替换 |
| BCB-867 | 正则 | 标准 | string, re | 11 | 6 | 6 | 无 | 删除 ASCII 标点 |
| BCB-893 | API 参数误用/数据处理 | 标准 | datetime, re | 20 | 6 | 6 | 无 | 日志时间解析与平均，datetime 组合 |
| BCB-911 | 数据处理 | 标准 | operator, string, functools | 10 | 5 | 5 | 无 | 字母映射与 reduce 乘积 |
| BCB-928 | 数据处理/排序查找 | 困难候选 | collections, itertools, string | 12 | 22 | 5 | 无 | 生成全部双字母组合并统计，规模较大 |
| BCB-931 | 正则/数据处理 | 标准 | collections, re | 9 | 7 | 7 | 无 | 清洗后统计相邻字母对 |
| BCB-932 | 正则/排序查找 | 标准 | collections, re | 12 | 7 | 7 | 无 | 最频繁双字母组合 |
| BCB-937 | 正则/数据处理 | 标准 | collections, re | 3 | 7 | 7 | 无 | 字母数字频次统计 |
| BCB-957 | 正则/数据处理 | 标准 | string, re | 4 | 9 | 9 | 无 | 词数、字符数、唯一字符数 |
| BCB-972 | API 参数误用 | 困难候选 | pathlib, os | 19 | 8 | 7 | 无 | 路径分隔与非法字符校验，适合改造为路径拼接任务 |
| BCB-1090 | 数据处理/API 参数误用 | 困难候选 | ast, collections, json | 15 | 8 | 8 | 无 | JSON 文件指针、ast 解析与键频次 |
| BCB-1098 | 正则/排序查找 | 标准 | collections, re | 10 | 5 | 5 | 无 | 去除 URL 后取 top N 词 |
| BCB-1126 | 正则/API 参数误用 | 标准 | hashlib, re | 4 | 9 | 9 | 无 | 清洗后 SHA256，适合正则与 API 组合 |

## 使用规则

1. 候选池不是最终题目集。最终 24 题按 12 标准加 12 困难选择，并保持七类错误覆盖。
2. BigCodeBench 的原始测试只作为参考。入库前必须重写目标测试与回归测试，去掉第三方依赖和弱断言。
3. QuixBugs 的 JSON 用例可以拆为目标用例与回归用例，但必须补充相邻模块或共享 helper 的回归测试。
4. 困难题通过多文件包装实现，不直接按原题难度认定。共享 helper、多个调用方和回归陷阱是困难题的必要条件。
5. 所有题目必须通过 G1 到 G12、V4-Pro 盲解和人工复核后才可冻结。

## 已知限制

- BigCodeBench 的 `libs` 字段不包含测试依赖。本脚本额外解析测试导入，但仍需人工检查。
- 部分 BigCodeBench 测试使用 `faker`、`pytz` 或文件系统。候选池标出这些风险，入库前必须改写。
- QuixBugs 与 BigCodeBench 都是公开基准，存在训练数据污染。最终题目需要改写标识符、常量和调用链。
- 本脚本不执行下载代码，只做静态读取。
