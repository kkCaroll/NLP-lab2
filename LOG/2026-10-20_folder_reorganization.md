# 2026-10-20 目录整理

## 目标

按 CLAUDE.md 的目录约定整理项目，使计划、日志、结果与笔记各自归位。

## 操作

1. 将根目录的 PLAN.md 移至 PLAN/00_experiment_plan.md。
2. 将 TASK_AUTHORING_EVAL.md 移至 PLAN/02_task_authoring_eval.md。
3. 将 PLAN/TASK_SOURCE_EVAL.md 更名为 PLAN/01_task_source_eval.md。
4. 将候选池文件更名为 PLAN/03_candidate_pool.json 与 PLAN/03_candidate_pool.md。
5. 将 models 目录移至 PLAN/models。
6. 更新文档链接、inventory_sources.py 输出路径与来源说明中的路径。
7. 为根目录及 PLAN、LOG、RECORD、NOTES、harness、tasks 添加 README。

## 结果

```text
nlp_proj_2/
  README.md
  REQUIRE.md
  PLAN/
    README.md
    00_experiment_plan.md
    01_task_source_eval.md
    02_task_authoring_eval.md
    03_candidate_pool.md
    03_candidate_pool.json
    models/
      README.md
      MODELS.md
      models.json
  LOG/
    README.md
    2026-10-20_source_inventory.md
    2026-10-20_T01_construction.md
    2026-10-20_folder_reorganization.md
  RECORD/
    README.md
  NOTES/
    README.md
  harness/
    README.md
    inventory_sources.py
  tasks/
    README.md
    _sources/
    T01_next_palindrome/
```

## 验证

- 本地 Markdown 链接检查无缺失
- 候选池重新生成，总数 53，QuixBugs 22，BigCodeBench 31
- T01 buggy 状态仍为 4 failed 与 5 passed

## 备注

本次整理未执行 git commit。

## 下一步

1. 重新运行 python -I harness/inventory_sources.py，确认候选池写入新路径。
2. 构造 T05、T16、T21。
3. 对 pilot 题执行 G1 到 G12 验证。
