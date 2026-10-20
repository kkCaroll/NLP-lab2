# 2026-10-20 T02 构造记录

## 题目

- 题目编号：T02
- 题目名称：`parse_range`
- 类别：边界条件
- 难度：标准
- 来源：原创
- 许可：原创任务

## 目录

```text
tasks/T02_parse_range/
  repo/
    pyproject.toml
    README.md
    src/rangekit/__init__.py
    src/rangekit/parse.py
    src/rangekit/merge.py
    src/rangekit/format.py
    tests/test_target.py
    tests/test_regression.py
  meta.json
  initial_test_log.txt
  gold.patch
  ATTRIBUTION.md
```

## Bug

`parse_range` 按半开区间处理输入，`1-5` 返回 1 到 4，缺少上界 5。缺陷位于 `src/rangekit/parse.py`，gold patch 把 `range(start, end)` 改为 `range(start, end + 1)`。

目标测试 2 个，覆盖单区间解析与多区间展开时的上界。回归测试 13 个，覆盖单值解析、非法输入、区间合并、格式化、摘要、去重、展开与端点校验。

## 验证结果

buggy 状态：

```text
2 failed, 13 passed
```

gold 状态：

```text
15 passed
```

`harness/validate_tasks.py` 检查结果：

```text
T02_parse_range: OK
  note: files=4 lines=119 buggy=2 failed, 13 passed gold=15 passed
```

## 备注

- 源码规模为 4 个文件 119 行，符合标准题约束。
- `--repeat 5` 的五轮 buggy 状态检查结果一致。
- G10 检查通过，替代修复用列表推导生成闭区间，错误修复把上界多加一。
- 生成 gold patch 时发现 `Path.write_text` 在 Windows 上默认写入 CRLF，导致 `git apply` 失败。补丁现以 `newline="\n"` 写入。
- 未对项目仓库执行 git commit。
- 下一步安排 T02 的 V4-Pro 盲解与人工复核。
