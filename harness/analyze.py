#!/usr/bin/env python3
"""Descriptive and paired analyses for the feedback experiment.

The main analysis uses the branch subset, that is tasks whose first round
failed. Round 1 passing tasks are reused across all five conditions and are
reported separately as a full sample descriptive table.

All tests are exploratory. Binary outcomes use Cochran's Q and exact McNemar
tests. Continuous outcomes use Friedman and Wilcoxon signed-rank tests. Ten
pairwise comparisons are adjusted with Holm's method. Effect sizes are Cliff's
delta with a paired bootstrap interval.
"""

from __future__ import annotations

import argparse
import json
import math
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "RECORD" / "analysis"
CONDITIONS = [
    "pure_continue",
    "neutral",
    "method_guidance",
    "negative",
    "negative_guidance",
]
SEED = 20261021
BOOTSTRAP = 10000


def regression_test_counts() -> dict[str, int]:
    counts = {}
    for meta_path in (ROOT / "tasks").glob("T*/meta.json"):
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        counts[meta_path.parent.name] = len(meta.get("regression_tests", []))
    return counts


def model_slug(model: str) -> str:
    return model.replace("/", "_").replace(":", "_")


def attach_tool_attempts(frame: pd.DataFrame, run_id: str) -> pd.DataFrame:
    path = ANALYSIS / f"tool_attempts_{run_id}.csv"
    if not path.is_file():
        return frame
    attempts = pd.read_csv(path)
    slug_to_model = {model_slug(model): model for model in frame["model"].unique()}
    attempts["model"] = attempts["model"].map(slug_to_model)
    attempts["episode_key"] = attempts["episode"].astype(str)
    frame = frame.copy()
    frame["episode_key"] = frame.apply(
        lambda row: "round1"
        if row["round1_passed"] == True  # noqa: E712
        else f"branches/{row['condition']}",
        axis=1,
    )
    columns = [
        "bash_attempts",
        "bash_completed",
        "bash_permission_denied",
        "bash_unavailable",
        "invalid_calls",
    ]
    merged = frame.merge(
        attempts[["model", "task", "episode_key", *columns]],
        on=["model", "task", "episode_key"],
        how="left",
    )
    return merged


def read_episodes(path: Path, run_id: str | None = None) -> pd.DataFrame:
    frame = pd.read_csv(path)
    counts = regression_test_counts()
    frame["regression_test_count"] = frame["task"].map(counts).fillna(0).astype(int)
    for column in (
        "valid",
        "round1_passed",
        "reused_round1",
        "all_passed",
        "repair_success",
        "over_edit",
        "unrelated_file",
        "test_tampered",
        "budget_exhausted",
        "timed_out",
        "any_edit",
        "no_edit",
        "no_edit_failure",
        "revert",
    ):
        if column in frame:
            frame[column] = frame[column].astype(str).str.lower().map(
                {"true": True, "false": False, "nan": np.nan}
            )
    if run_id:
        frame = attach_tool_attempts(frame, run_id)
    return frame


def branch_frame(frame: pd.DataFrame) -> pd.DataFrame:
    return frame[
        (frame["valid"] == True)  # noqa: E712
        & (frame["round1_passed"] == False)  # noqa: E712
    ].copy()


def full_frame(frame: pd.DataFrame) -> pd.DataFrame:
    return frame[frame["valid"] == True].copy()  # noqa: E712


def numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def describe(values: pd.Series) -> dict:
    clean = numeric(values).dropna()
    if clean.empty:
        return {
            "n": 0,
            "mean": None,
            "median": None,
            "q1": None,
            "q3": None,
            "min": None,
            "max": None,
        }
    return {
        "n": int(clean.size),
        "mean": round(float(clean.mean()), 4),
        "median": round(float(clean.median()), 4),
        "q1": round(float(clean.quantile(0.25)), 4),
        "q3": round(float(clean.quantile(0.75)), 4),
        "min": round(float(clean.min()), 4),
        "max": round(float(clean.max()), 4),
    }


def rate(values: pd.Series) -> tuple[float | None, int, int]:
    clean = values.dropna()
    if clean.empty:
        return None, 0, 0
    return round(float(clean.mean()), 4), int(clean.sum()), int(clean.size)


def descriptive_row(
    frame: pd.DataFrame, model: str, condition: str, sample: str
) -> dict:
    subset = frame[
        (frame["model"] == model) & (frame["condition"] == condition)
    ]
    pass_rate, passed, n = rate(subset["all_passed"])
    repaired = int(subset["repair_success"].fillna(False).sum())
    failures = int((subset["round1_passed"] == False).sum())  # noqa: E712
    repair_rate = round(repaired / failures, 4) if failures else None
    regression_failed = int(
        pd.to_numeric(subset["regression_failed"], errors="coerce")
        .fillna(0)
        .sum()
    )
    regression_tests = int(subset["regression_test_count"].sum())
    regression_rate = (
        round(regression_failed / regression_tests, 4)
        if regression_tests
        else None
    )
    effective = pd.to_numeric(
        subset.get("effective_tool_calls", pd.Series(dtype=float)),
        errors="coerce",
    )
    if effective.notna().sum() == 0 and "invalid_calls" in subset:
        effective = (
            pd.to_numeric(subset["tool_calls"], errors="coerce")
            - pd.to_numeric(subset["invalid_calls"], errors="coerce").fillna(0)
            - pd.to_numeric(
                subset.get(
                    "bash_permission_denied", pd.Series(dtype=float)
                ),
                errors="coerce",
            ).fillna(0)
        )
    return {
        "sample": sample,
        "model": model,
        "condition": condition,
        "n": n,
        "passed": passed,
        "pass_rate": pass_rate,
        "repaired": repaired,
        "round1_failures": failures,
        "repair_success": repair_rate,
        "regression_failed_tests": regression_failed,
        "regression_rate": regression_rate,
        "regression_tests": regression_tests,
        "edit_size": describe(subset["edit_lines"]),
        "edit_ratio": describe(subset["edit_ratio"]),
        "edit_files": describe(subset["edit_file_count"]),
        "over_edit_rate": rate(subset["over_edit"])[0],
        "unrelated_file_rate": rate(subset["unrelated_file"])[0],
        "test_tamper_rate": rate(subset["test_tampered"])[0],
        "budget_exhausted_rate": rate(subset["budget_exhausted"])[0],
        "timeout_rate": rate(subset["timed_out"])[0],
        "any_edit_rate": rate(subset["any_edit"])[0],
        "no_edit_rate": rate(subset["no_edit"])[0],
        "no_edit_failure_rate": rate(subset["no_edit_failure"])[0],
        "revert_rate": rate(subset["revert"])[0],
        "effective_tool_calls": describe(effective),
        "bash_attempts": describe(
            subset.get("bash_attempts", pd.Series(dtype=float))
        ),
        "tool_calls": describe(subset["tool_calls"]),
        "duration_s": describe(subset["duration_s"]),
    }


def wide_matrix(
    frame: pd.DataFrame, model: str, metric: str, binary: bool = False
) -> pd.DataFrame:
    subset = frame[frame["model"] == model]
    wide = subset.pivot_table(
        index="task", columns="condition", values=metric, aggfunc="first"
    )
    wide = wide.reindex(columns=CONDITIONS)
    wide = wide.dropna()
    if binary:
        wide = wide.astype(float).astype(int)
    else:
        wide = wide.astype(float)
    return wide


def cochran_q(matrix: np.ndarray) -> tuple[float, float]:
    n, k = matrix.shape
    column_sums = matrix.sum(axis=0)
    row_sums = matrix.sum(axis=1)
    total = matrix.sum()
    denominator = k * total - float((row_sums**2).sum())
    if denominator == 0:
        return 0.0, 1.0
    q = (k - 1) * (k * float((column_sums**2).sum()) - total**2) / denominator
    return float(q), float(stats.chi2.sf(q, k - 1))


def mcnemar_exact(a: np.ndarray, b: np.ndarray) -> dict:
    both = int(((a == 1) & (b == 1)).sum())
    only_a = int(((a == 1) & (b == 0)).sum())
    only_b = int(((a == 0) & (b == 1)).sum())
    neither = int(((a == 0) & (b == 0)).sum())
    discordant = only_a + only_b
    if discordant == 0:
        p_value = 1.0
    else:
        p_value = float(
            stats.binomtest(min(only_a, only_b), discordant, 0.5).pvalue
        )
    return {
        "both": both,
        "only_first": only_a,
        "only_second": only_b,
        "neither": neither,
        "discordant": discordant,
        "p": p_value,
        "risk_difference": round((a.mean() - b.mean()), 4),
    }


def cliffs_delta(first: np.ndarray, second: np.ndarray) -> float:
    first = np.asarray(first, dtype=float)
    second = np.asarray(second, dtype=float)
    diff = first[:, None] - second[None, :]
    return float((np.sign(diff)).sum() / (first.size * second.size))


def bootstrap_delta_ci(
    first: np.ndarray, second: np.ndarray, rng: np.random.Generator
) -> tuple[float, float]:
    n = first.size
    values = np.empty(BOOTSTRAP)
    for index in range(BOOTSTRAP):
        sample = rng.integers(0, n, n)
        values[index] = cliffs_delta(first[sample], second[sample])
    lower, upper = np.percentile(values, [2.5, 97.5])
    return float(lower), float(upper)


def holm(p_values: list[float]) -> list[float]:
    count = len(p_values)
    order = sorted(range(count), key=lambda index: p_values[index])
    adjusted = [0.0] * count
    running = 0.0
    for rank, index in enumerate(order):
        value = min(1.0, (count - rank) * p_values[index])
        running = max(running, value)
        adjusted[index] = running
    return adjusted


def paired_analysis(
    frame: pd.DataFrame, model: str, metric: str, binary: bool
) -> dict:
    wide = wide_matrix(frame, model, metric, binary=binary)
    result = {"model": model, "metric": metric, "n_tasks": int(len(wide))}
    if len(wide) < 3:
        result["error"] = "fewer than three complete tasks"
        return result
    arrays = {condition: wide[condition].to_numpy() for condition in CONDITIONS}
    if binary:
        q, q_p = cochran_q(np.column_stack([arrays[c] for c in CONDITIONS]))
        result["omnibus"] = {"test": "cochran_q", "statistic": round(q, 4), "p": q_p}
    else:
        statistic, p_value = stats.friedmanchisquare(
            *[arrays[condition] for condition in CONDITIONS]
        )
        result["omnibus"] = {
            "test": "friedman",
            "statistic": round(float(statistic), 4),
            "p": float(p_value),
        }
    rng = np.random.default_rng(SEED)
    pairs = []
    for first, second in combinations(CONDITIONS, 2):
        if binary:
            test = mcnemar_exact(arrays[first], arrays[second])
            pairs.append(
                {
                    "first": first,
                    "second": second,
                    **test,
                }
            )
        else:
            if np.allclose(arrays[first], arrays[second]):
                p_value = 1.0
            else:
                p_value = float(
                    stats.wilcoxon(
                        arrays[first],
                        arrays[second],
                        zero_method="zsplit",
                        alternative="two-sided",
                    ).pvalue
                )
            delta = cliffs_delta(arrays[first], arrays[second])
            lower, upper = bootstrap_delta_ci(
                arrays[first], arrays[second], rng
            )
            pairs.append(
                {
                    "first": first,
                    "second": second,
                    "median_first": round(float(np.median(arrays[first])), 4),
                    "median_second": round(float(np.median(arrays[second])), 4),
                    "median_difference": round(
                        float(np.median(arrays[first] - arrays[second])), 4
                    ),
                    "cliffs_delta": round(delta, 4),
                    "delta_ci_low": round(lower, 4),
                    "delta_ci_high": round(upper, 4),
                    "p": p_value,
                }
            )
    adjusted = holm([pair["p"] for pair in pairs])
    for pair, value in zip(pairs, adjusted):
        pair["p_holm"] = value
    result["pairs"] = pairs
    return result


def cohen_kappa(first: list[int], second: list[int]) -> float | None:
    if not first:
        return None
    first_array = np.asarray(first)
    second_array = np.asarray(second)
    observed = float((first_array == second_array).mean())
    categories = sorted(set(first) | set(second))
    expected = 0.0
    for category in categories:
        expected += float((first_array == category).mean()) * float(
            (second_array == category).mean()
        )
    if math.isclose(expected, 1.0):
        return None
    return round((observed - expected) / (1 - expected), 4)


def icc_2_1(matrix: np.ndarray) -> float | None:
    n, k = matrix.shape
    if n < 2 or k < 2:
        return None
    grand = float(matrix.mean())
    row_means = matrix.mean(axis=1)
    column_means = matrix.mean(axis=0)
    ssr = k * float(((row_means - grand) ** 2).sum())
    ssc = n * float(((column_means - grand) ** 2).sum())
    residual = (
        matrix - row_means[:, None] - column_means[None, :] + grand
    )
    sse = float((residual**2).sum())
    msr = ssr / (n - 1)
    msc = ssc / (k - 1)
    mse = sse / ((n - 1) * (k - 1))
    denominator = msr + (k - 1) * mse + k * (msc - mse) / n
    if denominator == 0:
        return None
    return round((msr - mse) / denominator, 4)


def reliability_analysis(main: pd.DataFrame, rerun: pd.DataFrame) -> dict:
    keys = ["model", "task", "condition"]
    left = branch_frame(main)[keys + ["all_passed", "edit_lines"]].rename(
        columns={"all_passed": "all_passed_main", "edit_lines": "edit_main"}
    )
    right = branch_frame(rerun)[keys + ["all_passed", "edit_lines"]].rename(
        columns={"all_passed": "all_passed_rerun", "edit_lines": "edit_rerun"}
    )
    merged = left.merge(right, on=keys, how="inner")
    result = {"n_episodes": int(len(merged)), "by_model": {}}
    for model, group in merged.groupby("model"):
        binary = group.dropna(subset=["all_passed_main", "all_passed_rerun"])
        continuous = group.dropna(subset=["edit_main", "edit_rerun"])
        matrix = continuous[["edit_main", "edit_rerun"]].to_numpy(dtype=float)
        if len(continuous) >= 2 and continuous["edit_main"].nunique() > 1:
            rho, rho_p = stats.spearmanr(
                continuous["edit_main"], continuous["edit_rerun"]
            )
            spearman = [round(float(rho), 4), float(rho_p)]
        else:
            spearman = [None, None]
        result["by_model"][model] = {
            "n": int(len(group)),
            "binary_n": int(len(binary)),
            "agreement": round(
                float(
                    (
                        binary["all_passed_main"]
                        == binary["all_passed_rerun"]
                    ).mean()
                ),
                4,
            )
            if len(binary)
            else None,
            "kappa": cohen_kappa(
                binary["all_passed_main"].astype(int).tolist(),
                binary["all_passed_rerun"].astype(int).tolist(),
            ),
            "icc_2_1_edit_lines": icc_2_1(matrix) if len(continuous) >= 2 else None,
            "spearman_edit": spearman[0],
            "spearman_p": spearman[1],
            "mean_absolute_edit_difference": round(
                float(np.abs(matrix[:, 0] - matrix[:, 1]).mean()), 4
            )
            if len(continuous)
            else None,
            "by_condition": {},
        }
        for condition, cell in group.groupby("condition"):
            cell_binary = cell.dropna(
                subset=["all_passed_main", "all_passed_rerun"]
            )
            result["by_model"][model]["by_condition"][condition] = {
                "n": int(len(cell)),
                "agreement": round(
                    float(
                        (
                            cell_binary["all_passed_main"]
                            == cell_binary["all_passed_rerun"]
                        ).mean()
                    ),
                    4,
                )
                if len(cell_binary)
                else None,
                "kappa": cohen_kappa(
                    cell_binary["all_passed_main"].astype(int).tolist(),
                    cell_binary["all_passed_rerun"].astype(int).tolist(),
                ),
            }
    return result


def ablation_analysis(main: pd.DataFrame, ablation: pd.DataFrame) -> dict:
    keys = ["model", "task", "condition"]
    left = branch_frame(main)[keys + ["all_passed", "edit_lines"]].rename(
        columns={"all_passed": "all_passed_main", "edit_lines": "edit_main"}
    )
    right = branch_frame(ablation)[keys + ["all_passed", "edit_lines"]].rename(
        columns={"all_passed": "all_passed_ablation", "edit_lines": "edit_ablation"}
    )
    merged = left.merge(right, on=keys, how="inner")
    result = {"n_episodes": int(len(merged)), "by_model": {}}
    rng = np.random.default_rng(SEED)
    for model, group in merged.groupby("model"):
        binary = group.dropna(subset=["all_passed_main", "all_passed_ablation"])
        continuous = group.dropna(subset=["edit_main", "edit_ablation"])
        entry = {
            "n": int(len(group)),
            "pass_rate_main": round(float(binary["all_passed_main"].mean()), 4)
            if len(binary)
            else None,
            "pass_rate_ablation": round(
                float(binary["all_passed_ablation"].mean()), 4
            )
            if len(binary)
            else None,
            "pass_difference": round(
                float(
                    (
                        binary["all_passed_main"]
                        - binary["all_passed_ablation"]
                    ).mean()
                ),
                4,
            )
            if len(binary)
            else None,
            "median_edit_main": round(float(continuous["edit_main"].median()), 4)
            if len(continuous)
            else None,
            "median_edit_ablation": round(
                float(continuous["edit_ablation"].median()), 4
            )
            if len(continuous)
            else None,
        }
        if len(continuous) >= 2:
            delta = cliffs_delta(
                continuous["edit_main"].to_numpy(),
                continuous["edit_ablation"].to_numpy(),
            )
            lower, upper = bootstrap_delta_ci(
                continuous["edit_main"].to_numpy(),
                continuous["edit_ablation"].to_numpy(),
                rng,
            )
            entry.update(
                {
                    "cliffs_delta_edit": round(delta, 4),
                    "delta_ci_low": round(lower, 4),
                    "delta_ci_high": round(upper, 4),
                }
            )
        result["by_model"][model] = entry
    return result


def describe_table(frame: pd.DataFrame, sample: str) -> list[dict]:
    rows = []
    for model in sorted(frame["model"].unique()):
        for condition in CONDITIONS:
            rows.append(descriptive_row(frame, model, condition, sample))
    return rows


def flatten_rows(rows: list[dict]) -> pd.DataFrame:
    flat = []
    for row in rows:
        item = {
            key: value
            for key, value in row.items()
            if not isinstance(value, dict) and key != "model"
        }
        item["model"] = row["model"]
        for prefix in (
            "edit_size",
            "edit_ratio",
            "edit_files",
            "effective_tool_calls",
            "bash_attempts",
            "tool_calls",
            "duration_s",
        ):
            for key, value in row[prefix].items():
                item[f"{prefix}_{key}"] = value
        flat.append(item)
    columns = [
        "sample",
        "model",
        "condition",
        "n",
        "passed",
        "pass_rate",
        "repaired",
        "round1_failures",
        "repair_success",
        "regression_failed_tests",
        "regression_rate",
        "regression_tests",
        "over_edit_rate",
        "unrelated_file_rate",
        "test_tamper_rate",
        "budget_exhausted_rate",
        "timeout_rate",
        "any_edit_rate",
        "no_edit_rate",
        "no_edit_failure_rate",
        "revert_rate",
        "edit_size_mean",
        "edit_size_median",
        "edit_size_q1",
        "edit_size_q3",
        "edit_size_min",
        "edit_size_max",
        "edit_ratio_mean",
        "edit_ratio_median",
        "edit_ratio_q1",
        "edit_ratio_q3",
        "edit_files_median",
        "effective_tool_calls_median",
        "bash_attempts_median",
        "tool_calls_median",
        "duration_s_median",
    ]
    return pd.DataFrame(flat)[columns]


def markdown_report(
    branch_rows: list[dict], full_rows: list[dict], stats_payload: dict
) -> str:
    lines = [
        "# 主实验统计分析",
        "",
        "配对分析仅使用第一轮失败任务的分支子集。全样本表包含第一轮通过任务在五条件中复用的终态。",
        "",
        "## 分支子集描述统计",
        "",
        "| 模型 | 条件 | n | PassRate | RepairSuccess | RegressionRate | EditSize 中位数 | EditRatio 中位数 | OverEditRate | 无编辑失败率 |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in branch_rows:
        lines.append(
            f"| {short_model(row['model'])} | {row['condition']} | {row['n']} | "
            f"{fmt(row['pass_rate'])} | {fmt(row['repair_success'])} | "
            f"{fmt(row['regression_rate'])} | {fmt(row['edit_size']['median'])} | "
            f"{fmt(row['edit_ratio']['median'])} | {fmt(row['over_edit_rate'])} | "
            f"{fmt(row['no_edit_failure_rate'])} |"
        )
    lines.extend(
        [
            "",
            "## 全样本描述统计",
            "",
            "| 模型 | 条件 | n | PassRate | RepairSuccess | EditSize 中位数 | EditRatio 中位数 |",
            "|---|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in full_rows:
        lines.append(
            f"| {short_model(row['model'])} | {row['condition']} | {row['n']} | "
            f"{fmt(row['pass_rate'])} | {fmt(row['repair_success'])} | "
            f"{fmt(row['edit_size']['median'])} | {fmt(row['edit_ratio']['median'])} |"
        )
    lines.extend(["", "## 配对检验", ""])
    for model, entry in stats_payload["paired"].items():
        lines.append(f"### {short_model(model)}")
        lines.append("")
        for metric, result in entry.items():
            omnibus = result.get("omnibus", {})
            lines.append(
                f"{metric} 整体检验 {omnibus.get('test', 'NA')} "
                f"统计量 {fmt(omnibus.get('statistic'))} "
                f"p {fmt_p(omnibus.get('p'))}，完整任务 {result.get('n_tasks', 0)}。"
            )
            lines.append("")
            lines.append(
                "| 条件 A | 条件 B | 效应量 | 95% CI | p | Holm p |"
            )
            lines.append("|---|---|---|---:|---:|---:|")
            for pair in result.get("pairs", []):
                if metric == "all_passed":
                    effect = f"RD {fmt(pair['risk_difference'])}"
                else:
                    effect = f"delta {fmt(pair['cliffs_delta'])}"
                ci = (
                    f"[{fmt(pair.get('delta_ci_low'))}, {fmt(pair.get('delta_ci_high'))}]"
                    if "delta_ci_low" in pair
                    else "NA"
                )
                lines.append(
                    f"| {pair['first']} | {pair['second']} | {effect} | {ci} | "
                    f"{fmt_p(pair['p'])} | {fmt_p(pair['p_holm'])} |"
                )
            lines.append("")
    if "reliability" in stats_payload:
        lines.extend(
            [
                "## 复跑一致性",
                "",
                "同一题同一条件在主运行与随机顺序复跑之间的结果一致性。覆盖仅限两轮均进入分支的 episode。",
                "",
                "| 模型 | n | 通过一致率 | Cohen kappa | ICC(2,1) EditSize | Spearman rho | 平均绝对修改差 |",
                "|---|---:|---:|---:|---:|---:|---:|",
            ]
        )
        for model, entry in stats_payload["reliability"]["by_model"].items():
            lines.append(
                f"| {short_model(model)} | {entry['n']} | {fmt(entry['agreement'])} | "
                f"{fmt(entry['kappa'])} | {fmt(entry['icc_2_1_edit_lines'])} | "
                f"{fmt(entry['spearman_edit'])} | "
                f"{fmt(entry['mean_absolute_edit_difference'])} |"
            )
        lines.append("")
        lines.append("按条件一致率如下。每格样本量为五或更少，仅作描述。")
        lines.append("")
        lines.append(
            "| 模型 | 条件 | n | 通过一致率 | Cohen kappa |"
        )
        lines.append("|---|---|---:|---:|---:|")
        for model, entry in stats_payload["reliability"]["by_model"].items():
            for condition, cell in entry.get("by_condition", {}).items():
                lines.append(
                    f"| {short_model(model)} | {condition} | {cell['n']} | "
                    f"{fmt(cell['agreement'])} | {fmt(cell['kappa'])} |"
                )
        lines.append("")
    if "ablation" in stats_payload:
        lines.extend(
            [
                "## 无测试消融",
                "",
                "同一题同一条件在主运行与无测试消融之间的配对差异。",
                "该表仅使用两次运行均进入分支的 episode。MiMo 消融六题第一轮通过，交集仅两题，因此 n 为十，不代表八题全样本。",
                "全样本比较见 `RECORD/analysis/ablation/README.md`。",
                "",
                "| 模型 | n | 主运行 PassRate | 消融 PassRate | 主减消融 | 主运行 EditSize 中位数 | 消融 EditSize 中位数 | Cliff delta | 95% CI |",
                "|---|---:|---:|---:|---:|---:|---:|---:|---|",
            ]
        )
        for model, entry in stats_payload["ablation"]["by_model"].items():
            lines.append(
                f"| {short_model(model)} | {entry['n']} | "
                f"{fmt(entry['pass_rate_main'])} | {fmt(entry['pass_rate_ablation'])} | "
                f"{fmt(entry['pass_difference'])} | {fmt(entry['median_edit_main'])} | "
                f"{fmt(entry['median_edit_ablation'])} | "
                f"{fmt(entry.get('cliffs_delta_edit'))} | "
                f"[{fmt(entry.get('delta_ci_low'))}, {fmt(entry.get('delta_ci_high'))}] |"
            )
        lines.append("")
    lines.extend(
        [
            "## 图",
            "",
            "![分支修复成功率](figures/repair_success.png)",
            "",
            "![分支 EditSize 分布](figures/edit_size.png)",
            "",
            "## 解释约束",
            "",
            "主实验条件顺序固定，条件与任务内位置完全共线，配对检验只能作为探索性描述。",
            "McNemar 检验在 MiniMax 十四对与 MiMo 六对失败任务下功效很低，不显著不能解释为无效应。",
            "回归测试零方差，不进行显著性检验，另见回归敏感性诊断。",
            "",
        ]
    )
    return "\n".join(lines)


def short_model(model: str) -> str:
    if "minimax" in model:
        return "MiniMax"
    if "mimo" in model:
        return "MiMo"
    return model


def fmt(value) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "NA"
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)


def fmt_p(value) -> str:
    if value is None:
        return "NA"
    return f"{value:.4f}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--main", default=str(ROOT / "RECORD" / "tables" / "episode_level.csv")
    )
    parser.add_argument("--reliability", default=None)
    parser.add_argument("--ablation", default=None)
    parser.add_argument("--output", default=str(ANALYSIS))
    args = parser.parse_args()

    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    main_frame = read_episodes(Path(args.main), "2026-10-21_main")
    branch = branch_frame(main_frame)
    full = full_frame(main_frame)

    branch_rows = describe_table(branch, "branch")
    full_rows = describe_table(full, "full")
    table = pd.concat(
        [flatten_rows(branch_rows), flatten_rows(full_rows)], ignore_index=True
    )
    table.to_csv(output / "main_results.csv", index=False, encoding="utf-8-sig")

    paired = {}
    for model in sorted(branch["model"].unique()):
        paired[model] = {
            "all_passed": paired_analysis(branch, model, "all_passed", True),
            "edit_lines": paired_analysis(branch, model, "edit_lines", False),
            "edit_ratio": paired_analysis(branch, model, "edit_ratio", False),
        }

    payload = {
        "seed": SEED,
        "bootstrap": BOOTSTRAP,
        "n_branch_rows": int(len(branch)),
        "n_full_rows": int(len(full)),
        "paired": paired,
        "descriptive": {"branch": branch_rows, "full": full_rows},
    }
    if args.reliability:
        rerun = read_episodes(Path(args.reliability), "2026-10-21_reliability")
        payload["reliability"] = reliability_analysis(main_frame, rerun)
    if args.ablation:
        ablation = read_episodes(Path(args.ablation), "2026-10-21_ablation")
        payload["ablation"] = ablation_analysis(main_frame, ablation)
    (output / "statistics.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (output / "main_results.md").write_text(
        markdown_report(branch_rows, full_rows, payload),
        encoding="utf-8",
        newline="\n",
    )
    print(
        f"wrote {output / 'main_results.csv'}, {output / 'main_results.md'}, "
        f"{output / 'statistics.json'}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
