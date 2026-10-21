# 质性编码材料

## 抽样

`qualitative_samples.csv` 按模型与条件分层，每个组合最多抽取两个成功与两个失败的分支 episode，不足时全取。抽样规则为任务名排序后取前两条，可复现。共三十一条。

每条记录给出累计 diff、事件流、提示词与 summary 的路径，便于从编码回溯到原始材料。

## 编码表

`qualitative_coding.csv` 保留同样的标识列，并增加八个编码列与备注列。

| 编码 | 取值 | 含义 |
|---|---|---|
| reads_log_first | 是 否 不确定 | 第一次编辑前是否读取错误日志或测试输出 |
| locates_callers | 是 否 不确定 | 是否用 grep 或 glob 查找调用方与相关模块 |
| only_target_lines | 是 否 不确定 | diff 是否只触碰目标函数的必要行 |
| rewrites_function | 是 否 不确定 | 是否整体重写目标函数而非局部修改 |
| unrelated_file | 是 否 不确定 | 是否修改目标文件之外的文件 |
| defensive_branch | 是 否 不确定 | 是否增加防御性分支或吞异常 |
| reverted_previous | 是 否 不确定 | 是否回退或重写上一轮方案 |
| claims_done_unverified | 是 否 不确定 | 是否未验证就宣称完成 |

`unrelated_file` 与 `reverted_previous` 可先由 episode 指标预填，再由编码者结合 diff 确认。其余编码需要阅读事件流与 diff。

## 使用约束

编码由同一人完成时，报告应说明编码者身份，不声称编码者间信度。编码表为空表示尚未开始，不得把空值当作否定。
