# 2026-10-20 pilot 题反过拟合检查

## 目标

按 G10 检查四道 pilot 题是否只接受 gold 写法。每道题准备一个语义等价的替代修复和一个错误修复，在任务仓库的临时副本上运行完整测试。

## 命令

```bash
python harness/check_variants.py
```

## 关键输出

```text
T01_next_palindrome:
  alternative: passed
  wrong: failed
  OK
T05_email_regex:
  alternative: passed
  wrong: failed
  OK
T16_sales_aggregation:
  alternative: passed
  wrong: failed
  OK
T21_first_duplicate:
  alternative: passed
  wrong: failed
  OK
```

## 替代修复与错误修复

| 题目 | 替代修复 | 错误修复 |
|---|---|---|
| T01 | 把补零数量写成乘法形式 | 补零数量再减一 |
| T05 | 在字符类中用转义连字符并保留加号 | 保持原缺陷，未加入加号 |
| T16 | 用减法赋值代替减等于 | 保持原缺陷，仍为加法 |
| T21 | 记录首次出现位置并返回对应值 | 保持原缺陷，覆盖为最后一次重复值 |

## 结论

四道题的替代修复均通过完整测试，错误修复均至少在一项测试上失败。测试未绑定 gold 的具体写法，G10 通过。

检查在临时目录中进行，任务仓库未被修改。未对项目仓库执行 git commit。下一步安排 V4-Pro 盲解与人工复核。
