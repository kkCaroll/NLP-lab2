# 回归测试、覆盖率与变异测试

## 回归测试

回归测试用于确认新修改没有破坏原有功能。本实验的每个任务仓库同时包含 `tests/test_target.py` 与 `tests/test_regression.py`。目标测试在缺陷版本上失败，修复后应通过。回归测试在缺陷版本上通过，修复后仍应通过。

回归测试全部通过不等于代码没有回归。若回归测试没有覆盖被修改的行为，错误仍可能漏过。因此需要检查测试本身的检出能力。

## 行覆盖率

覆盖率统计测试执行了源码中的哪些语句。常见指标为 statement coverage 与 branch coverage。覆盖率是必要条件而非充分条件。一条语句被执行，不代表测试断言了它的输出。

本实验用 `coverage` 只运行回归测试，分别统计目标文件与非目标文件的覆盖率。若非目标文件覆盖率很低，零回归更可能来自测试盲区。

## 变异测试

变异测试人为修改源码，例如翻转比较运算符或改变常量，然后运行测试。测试失败称为变异体被杀死。杀死比例称为变异得分。

变异得分高说明测试能够发现源码改动。存活变异体可能有两类原因。第一，测试没有覆盖该行为。第二，变异与原始代码语义等价。人工判断等价性成本较高，因此变异得分通常作为敏感性下界报告。

## 本实验中的使用

主实验十个模型条件组合的 RegressionRate 都是 0.000。若直接解释为负面反馈没有引入回归，会忽略指标不敏感的可能。

回归敏感性诊断显示，24 题回归测试总覆盖率为 0.916，非目标文件覆盖率为 0.918。六题变异得分为 0.787，其中 T13 为 0.375。该结果说明回归测试整体可用，但部分边界行为存在盲区，零回归需要谨慎表述。

## 参考

- Papadakis M, Kintis M, Zhang J, et al. Mutation Testing Advances: An Analysis and Survey. Advances in Computers, 2019.
- Hemmati H. How Effective Are Code Coverage Criteria? IEEE International Conference on Software Quality, Reliability and Security, 2015.
