# 机械化判定核查

> 性质：编码表与源数据的一致性核查，不是信度证据
> 日期：2026-10-22
> 脚本：`harness/check_coding.py`

## 1 目的与定位

首轮三十一条编码由单一编码者完成。为把可由数据直接决定的编码从人工判断中分离出来，脚本对可机械化项独立重算，再与编码表逐项比对。

本节结果说明编码表与源数据是否一致。它不说明编码效度，也不替代编码信度统计。

## 2 可机械化范围

九项编码中三项可由数据直接决定。

| 编码 | 判定依据 |
|---|---|
| no_edit | 脱敏摘要的 `edits` 字段 |
| unrelated_file | 累计 diff 的文件列表与 `allowed_files` 作差 |
| reverted_previous | 第一轮 diff 与累计 diff 的行集合比对 |

其余六项不可机械化，原因如下。

1. `reads_log_first` 需判断模型是否把失败输出当作线索，属语义判断。
2. `locates_callers` 需判断某次读取或检索是否指向缺陷函数的调用方。
3. `only_target_lines` 需目标函数的行区间。任务元数据只给出 `gold_lines` 总改动行数，不给出区间，无法定位边界。
4. `rewrites_function` 需判断函数结构是否被整体替换，行数阈值不能可靠区分重写与集中修改。
5. `defensive_branch` 需判断新增分支是否为测试所要求，属语义判断。
6. `claims_done_unverified` 需判断最后文本是否构成可验证的完成声明。

## 3 判定规则

`no_edit` 取脱敏摘要的 `edits`，等于零记是，否则记否。

`unrelated_file` 在未编辑时记不适用。发生编辑时取累计 diff 的文件列表，减去 `allowed_files`，再减去测试文件与测试配置。测试文件包括 `tests/` 前缀、`conftest.py` 与 `sitecustomize.py`，测试配置包括 `pyproject.toml`、`pytest.ini`、`setup.cfg` 与 `tox.ini`。剩余集合非空记是，否则记否。排除测试文件的依据是手册 5.6 规定测试篡改另记，不并入本编码。

`reverted_previous` 在未编辑时记不适用。第一轮 diff 为空记否。否则取第一轮 diff 的新增行与累计 diff 的删除行，同一文件内出现交集记是。

第三条规则是手册 5.8 的宽松近似。脚本未实现主要方案这一限定，会把第一轮的单行修正误判为回退。本次三十一条的第一轮 diff 全部为空，该分支未被触发，差异不影响结果。若后续样本包含第一轮编辑，需要重新实现该规则。

## 4 结果

共 93 项判断，一致 93 项。

| 编码 | 一致数 | 编码表取值分布 |
|---|---:|---|
| no_edit | 31/31 | 是 10，否 21 |
| unrelated_file | 31/31 | 否 21，不适用 10 |
| reverted_previous | 31/31 | 否 21，不适用 10 |

无分歧条目。逐项明细见 `coding_machine_check.csv`。

## 5 解释边界

三项中两项在材料里已有现成答案。脱敏摘要同时保留 `edits`、`edit_files`、`unrelated_files` 与 `over_edit`，其中 `edits` 直接对应 `no_edit`，`unrelated_files` 直接对应 `unrelated_file`。编码手册 5.1 本身也规定 `no_edit` 由 `edits` 字段直接得到。因此这两项的一致属于定义内的一致，不含独立判断。

`reverted_previous` 的三十一条第一轮 diff 全部为空。按手册 5.8，结果只能是未编辑时的不适用或第一轮无修改时的否，由数据结构决定。

因此全部一致支持两点。编码表没有转录错误。三项规则在脚本与手册两种实现下给出同一结果。

不能支持编码判断准确这一表述。不能把本节数字作为编码信度写入报告。

## 6 对后续的意义

真正需要检验的是其余六项。第二编码者对九项全部重新判断，可对六项给出编码者间一致率。

机械化核查的作用是把不提供信息的项从一致性解释中去除，避免把结构决定的一致当作信度证据。报告中本节压缩为方法部分一句，附脚本与结果文件，不单独成表。

## 7 产物

| 文件 | 内容 |
|---|---|
| `harness/check_coding.py` | 三项编码的机械判定与比对 |
| `coding_machine_check.csv` | 93 行逐项结果，含 sample_id、code、manual、machine、match |

复现命令如下。

```bash
python harness/check_coding.py
```
