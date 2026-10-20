# 2026-10-20 来源下载与候选池

## 目标

建立 24 题任务的候选池，验证 QuixBugs、BigCodeBench、HumanEval 三个来源的可用性，并检查许可、依赖、测试质量和污染风险。

## 操作

1. 克隆 QuixBugs 到 `tasks/_sources/QuixBugs`。
   - commit `4257f44b0ff1181dedaedee6a447e133219fcebf`
   - 许可 MIT
   - Python 题目 40 道，另有 `node.py` 辅助文件

2. 从 HuggingFace 镜像下载 BigCodeBench v0.1.4 parquet 到 `tasks/_sources/bigcodebench/`。
   - 文件 `bigcodebench-v0.1.4.parquet`
   - 1140 题
   - 许可 Apache-2.0

3. 下载 HumanEval 到 `tasks/_sources/humaneval/`。
   - 164 题
   - 许可 MIT
   - 仅用于冒烟测试，不进入主候选池

4. 编写 `harness/inventory_sources.py`，静态读取来源并生成候选池。
   - 不执行下载代码
   - 解析 BigCodeBench 的 libs、测试导入、断言数、测试方法数
   - 输出 `PLAN/03_candidate_pool.json` 与 `PLAN/03_candidate_pool.md`

## 结果

候选池共 53 题。

| 来源 | 数量 | 说明 |
|---|---:|---|
| QuixBugs | 22 | 均有 buggy 与 fixed 版本，JSON 用例数不少于 5 |
| BigCodeBench | 31 | 标准库依赖为主，覆盖正则、数据、类型、排序、API |
| 合计 | 53 | 满足 40 到 60 题的候选池目标 |

## 关键发现

1. BigCodeBench 的 `libs` 字段只描述解法依赖，不包含测试依赖。例如 `BigCodeBench/464` 的解法只用标准库，但测试导入 `pytz`；`BigCodeBench/270` 的测试导入 `faker`；`BigCodeBench/778` 的测试导入 `faker`；`BigCodeBench/201` 的测试导入 `pandas`，而 `libs` 只写 `statistics,bisect`。因此不能只按 `libs` 过滤，必须解析测试导入。

2. BigCodeBench 的部分测试断言较弱，例如只检查返回类型或只检查非空。候选池标出断言数和测试方法数，入库前仍需重写目标测试与回归测试。

3. BigCodeBench 全量 1140 题中，`libs` 全部属于标准库的有 324 题。加上测试导入、文件系统、随机性、断言数等过滤后，得到 31 题的精选候选。这个数量足够支撑 12 道标准题和部分困难题改造。

4. QuixBugs 的 40 道题中，31 道有 JSON 测试数据，其余使用内嵌测试文件。按用例数不少于 5 筛选后保留 22 道。QuixBugs 缺少正则、类型转换和 API 误用，需要 BigCodeBench 和原创任务补足。

5. HumanEval 题目饱和且污染严重，单函数结构无法提供回归面，不进入主候选池。

## 下一步

1. 从 53 题中选出 24 题，保持 12 标准加 12 困难、七类错误覆盖。
2. 先改造四道 pilot 题：T01 边界条件、T05 正则、T16 数据处理、T21 排序查找。
3. 对 pilot 题执行 G1 到 G12 自动验证、V4-Pro 盲解和人工复核。

## 复现命令

```bash
python -I harness/inventory_sources.py
```

输出文件：

- `PLAN/03_candidate_pool.json`
- `PLAN/03_candidate_pool.md`
