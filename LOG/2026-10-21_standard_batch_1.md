# 2026-10-21 标准题批次一构造记录

## 范围

本批次构造 T04、T06、T07、T08 四道标准题。构造完成后标准题达到 8 道，困难题仍为 4 道。

| 题号 | 名称 | 类别 | 源码规模 | buggy | gold |
|---|---|---|---|---:|---|---|
| T04 | `next_permutation` | 函数逻辑 | 4 文件 101 行 | 2 failed, 12 passed | 14 passed |
| T06 | `version_scan` | 正则 | 4 文件 142 行 | 2 failed, 13 passed | 15 passed |
| T07 | `group_counts` | 数据处理 | 4 文件 106 行 | 2 failed, 12 passed | 14 passed |
| T08 | `inventory_summary` | 数据处理 | 4 文件 140 行 | 2 failed, 13 passed | 15 passed |

## T04 next_permutation

来源为 QuixBugs `next_permutation`，MIT 许可，commit 4257f44b。函数包装为 `seqkit` 包，增加序列比较、逆序计数、后缀反转与格式化模块，重写测试，并替换原始缺陷。

缺陷位于 `src/seqkit/permute.py`。反转后缀时从枢轴本身开始，正确做法是从枢轴的后继开始。以 1 2 3 为例，交换后得到 1 3 2，再从枢轴反转会把后缀复原为 2 3，最终返回原序列。gold patch 把切片起点由 `pivot` 改为 `pivot + 1`，涉及两行。

目标测试覆盖单步排列与连续三步排列。回归测试覆盖排序判断、序列比较、逆序计数、末排列返回空、输入不变、后缀反转、格式化与异常校验。回归测试避开带上升枢轴的多元素序列，因此在 buggy 状态全部通过。

G10 检查使用 `values[pivot + 1:][::-1]` 作为等价修复，通过；错误修复保留原始切片起点，失败。

## T06 version_scan

原创正则题。包 `textscan` 包含版本识别、位置定位、精确匹配、版本替换、文本规范化与版本汇总。

缺陷位于 `src/textscan/patterns.py`。版本正则缺少尾部边界，四段数字 `1.2.3.4` 中的前三段会被识别为版本。gold patch 在模式末尾增加 `(?![\w.-])`，涉及两行。

目标测试覆盖四段数字的拒绝与混合文本中只保留完整版本。回归测试覆盖正常版本提取、精确匹配、替换、空白规范化、行与空行处理、标点剥离、主版本统计、分组、汇总、格式化、位置定位与预发布后缀。回归测试不使用带数字后缀的输入，因此在 buggy 状态全部通过。

G10 检查使用显式字符类 `(?![0-9A-Za-z_.-])` 作为等价修复，通过；错误修复删除尾部边界，失败。

## T07 group_counts

原创数据处理题。包 `recordkit` 包含字段拆分、表头解析、行解析、分组计数、频次排序与文本渲染。

缺陷位于 `src/recordkit/aggregate.py`。分组键只去除首尾空白，没有折叠大小写，同一城市的 Beijing 与 beijing 被分成两组。gold patch 在 `strip` 后增加 `lower`，涉及两行。

目标测试覆盖大小写与空白混合的三条记录合并为一组。回归测试覆盖字段拆分、表头解析、行解析、缺失字段补空、空文本、非字符串键、空输入与缺失键、频次排序、非法上限、计数与表格渲染。回归测试使用大小写一致的值，因此在 buggy 状态全部通过。

G10 检查使用 `casefold` 作为等价修复，通过；错误修复完全不去除空白与大小写，失败。

## T08 inventory_summary

原创数据处理题。包 `inventory` 包含条目规范化、增删、总量统计、分类计数、低库存判断与格式化。

缺陷位于 `src/inventory/summary.py`。总量统计把缺失数量的条目按零计算，而规范化函数与其他路径均按一件处理。gold patch 把默认值由零改为一，涉及两行。

目标测试覆盖缺失数量条目的总量与汇总。回归测试覆盖默认值与显式值规范化、非法输入、增删、显式数量总量、分类计数、低库存阈值包含边界、格式化与汇总分类字段。回归测试或提供显式数量，或只断言其他字段，因此在 buggy 状态全部通过。

G10 检查使用显式 `None` 判断作为等价修复，通过；错误修复把默认值改为二，失败。

## 验证

四题均通过以下检查。

```text
python harness/validate_tasks.py --repeat 5 tasks/T04_next_permutation
python harness/validate_tasks.py --repeat 5 tasks/T06_version_scan
python harness/validate_tasks.py --repeat 5 tasks/T07_group_counts
python harness/validate_tasks.py --repeat 5 tasks/T08_inventory_summary
python harness/check_variants.py T04_next_permutation
python harness/check_variants.py T06_version_scan
python harness/check_variants.py T07_group_counts
python harness/check_variants.py T08_inventory_summary
```

五轮 buggy 状态计数完全一致，gold patch 只修改允许文件，测试目录哈希在补丁前后不变。

## 备注

- T07 初版源码为 95 行，低于标准题 100 行下限。增加表头解析函数与对应回归测试后达到 106 行。
- T04 的来源为公开基准，存在训练数据污染风险，已在 ATTRIBUTION 中注明来源、commit 与修改说明。
- 四题均尚未进行 V4-Pro 盲解与人工复核。
- 未执行 git commit。
