#!/usr/bin/env python3
"""Render the four report v1 figures.

Style, palette and model hues are imported from make_figures.py so the v1
figures match v0. Every figure draws from an existing analysis table; no
number is recomputed here.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_figures import (  # noqa: E402
    CONDITIONS,
    LABELS,
    MODEL_LABELS,
    MUTED,
    SURFACE,
    TEXT,
    clean_axes,
    repair_success_figure,
    setup_style,
)

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "RECORD" / "analysis" / "deepening"
DEEP_BLUE = "#2a78d6"
DEEP_ORANGE = "#eb6834"
DEEP_AQUA = "#1baf7a"
NEUTRAL_DARK = "#8a8880"
NEUTRAL_LIGHT = "#e1e0d9"

# The sensitivity table stores short model names without the provider prefix.
SHORT_TO_FULL = {
    key.split("/")[-1]: key for key in MODEL_LABELS
}


def difficulty_figure(sensitivity: pd.DataFrame, output: Path) -> None:
    """Pass rate by condition for standard and hard tasks, faceted."""
    data = sensitivity[sensitivity["scenario"].isin(["standard", "hard"])]
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.6), sharey=True)
    panels = [("standard", "标准题"), ("hard", "困难题")]
    styles = {
        "opencode/minimax-m3.1-flash-free": ("-", "o", 44),
        "opencode/mimo-v2.6-flash-free": ("--", "s", 104),
    }
    for ax, (scenario, title) in zip(axes, panels):
        subset = data[data["scenario"] == scenario]
        for short, full in SHORT_TO_FULL.items():
            rows = (
                subset[subset["model"] == short]
                .set_index("condition")
                .loc[CONDITIONS]
            )
            values = rows["pass_rate"].to_numpy(dtype=float)
            positions = np.arange(len(CONDITIONS))
            linestyle, marker, size = styles[full]
            # Draw MiMo behind MiniMax so the overlapping standard-panel
            # markers stay visible as a nested pair.
            zorder = 3 if full.endswith("minimax-m3.1-flash-free") else 4
            ax.plot(
                positions,
                values,
                linestyle=linestyle,
                color=DEEP_ORANGE if "mimo" in full else DEEP_BLUE,
                linewidth=1.8,
                marker=marker,
                markersize=np.sqrt(size),
                markerfacecolor=DEEP_ORANGE if "mimo" in full else DEEP_BLUE,
                markeredgecolor=SURFACE,
                markeredgewidth=1.6,
                label=MODEL_LABELS[full],
                zorder=zorder,
            )
            if scenario == "hard" and "minimax" in full:
                for position, value in zip(positions, values):
                    last = position == len(CONDITIONS) - 1
                    ax.text(
                        position - (0.14 if last else 0.0),
                        value + (0.0 if last else -0.045),
                        f"{value:.2f}",
                        ha="right" if last else "center",
                        va="center" if last else "top",
                        fontsize=7.5,
                        color=TEXT,
                    )
            if scenario == "hard" and "mimo" in full:
                for position, value in zip(positions, values):
                    if value < 1.0:
                        ax.text(
                            position,
                            value + 0.035,
                            f"{value:.2f}",
                            ha="center",
                            va="bottom",
                            fontsize=7.5,
                            color=TEXT,
                        )
        ax.set_xticks(range(len(CONDITIONS)))
        ax.set_xticklabels(
            [LABELS[condition] for condition in CONDITIONS],
            rotation=22,
            ha="right",
        )
        ax.set_ylim(0.45, 1.08)
        ax.set_yticks([0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_title(title)
        clean_axes(ax, "y")
    axes[0].set_ylabel("PassRate")
    axes[0].text(
        0.05,
        0.06,
        "两模型五条件共 120 行全部通过",
        transform=axes[0].transAxes,
        fontsize=8,
        color=MUTED,
    )
    axes[0].legend(
        frameon=False,
        loc="lower left",
        bbox_to_anchor=(0.0, 0.14),
        fontsize=8,
    )
    fig.suptitle("标准题全数通过，条件差异全部由困难题承载", fontsize=11)
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)


def first_round_figure(episodes: pd.DataFrame, output: Path) -> None:
    """First-round pass counts by difficulty and model."""
    units = episodes.drop_duplicates(["model", "task"])
    difficulties = [("标准", "标准题"), ("困难", "困难题")]
    models = [model for model in MODEL_LABELS if model in set(units["model"])]
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    positions = np.arange(len(difficulties))
    width = 0.34
    for index, model in enumerate(models):
        subset = units[units["model"] == model]
        values = [
            int(subset[subset["difficulty"] == key]["round1_passed"].sum())
            for key, _ in difficulties
        ]
        totals = [
            len(subset[subset["difficulty"] == key]) for key, _ in difficulties
        ]
        offsets = positions + (index - (len(models) - 1) / 2) * width
        color = DEEP_ORANGE if "mimo" in model else DEEP_BLUE
        bars = ax.bar(
            offsets,
            values,
            width=width - 0.04,
            color=color,
            edgecolor=SURFACE,
            linewidth=2,
            label=f"{MODEL_LABELS[model]} 合计 {sum(values)}/24",
        )
        for bar, value, total in zip(bars, values, totals):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                value + 0.25,
                f"{value}/{total}",
                ha="center",
                va="bottom",
                fontsize=9,
                color=TEXT,
            )
    ax.set_xticks(positions)
    ax.set_xticklabels([label for _, label in difficulties])
    ax.set_ylim(0, 14)
    ax.set_yticks([0, 3, 6, 9, 12])
    ax.set_ylabel("第一轮通过题数")
    ax.set_title("第一轮通过题数按难度分层")
    clean_axes(ax, "y")
    ax.legend(
        frameon=False,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.12),
        ncol=2,
    )
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)


def pass_rate_figure(results: pd.DataFrame, output: Path) -> None:
    """Full-sample pass rate by condition, one series per model."""
    data = results[results["sample"] == "full"]
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    positions = np.arange(len(CONDITIONS))
    for full in MODEL_LABELS:
        if full not in set(data["model"]):
            continue
        rows = data[data["model"] == full].set_index("condition").loc[CONDITIONS]
        values = rows["pass_rate"].to_numpy(dtype=float)
        color = DEEP_ORANGE if "mimo" in full else DEEP_BLUE
        marker = "s" if "mimo" in full else "o"
        ax.plot(
            positions,
            values,
            color=color,
            linewidth=1.8,
            marker=marker,
            markersize=7,
            markerfacecolor=color,
            markeredgecolor=SURFACE,
            markeredgewidth=1.6,
            label=MODEL_LABELS[full],
        )
        for position, value in zip(positions, values):
            above = "mimo" in full
            last = position == len(CONDITIONS) - 1
            ax.text(
                position + (-0.12 if last and not above else 0.0),
                value + (0.014 if above else (0.010 if last else -0.014)),
                f"{value:.3f}",
                ha="right" if last and not above else "center",
                va="bottom" if above or last else "top",
                fontsize=7.5,
                color=TEXT,
            )
    ax.set_xticks(positions)
    ax.set_xticklabels([LABELS[condition] for condition in CONDITIONS])
    ax.set_ylim(0.75, 1.03)
    ax.set_yticks([0.75, 0.80, 0.85, 0.90, 0.95, 1.00])
    ax.set_ylabel("PassRate")
    ax.set_title("全样本整体通过率，每格 n=24")
    clean_axes(ax, "y")
    ax.legend(
        frameon=False,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.12),
        ncol=2,
    )
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)


def coding_figure(summary: pd.DataFrame, output: Path) -> None:
    """Value distribution of the nine qualitative codes."""
    rows = summary[summary["grouping"] == "overall"]
    codes = list(dict.fromkeys(rows["code"]))
    order = ["是", "否", "不适用"]
    colors = {"是": DEEP_BLUE, "否": NEUTRAL_DARK, "不适用": NEUTRAL_LIGHT}
    counts = (
        rows.pivot_table(
            index="code", columns="value", values="count", aggfunc="sum"
        )
        .reindex(index=codes, columns=order)
        .fillna(0)
        .astype(int)
    )
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    y = np.arange(len(codes))
    left = np.zeros(len(codes))
    for value in order:
        widths = counts[value].to_numpy()
        bars = ax.barh(
            y,
            widths,
            left=left,
            height=0.62,
            color=colors[value],
            edgecolor=SURFACE,
            linewidth=2,
            label=value,
        )
        for bar, width in zip(bars, widths):
            if width >= 4:
                ax.text(
                    bar.get_x() + width / 2,
                    bar.get_y() + bar.get_height() / 2,
                    str(int(width)),
                    ha="center",
                    va="center",
                    fontsize=8,
                    color="white" if value == "是" else TEXT,
                )
        left += widths
    ax.set_yticks(y)
    ax.set_yticklabels(codes)
    ax.invert_yaxis()
    ax.set_xlim(0, 33)
    ax.set_xlabel("episode 数，共三十一条")
    ax.set_title("九项编码的取值分布")
    clean_axes(ax, "x")
    ax.legend(
        frameon=False,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.14),
        ncol=3,
    )
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)


def power_figure(required: pd.DataFrame, output: Path) -> None:
    """Units needed to reach a target risk difference at 80 percent power."""
    fig, ax = plt.subplots(figsize=(8.2, 3.3))
    series = [
        (0.3, DEEP_BLUE, "-", "o"),
        (0.4, DEEP_ORANGE, "-", "s"),
        (0.5, DEEP_AQUA, "-", "D"),
    ]
    for discordance, color, linestyle, marker in series:
        subset = required[required["assumed_discordance"] == discordance].sort_values(
            "target_risk_difference"
        )
        ax.plot(
            subset["target_risk_difference"],
            subset["required_units"],
            linestyle=linestyle,
            color=color,
            linewidth=1.8,
            marker=marker,
            markersize=5.5,
            markeredgecolor=SURFACE,
            markeredgewidth=1.4,
            label=f"不一致比例 {discordance:.1f}",
        )
        last = subset.iloc[-1]
        ax.text(
            last["target_risk_difference"] + 0.006,
            last["required_units"],
            f"{int(last['required_units'])}",
            va="center",
            ha="left",
            fontsize=8,
            color=TEXT,
        )
    for units, note in [(20, "当前二十个单位"), (48, "任务集上限四十八个")]:
        ax.axhline(units, color=MUTED, linewidth=1.0, linestyle=(0, (4, 3)))
        ax.text(
            0.101,
            units * 1.06,
            note,
            fontsize=7.5,
            color=MUTED,
            va="bottom",
        )
    ax.set_yscale("log")
    ax.set_yticks([20, 50, 100, 200, 400])
    ax.set_yticklabels(["20", "50", "100", "200", "400"])
    ax.yaxis.set_minor_formatter(mticker.NullFormatter())
    ax.yaxis.set_minor_locator(mticker.NullLocator())
    ax.set_ylim(15, 520)
    ax.set_xlim(0.096, 0.312)
    ax.set_xticks([0.10, 0.15, 0.20, 0.30])
    ax.set_xticklabels(["0.10", "0.15", "0.20", "0.30"])
    ax.set_xlabel("目标风险差")
    ax.set_ylabel("所需配对单位数，对数刻度")
    ax.set_title("达到百分之八十功效所需的配对单位数")
    clean_axes(ax, "y")
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default=str(ROOT / "RECORD" / "report" / "figures_v1"),
    )
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    setup_style()

    results = pd.read_csv(ROOT / "RECORD" / "analysis" / "main_results.csv")
    episodes = pd.read_csv(ROOT / "RECORD" / "tables" / "episode_level.csv")
    sensitivity = pd.read_csv(ANALYSIS / "sensitivity.csv", encoding="utf-8")
    summary = pd.read_csv(ANALYSIS / "coding_summary.csv", encoding="utf-8")
    required = pd.read_csv(
        ANALYSIS / "power_analysis_required.csv", encoding="utf-8"
    )

    repair_success_figure(results, output / "repair_success.png")
    pass_rate_figure(results, output / "pass_rate.png")
    first_round_figure(episodes, output / "first_round.png")
    difficulty_figure(sensitivity, output / "difficulty_split.png")
    coding_figure(summary, output / "coding_distribution.png")
    power_figure(required, output / "power_required_units.png")
    print(f"wrote six figures to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
