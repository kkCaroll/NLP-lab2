# 报告与演示

本目录存放最终报告、演示文稿与插图，按版本分目录。v1 为当前版本，v0 保留作对照。

| 路径 | 内容 |
|---|---|
| `report_v0/report_v0.md` | 报告 v0，主结果与首版补充诊断 |
| `report_v1/report_v1.md` | 报告 v1，新增质性编码、过程指标、预算补跑、功效分析与敏感性分析 |
| `slides_v0/` | 演示 v0 的 Marp 源文件与导出结果 |
| `slides_v1/` | 演示 v1 的源文件、导出结果与提示稿，`slides_v1_notes.md` 为十分钟讲稿 |
| `figures_v1/` | 报告 v1 与演示 v1 共用的六张插图，说明见该目录 README |
| `usage_recommendations.md` | 一页使用建议 |

各版本的源文件与插图目录同级，图片使用相对路径引用，移动文件时需同步修改。

重新渲染 v1 演示文稿，在 `slides_v1/` 目录内执行。

```bash
npx --yes @marp-team/marp-cli slides_v1.md --pptx --allow-local-files -o slides_v1.pptx
```

本机若无 Chrome，改用 Edge。

```bash
npx --yes @marp-team/marp-cli slides_v1.md --pptx --allow-local-files \
  --browser-path "/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" \
  -o slides_v1.pptx
```

报告中的数字来自 `RECORD/analysis/`，插图由 `harness/make_figures_v1.py` 生成。若重新运行分析脚本，应同步检查报告表格与正文。
