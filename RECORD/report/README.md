# 报告与演示

本目录存放最终报告与演示文稿。

| 文件 | 内容 |
|---|---|
| `report.md` | 完整实验报告，含研究问题、任务集、设计、主结果、补充诊断、效度威胁与结论 |
| `usage_recommendations.md` | 一页使用建议 |
| `slides_v0.md` | 演示文稿源文件 v0，Marp 格式 |
| `slides_v0.pptx` | 由 `slides_v0.md` 渲染的 v0 演示文稿 |
| `slides_preview_v0/` | v0 逐页 PNG 预览，用于检查排版 |

v0 为当前冻结版本。后续修订另存为 v1，本次不重新渲染。

重新渲染演示文稿。

```bash
npx --yes @marp-team/marp-cli slides_v0.md --pptx --allow-local-files -o slides_v0.pptx
npx --yes @marp-team/marp-cli slides_v0.md --images png --allow-local-files -o slides_preview_v0/slide.png
```

报告中的数字来自 `RECORD/analysis/`。若重新运行分析脚本，应同步检查报告表格与正文。
