# 2026-10-21 困难题批次构造记录

## 范围

本批次构造 T13、T15、T17、T18、T19、T22、T23、T24 八道困难题。构造完成后标准题 12 道与困难题 12 道齐备，任务集累计 24 题。

| 题号 | 名称 | 类别 | 源码规模 | buggy | gold |
|---|---|---|---|---:|---|---|
| T13 | `paginate` | 边界条件 | 7 文件 270 行 | 2 failed, 17 passed | 19 passed |
| T15 | `slugify` | 正则 | 7 文件 295 行 | 2 failed, 13 passed | 15 passed |
| T17 | `merge_records` | 数据处理 | 6 文件 279 行 | 2 failed, 13 passed | 15 passed |
| T18 | `parse_bool` | 类型转换 | 7 文件 276 行 | 2 failed, 12 passed | 14 passed |
| T19 | `to_decimal` | 类型转换 | 7 文件 280 行 | 2 failed, 8 passed | 10 passed |
| T22 | `json_dumps` | API 误用 | 6 文件 263 行 | 2 failed, 9 passed | 11 passed |
| T23 | `parse_flags` | API 误用 | 7 文件 260 行 | 2 failed, 12 passed | 14 passed |
| T24 | `join_path` | API 误用 | 7 文件 306 行 | 2 failed, 9 passed | 11 passed |

八题均为原创多模块包，缺陷位于共享 helper 或多条调用链的汇合处，修复需要沿调用关系定位，而不是只读单个函数。

## T13 paginate

包 `pagekit` 包含区间限制、分页、窗口切片、分块、页面状态与文本渲染。缺陷位于共享区间限制函数，上界多加一。请求超出末页时，分页返回空列表，窗口切片只返回最后一个元素，两个调用方同时受影响。目标测试分别覆盖两条调用链。回归测试覆盖正常页码、页数、分块、页码定位、进度条、页面状态与渲染。

## T15 slugify

包 `slugkit` 包含空白归一化、重音折叠、标识生成、标题大小写、分词与报告。缺陷位于标识正则，逐字符替换非字母数字，连续分隔符保留为多个连字符。标识生成与索引渲染两条调用链同时受影响。回归测试重点验证共享空白函数与标题归一化未被改动。

## T17 merge_records

包 `mergekit` 包含字段补全、按标识合并、排序、冲突检测与报告。缺陷位于合并循环，只写入第一次出现的记录，不比较版本。合并与版本摘要两条调用链同时受影响。回归测试使用唯一标识或相同版本，确保顺序与字段补全不受影响。

## T18 parse_bool

包 `confkit` 包含布尔解析、默认配置、命令行解析、键校验、环境变量与报告。缺陷位于布尔解析，任意非空文本都成为真值，false 与 no 等关闭取值失效。配置加载与命令行选项两条调用链同时受影响。回归测试使用真值文本或非文本取值。

## T19 to_decimal

包 `moneykit` 包含金额转换、舍入、汇总、百分比、货币与格式化。缺陷位于浮点转换分支，使用二进制浮点近似值，半分金额在四舍五入时向下偏移。舍入与格式化两条调用链同时受影响。回归测试使用文本或整数金额，在 buggy 状态下走正确分支。

## T22 json_dumps

包 `payloadkit` 包含 JSON 转换、信封、文本处理、规范化与描述。缺陷位于序列化选项组合，非 ASCII 被转义、键未排序、分隔符带空格。直接序列化与信封构造两条调用链同时受影响。回归测试验证往返解析而非精确文本，因此在 buggy 状态全部通过。

## T23 parse_flags

包 `clikit` 包含开关解析、命令行构造、参数辅助、校验、命令与报告。缺陷位于解析器把文本开关交给内置类型转换，false 仍为真值。解析与命令执行两条调用链同时受影响。正确转换函数已存在于 flags 模块但未被解析器使用。回归测试使用真值或省略开关。

## T24 join_path

包 `pathmont` 包含路径归一化、拼接、根目录约束、扩展名、片段校验与报告。缺陷位于拼接函数，以斜杠开头的片段丢弃前面的根目录。直接拼接与根目录解析两条调用链同时受影响。回归测试只使用相对片段。

## 验证

八题均通过以下检查。

```text
python harness/validate_tasks.py --repeat 5 tasks/T13_paginate
python harness/validate_tasks.py --repeat 5 tasks/T15_slugify
python harness/validate_tasks.py --repeat 5 tasks/T17_merge_records
python harness/validate_tasks.py --repeat 5 tasks/T18_parse_bool
python harness/validate_tasks.py --repeat 5 tasks/T19_to_decimal
python harness/validate_tasks.py --repeat 5 tasks/T22_json_dumps
python harness/validate_tasks.py --repeat 5 tasks/T23_parse_flags
python harness/validate_tasks.py --repeat 5 tasks/T24_join_path
python harness/check_variants.py T13_paginate T15_slugify T17_merge_records T18_parse_bool T19_to_decimal T22_json_dumps T23_parse_flags T24_join_path
```

五轮 buggy 状态计数完全一致，gold patch 只修改允许文件，测试目录哈希在补丁前后不变。G10 检查中，T23 的等价修复需要同时增加导入语句与修改解析器参数，因此该题在 `harness/check_variants.py` 中使用多文件编辑形式记录两处改动。

2026-10-21 对全部 24 题执行 `python harness/validate_tasks.py --repeat 1`，全部通过。

## 备注

- T19 的回归测试只有 8 个，处于 6 至 14 个的取值范围下限附近，但每条测试包含多个断言，覆盖转换、舍入、汇总、百分比、货币与格式化六类行为。
- 八题均尚未进行 V4-Pro 盲解与人工复核。
- 未执行 git commit。
