# 2026-10-21 被测模型 pilot 首轮

## 目标

用 DeepSeek-V4.1-Flash 与 GLM-5.3-Flash 运行四道 pilot 题，检查首轮失败率。

## 命令

```bash
python harness/blind_solve.py --model deepseek/deepseek-flash --output RECORD/pilot/deepseek-flash
python harness/blind_solve.py --model opencode/glm-5.3-flash-free --output RECORD/pilot/glm-5.3-flash-free
```

## 结果

```text
DeepSeek-V4.1-Flash   4 passed  0 failed  失败率 0%  费用 0.007904 美元
GLM-5.3-Flash         4 passed  0 failed  失败率 0%  费用 0 美元
```

八次运行均未超时，均未修改测试，均只修改允许的源码文件。

## 结论

首轮失败率低于 40% 到 80% 的预注册区间。现有 pilot 题过易，不能直接进入主实验。

## 待办

需要在以下方案中选择一项并记录理由。

1. 用更困难的共享 helper 题替换 T16 与 T21。
2. 扩充 T16 与 T21 的模块耦合与干扰调用。
3. 接受 pilot 偏易并在主实验中提高困难题比例。

在方案确定前不修改题目，不进入主实验。未执行 git commit。
