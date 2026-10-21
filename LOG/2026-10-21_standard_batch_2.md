# 2026-10-21 标准题批次二构造记录

## 范围

本批次构造 T09、T10、T11、T12 四道标准题。构造完成后标准题达到 12 道，困难题仍为 4 道，任务集累计 16 题。

| 题号 | 名称 | 类别 | 源码规模 | buggy | gold |
|---|---|---|---|---:|---|---|
| T09 | `safe_int` | 类型转换 | 4 文件 129 行 | 2 failed, 12 passed | 14 passed |
| T10 | `top_k` | 排序查找 | 4 文件 102 行 | 2 failed, 12 passed | 14 passed |
| T11 | `sort_items` | API 误用 | 4 文件 115 行 | 2 failed, 11 passed | 13 passed |
| T12 | `format_datetime` | API 误用 | 4 文件 153 行 | 2 failed, 10 passed | 12 passed |

## T09 safe_int

原创类型转换题。包 `convertkit` 包含文本与对象转数字、整值校验、区间截断、正数兜底与数值格式化。

缺陷位于 `src/convertkit/parse.py`。转换对象分支只捕获 `ValueError`，缺失值触发 `TypeError` 并使批量转换整批中断。目标测试断言缺失值返回调用方给定的默认值，以及批量转换把缺失条目替换为零。gold patch 把异常类型扩展为 `TypeError` 与 `ValueError`，涉及一行。

与其余题目不同，本题目标测试在 buggy 状态以异常而非断言失败结束，`target_failure_mode` 记为 `error`。评分的 JUnit 解析把异常与断言失败都视为未通过，不影响指标计算。

回归测试覆盖带空白的文本、正负号、不可转换文本、空文本、浮点截断、浮点解析、非法序列、整值判断、必需值校验、区间截断、正数兜底与格式化，均不向转换函数传入缺失值。

G10 检查使用异常元组交换顺序作为等价修复，通过；错误修复虽捕获异常但忽略调用方默认值，失败。

## T10 top_k

原创排序查找题。包 `rankkit` 包含降序副本、前若干名选取、均值中位数极差与名次计算、榜单与表格渲染。

缺陷位于 `src/rankkit/topk.py`。切片上界多加一，返回值总比请求条数多一条。目标测试覆盖纯数值取前两名与带并列分数的稳定取前两名。gold patch 把上界改为 `limit`，涉及一行。

回归测试覆盖降序副本不改写输入、非序列校验、空列表取零条、取满全部、非法上限、均值、中位数、极差、名次、榜单、表格与摘要。回归测试只使用空输入或取满全长的情形，因而不受上界错误影响。

G10 检查使用等价的切片写法作为修复，通过；错误修复把上界再加一，失败。

## T11 sort_items

原创 API 误用题。包 `listkit` 包含值排序、按键排序、去重、分组、展平、分块、轮转与文本渲染。

缺陷位于 `src/listkit/ordering.py`。排序函数返回就地方法的返回值空值，同时改写调用方传入的列表。目标测试覆盖返回值内容与输入列表保持不变。gold patch 改为返回排序后的新列表，涉及一行。

回归测试覆盖类型校验、按键排序及其异常、去重、分组、展平、分块、轮转、逐项渲染、记录渲染与排序渲染。回归测试不调用受影响的排序函数，仅验证其类型守卫。

G10 检查使用返回新列表的等价写法，通过；错误修复先就地排序再返回原列表，仍然改写输入，失败。

## T12 format_datetime

原创 API 误用题。包 `timekit` 包含日期时间格式化、日期时间解析与日期间隔计算。

缺陷位于 `src/timekit/format.py`。日期格式在月份位置使用分钟指令，只有七月的分钟数与月份恰好相同才输出正确结果。目标测试覆盖三月日期与带分钟数的完整时间戳。gold patch 把指令改为月份，涉及一行。

回归测试覆盖时间格式化、紧凑日期、日期解析、时间解析、可选解析、批量解析、日间隔、周末判断、下一工作日与月份长度。回归测试不调用日期与时间戳格式化函数。

G10 检查使用正确的月份指令作为等价修复，通过；错误修复互换月份与日期指令，失败。

## 验证

四题均通过以下检查。

```text
python harness/validate_tasks.py --repeat 5 tasks/T09_safe_int
python harness/validate_tasks.py --repeat 5 tasks/T10_top_k
python harness/validate_tasks.py --repeat 5 tasks/T11_sort_items
python harness/validate_tasks.py --repeat 5 tasks/T12_format_datetime
python harness/check_variants.py T09_safe_int T10_top_k T11_sort_items T12_format_datetime
```

五轮 buggy 状态计数完全一致，gold patch 只修改允许文件，测试目录哈希在补丁前后不变。

## 备注

- T09 是任务集中唯一以异常作为目标失败方式的题目，分析时需单独说明。
- 四题均尚未进行 V4-Pro 盲解与人工复核。
- 未执行 git commit。
