# 2026-10-20 T05 构造记录

## 题目

- 题目编号：T05
- 题目名称：`email_regex`
- 类别：正则
- 难度：标准
- 来源：BigCodeBench 761
- 来源版本：v0.1.4
- 许可：Apache-2.0

## 目录

```text
tasks/T05_email_regex/
  repo/
    pyproject.toml
    README.md
    src/mailscan/__init__.py
    src/mailscan/patterns.py
    src/mailscan/normalize.py
    src/mailscan/report.py
    tests/test_target.py
    tests/test_regression.py
  meta.json
  initial_test_log.txt
  gold.patch
  ATTRIBUTION.md
  LICENSE
```

## Bug

邮箱正则的本地部分字符类缺少加号，`alice+news@example.com` 无法通过 `is_email`，`extract_emails` 返回空列表。缺陷位于 `src/mailscan/patterns.py`，gold patch 只恢复字符类中的一个加号。

目标测试 2 个，覆盖加号标签地址的提取与报告辅助函数。回归测试 12 个，覆盖普通地址、校验、替换、域名统计、小写化、掩码、摘要、归一化和非法输入。

## 验证结果

buggy 状态：

```text
2 failed, 12 passed
```

gold 状态：

```text
14 passed
```

`harness/validate_tasks.py` 检查结果：

```text
T05_email_regex: OK
  note: files=4 lines=113 buggy=2 failed, 12 passed gold=14 passed
```

## 备注

- 源码规模为 4 个文件 113 行，符合标准题 2 到 4 个文件、100 到 250 行的约束。
- 测试文件在 gold 补丁前后哈希一致。
- `--repeat 5` 的五轮 buggy 状态检查结果一致，未出现跳过、随机失败或超时。
- 未对项目仓库执行 git commit。
- 等价修复与错误修复检查已通过，见 `2026-10-20_pilot_variant_checks.md`。
- 下一步安排 V4-Pro 盲解与人工复核。
