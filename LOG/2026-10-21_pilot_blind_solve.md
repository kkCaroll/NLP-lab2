# 2026-10-21 pilot 盲解与复核准备

## 目标

为 T01、T05、T16、T21 安排 DeepSeek-V4-Pro 盲解，生成人工复核材料，并检查任务文件夹。

## 盲解环境

- OpenCode 1.18.25
- 模型 deepseek/deepseek-v4-pro
- 隔离配置位于 `RECORD/calibration/opencode-config`
- 隔离数据目录位于 `RECORD/calibration/opencode-data`
- 权限只允许读取、编辑、glob、grep、list 与 `python -m pytest`
- 步数上限 12，单次超时 420 秒

## 命令

```bash
python harness/blind_solve.py
```

## 结果

```text
T01_next_palindrome   PASS 15 passed  steps=5  tools=10  diff=2  tampered=False
T05_email_regex       PASS 14 passed  steps=6  tools=10  diff=2  tampered=False
T16_sales_aggregation PASS 16 passed  steps=6  tools=13  diff=2  tampered=False
T21_first_duplicate   PASS 19 passed  steps=6  tools=15  diff=7  tampered=False
```

四次运行合计费用 0.041564 美元，无超时，无测试篡改。

## 产物

| 路径 | 内容 |
|---|---|
| RECORD/calibration/blind/T*/prompt.txt | 盲解提示词 |
| RECORD/calibration/blind/T*/events.jsonl | OpenCode 原始事件 |
| RECORD/calibration/blind/T*/model.patch | 模型修改 |
| RECORD/calibration/blind/T*/pytest.txt | 最终测试输出 |
| RECORD/calibration/blind/T*/summary.json | 单题汇总 |
| RECORD/calibration/blind/summary.json | 四题汇总 |
| RECORD/calibration/review/ | 人工复核表 |

## 处理记录

- 首次生成 T01 补丁时使用 `git diff --no-index`，路径包含绝对路径与引号。现改为逐文件 `difflib` 对比，补丁路径统一为 `a/` 与 `b/` 前缀的相对路径。
- 单题运行会覆盖顶层 `summary.json`。现有汇总由四个单题文件重新合并。
- T21 的工具调用达到外部上限 15 次，但进程正常结束并全部通过。正式实验需单独记录接近上限与预算耗尽的运行。

## 待办

人工复核表已生成，签字栏保持空白。签字后再冻结 pilot 题，并用 DeepSeek-V4.1-Flash 与 GLM-5.3-Flash 运行 pilot。未执行 git commit。
