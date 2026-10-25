# 目录整理与路径修复

## 目标

整理报告目录的层级，修复文件移动造成的相对路径失效，清除可再生成的中间文件。

## 结构调整

报告目录此前将 v0 文件平铺在根层，v1 分置于子目录。现统一为按版本分目录。

```text
RECORD/report/
├── README.md
├── figures_v1/                 六张插图，报告与演示共用
├── report_v0/report_v0.md      由 RECORD/report/report.md 移入
├── report_v1/report_v1.md
├── slides_v0/slides_v0.md, slides_v0.pptx
├── slides_v1/slides_v1.md, slides_v1.pptx, slides_v1_notes.md
└── usage_recommendations.md
```

`report.md` 改名为 `report_v0.md` 并移入 `report_v0/`，与 `report_v1/` 对称，避免根层同时出现无名版本与 v1 版本。

## 路径修复

上一步用户移动文件后，源文件内的图片引用仍按旧层级书写。子目录加深一层，因此逐一修正。

1. `slides_v1.md` 六处图片引用由 `figures_v1/` 改为 `../figures_v1/`。
2. `report_v1.md` 五处图片引用同步修改，其中 `../analysis/figures/edit_size.png` 改为 `../../analysis/figures/edit_size.png`。
3. `report_v1.md` 首部对上一版本的引用改为 `../report_v0/report_v0.md`。

逐项核对目标文件存在，六张 v1 插图与 `edit_size.png` 均在预期位置。

同步更新下列文档中的路径。

1. 根 `README.md` 的进度条目。
2. `RECORD/README.md` 与 `RECORD/report/README.md` 的目录说明。
3. `NOTES/experiment_walkthrough.md` 的配套材料路径。
4. `PLAN/00_experiment_plan.md` 第 13 节交付物与 `PLAN/05_deepening.md` 的产出清单。

历史日志中的旧路径未改动，日志记录当时的状态。

## 已删除

| 路径 | 原因 | 体积 |
|---|---|---|
| `RECORD/report/slides.pptx` | 与 `slides_v0/slides_v0.pptx` 逐字节相同，校验值均为 d9202457 | 2.1M |
| `.pytest_cache/`、`harness/__pycache__/`、`RECORD/__pycache__/` | 解释器与测试缓存 | 少量 |
| `RECORD/report/slides_preview_v0/` | v0 逐页预览图，可由 Marp 重新导出 | 0.9M |

## 待确认的清理

以下目录体积较大，但属于原始运行数据或运行时环境，删除后需重新运行实验或重新安装依赖才能恢复，本次未删除，等待确认。

| 路径 | 内容 | 体积 | 可恢复性 |
|---|---|---|---|
| `RECORD/runs/2026-10-21_e2e` | 首轮端到端测试，其中 61M 为 opencode 依赖副本 | 64M | 需重跑测试 |
| `RECORD/runs/2026-10-21_e2e2` | 第二轮端到端测试，其中 29M 为依赖副本 | 32M | 需重跑测试 |
| `RECORD/runs/2026-10-21_e2e3` | 端到端测试，已被 e2e4 取代 | 0.5M | 需重跑测试 |
| `RECORD/runs/2026-10-22_budget_rerun_smoke` | 补跑冒烟测试，正式补跑已保留 | 0.2M | 需重跑测试 |
| `RECORD/calibration/opencode-config` | 盲解运行时的依赖与配置缓存 | 30M | 由 `blind_solve.py` 重建 |
| `RECORD/calibration/opencode-data` | 盲解运行时的日志、数据库与快照缓存 | 23M | 运行后自动重建 |
| `.runner/config/opencode/node_modules` | 主实验 opencode 运行时依赖 | 61M | 需联网重装 |

前六项合计约 150M，均为可再生成的运行时缓存或已被取代的测试记录，不影响主实验、复跑、消融与补跑的原始数据，也不影响任何分析脚本，因为相关脚本默认只读取指定运行目录。第七项为当前 harness 正在使用的运行时，若删除，下一次运行需重新下载依赖。

## 校验

1. `grep` 检查全部 Markdown 与 Python 文件，活跃文档中无指向旧层级的路径。
2. 历史日志保留旧路径，属于记录当时状态的正常情况。
3. 未执行任何 git 提交。
