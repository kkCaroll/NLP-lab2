# 回归敏感性诊断执行记录

## 时间

2026-10-21

## 工作内容

1. 新增 `harness/regression_sensitivity.py`，实现覆盖率与变异两类诊断。
2. 覆盖率诊断在临时仓库副本中只运行 `tests/test_regression.py`，按目标文件与非目标文件分别统计 statement coverage。
3. 变异诊断对非目标源文件生成 AST 变异体，变异类型为比较运算符翻转、布尔运算符翻转、四则运算符互换、数值常量加减一。每个变异体单独运行回归测试。
4. 目标测试在缺陷基线上本就失败，未作为变异信号，避免误把基线失败记为目标测试检出。
5. 新增 `harness/analyze.py`，完成主实验描述统计与配对检验的首版。
6. 统计依赖写入 `requirements.txt`，包括 numpy scipy pandas matplotlib coverage。

## 结果

覆盖率诊断覆盖 24 题。总覆盖率 0.916，目标文件 0.908，非目标文件 0.918。最低为 T15 0.837，最高为 T21 1.000。

变异诊断覆盖 T13 T14 T18 T19 T20 T24。共 47 个变异体，回归测试杀死 37 个，变异得分 0.787。逐题得分 T13 0.375，T14 1.000，T18 0.875，T19 0.875，T20 0.625，T24 1.000。

主实验描述统计与配对检验已生成。MiniMax 分支子集 RepairSuccess 为 pure 0.857，neutral 0.643，method_guidance 0.786，negative 0.643，negative_guidance 0.929。MiMo 分支子集 pure 1.000，neutral 0.833，method_guidance 1.000，negative 0.833，negative_guidance 1.000。

## 发现

1. 覆盖率接近上限，但 T13 与 T20 的变异得分偏低，说明部分非目标行为被执行却未被断言约束。
2. 变异得分应表述为敏感性下界，因为部分存活变异体可能语义等价。
3. 主实验条件顺序固定，配对检验只能作为探索性结果，不能解释为因果效应。
4. 主实验数据缺少部分新增派生字段，无编辑失败率显示为 NA，需要从事件日志单独解析。

## 产物

- `RECORD/analysis/regression_sensitivity.md`
- `RECORD/analysis/regression_coverage.csv`
- `RECORD/analysis/regression_mutation.csv`
- `RECORD/analysis/main_results.csv`
- `RECORD/analysis/main_results.md`
- `RECORD/analysis/statistics.json`
