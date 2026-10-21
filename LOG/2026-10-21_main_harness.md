# 2026-10-21 主实验 harness 与单题端到端流程

## 目标

构建主实验 harness，先打通单题从第一轮到五个反馈分支再到第二轮的完整流程。该阶段只验证流程正确性与产物完整性，不产生主实验结果。

## 实现

新增以下模块。

```text
harness/opencode_runner.py   启动 OpenCode，解析事件流，执行预算终止
harness/task_repo.py         任务仓库复制，git 初始化，提交，标签，diff，测试文件哈希
harness/grading.py           pytest 运行，JUnit XML 解析，目标测试与回归测试评分
harness/metrics.py           episode 指标计算
harness/branching.py         从第一轮状态复制五个独立分支
harness/prompts.py           第一轮模板，第二轮公共前缀，五种反馈句
harness/run_experiment.py    单题端到端编排
harness/configs/main/opencode.json      主实验配置
harness/configs/ablation/opencode.json  无测试消融配置，禁止全部 bash 命令
```

`run_experiment.py` 新增 `--config` 参数，可在主实验配置与消融配置之间切换，所用配置路径写入 `run_config.json`。

流程如下。

1. 把任务仓库复制到临时目录并初始化 git，提交 `baseline` 标签。
2. 运行第一轮，工具调用上限 10 次。
3. 恢复被篡改的测试文件，提交并打 `round1` 标签，运行 pytest，计算指标与 diff。
4. 若第一轮未通过，复制含 `.git` 的完整工作区五次，得到五个独立分支。
5. 每个分支运行第二轮，工具调用上限 15 次，使用新的 OpenCode 会话。
6. 提交并打 `round2` 标签，运行 pytest，计算累积 diff 与增量 diff。

第二轮 prompt 由三部分组成，即项目说明、第一轮累积 diff、当前测试日志，最后一句反馈因条件而异。运行前校验五个 prompt 的公共前缀逐字节相同，只有反馈句不同。

## 关键设计

**状态由 git 标签固定。** 第一轮与每个分支各自提交，所有 diff 与指标从标签计算，不依赖事件日志推断文件状态。每个 episode 记录 `baseline`、`round1`、`head` 三个提交哈希与工作树是否干净，用于事后审计。

**分支独立性由提交哈希核验。** 五个分支的 `round1` 标签必须等于第一轮 episode 的 `head`。2026-10-21 的验证运行中五个哈希完全一致。

**预算终止由外层控制。** OpenCode 的 `tool_use` 事件在工具执行结束后输出，因此计数达到上限时终止进程树，已完成的调用保留在 workspace 中。最后可能在途的一次调用会在终止前完成，其写入由稳定检测纳入提交。

**测试篡改检测。** 每个 episode 开始与结束时计算 `tests/` 与测试配置文件的哈希。若发生变化，从初始快照恢复，并记录 `test_tampered`。

**路径规范化。** 第二轮 prompt 中的临时工作区绝对路径替换为 `<workspace>`，避免把机器相关路径写入记录。

## 问题与修正

**预算计数差一。** 首次实现以计数大于上限终止，实际允许上限加一次完成调用。改为计数达到上限即终止。该问题在首轮预算收紧阶段已单独记录。

**diff 为空。** 提交信息被当作 git 引用使用。改为提交后打标签，diff 从标签计算。

**dataclass 字段顺序错误。** 有默认值的字段位于无默认值字段之前，导入时报错。调整字段顺序。

**第二轮前缀校验失败。** 以反馈句长度截断公共前缀时，反馈句首字符被留在前缀中。新增 `round2_prefix` 函数，直接构造公共前缀并做精确相等比较。

**进程残留导致运行挂起。** 一次运行 300 秒无输出，检查发现两个残留的 `opencode.exe` 进程持有锁。终止进程后恢复。随后把每个 episode 的 `XDG_DATA_HOME` 改为独立临时目录，避免会话数据库锁竞争。

**迟到写入与分支状态不一致。** 一次运行中 `negative_guidance` 分支只记录一次编辑，累积 diff 却包含两个文件。检查发现该分支继承了第一轮终止后迟到写入的 `units.py` 修改，而其余分支没有继承。根因是预算终止时仍有一次在途调用，其事件未输出但文件写入完成，分支复制发生在其落盘过程中。

修正方式是在 OpenCode 返回后等待源码树哈希连续两次相同，再恢复测试、提交与评分。修正后重跑，五个分支继承的 `round1` 哈希完全一致，工作树全部干净。最后在途调用仍可能不被事件计数，因此工具调用数与编辑次数可能少计一次，而 `EditSize`、文件数与 `EditRatio` 均由 diff 计算，不受该问题影响。报告方法部分需说明这一事件时序。

**运行产物占用过大。** OpenCode 把约 44 MB 依赖安装到配置目录，每个 episode 又持久化约 4 MB 会话数据库。配置目录改到项目内 `.runner/config` 并加入忽略规则，会话数据改到临时目录并随运行清理。记录目录只保留事件、prompt、pytest 输出、JUnit 报告、diff 与汇总，单题单模型约 0.5 MB。

## 验证

预算为 3 次与 4 次的短预算冒烟运行覆盖全部六个 episode，均按预期因预算耗尽失败，流程无异常。配置目录迁移后再次运行该冒烟测试，记录目录降至 221 KB，分支继承状态一致，说明存储调整未影响流程。

实际预算为 10 次与 15 次的 T14 运行结果如下。

```text
round1  FAIL  tools=10  edits=0  diff=0  budget=True
pure_continue       PASS  tools=15  edits=2  diff=4  delta=4  budget=True
neutral             PASS  tools=13  edits=2  diff=4  delta=4  budget=False
method_guidance     PASS  tools=13  edits=2  diff=4  delta=4  budget=False
negative            PASS  tools=13  edits=2  diff=4  delta=4  budget=False
negative_guidance   PASS  tools=15  edits=1  diff=4  delta=4  budget=True
```

第一轮因阅读阶段耗尽 10 次调用而失败，没有源码改动。五个分支均通过目标测试与回归测试，分支继承状态一致，第二轮 prompt 公共前缀逐字节相同。

## 状态

未执行 git commit。下一步补齐任务集到 12 道标准题与 12 道困难题，并实现批量运行、指标聚合与统计分析。无测试消融配置已经建立。
