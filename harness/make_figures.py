#!/usr/bin/env python3
"""Render report figures from the aggregated episode table.

Static PNG figures use the light categorical slots 1 and 2 from the reference
palette. The two model hues were checked with the palette validator in light
mode. Figures avoid dual axes and keep direct labels on every bar.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CONDITIONS = [
    "pure_continue",
    "neutral",
    "method_guidance",
    "negative",
    "negative_guidance",
]
LABELS = {
    "pure_continue": "纯继续",
    "neutral": "中性",
    "method_guidance": "方法指引",
    "negative": "负面",
    "negative_guidance": "负面加指导",
}
MODEL_LABELS = {
    "opencode/minimax-m3.1-flash-free": "MiniMax",
    "opencode/mimo-v2.6-flash-free": "MiMo",
}
COLORS = {
    "opencode/minimax-m3.1-flash-free": "#2a78d6",
    "opencode/mimo-v2.6-flash-free": "#eb6834",
}
SURFACE = "#fcfcfb"
TEXT = "#0b0b0b"
MUTED = "#52514e"
GRID = "#dedcd5"


def setup_style() -> None:
    plt.rcParams.update(
        {
            "font.sans-serif": [
                "Microsoft YaHei",
                "SimHei",
                "Noto Sans CJK SC",
                "DejaVu Sans",
            ],
            "axes.unicode_minus": False,
            "figure.facecolor": SURFACE,
            "axes.facecolor": SURFACE,
            "savefig.facecolor": SURFACE,
            "axes.edgecolor": GRID,
            "axes.labelcolor": TEXT,
            "text.color": TEXT,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "axes.titlesize": 11,
            "axes.labelsize": 10,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "legend.fontsize": 9,
        }
    )


def clean_axes(ax: plt.Axes, axis: str = "x") -> None:
    for side in ("top", "right", "left" if axis == "x" else "bottom"):
        ax.spines[side].set_visible(False)
    ax.grid(axis=axis, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def repair_success_figure(results: pd.DataFrame, output: Path) -> None:
    branch = results[results["sample"] == "branch"]
    models = [
        model for model in MODEL_LABELS if model in set(branch["model"])
    ]
    y = np.arange(len(CONDITIONS))
    height = 0.34
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    for index, model in enumerate(models):
        subset = branch[branch["model"] == model].set_index("condition")
        values = [subset.loc[condition, "repair_success"] for condition in CONDITIONS]
        offsets = y + (index - (len(models) - 1) / 2) * height
        bars = ax.barh(
            offsets,
            values,
            height=height - 0.04,
            color=COLORS[model],
            label=f"{MODEL_LABELS[model]} n={int(subset['n'].iloc[0])}",
            edgecolor=SURFACE,
            linewidth=2,
        )
        for bar, value in zip(bars, values):
            ax.text(
                min(value + 0.02, 1.03),
                bar.get_y() + bar.get_height() / 2,
                f"{value:.3f}",
                va="center",
                ha="left",
                fontsize=8,
                color=TEXT,
            )
    ax.set_yticks(y)
    ax.set_yticklabels([LABELS[condition] for condition in CONDITIONS])
    ax.invert_yaxis()
    ax.set_xlim(0, 1.12)
    ax.set_xlabel("RepairSuccess")
    ax.set_title("第一轮失败任务的分支修复成功率")
    clean_axes(ax, "x")
    ax.legend(
        frameon=False,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.2),
        ncol=2,
    )
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)


def edit_size_figure(episodes: pd.DataFrame, output: Path) -> None:
    branch = episodes[
        (episodes["valid"] == True)  # noqa: E712
        & (episodes["round1_passed"] == False)  # noqa: E712
    ]
    models = [
        model for model in MODEL_LABELS if model in set(branch["model"])
    ]
    fig, axes = plt.subplots(
        1, len(models), figsize=(8.0, 3.8), sharey=True
    )
    if len(models) == 1:
        axes = [axes]
    for ax, model in zip(axes, models):
        subset = branch[branch["model"] == model]
        for position, condition in enumerate(CONDITIONS):
            values = subset[subset["condition"] == condition]["edit_lines"].dropna()
            jitter = (
                np.linspace(-0.16, 0.16, len(values))
                if len(values) > 1
                else np.zeros(len(values))
            )
            ax.scatter(
                position + jitter,
                values,
                s=26,
                color=COLORS[model],
                alpha=0.75,
                edgecolor=SURFACE,
                linewidth=0.8,
                zorder=3,
            )
            median = float(values.median()) if len(values) else 0.0
            ax.plot(
                [position - 0.22, position + 0.22],
                [median, median],
                color=TEXT,
                linewidth=1.6,
                zorder=4,
            )
            ax.text(
                position + 0.24,
                median,
                f"{median:.1f}",
                va="center",
                ha="left",
                fontsize=8,
                color=MUTED,
            )
        ax.set_xticks(range(len(CONDITIONS)))
        ax.set_xticklabels(
            [LABELS[condition] for condition in CONDITIONS],
            rotation=25,
            ha="right",
        )
        ax.set_title(MODEL_LABELS[model])
        ax.set_xlim(-0.5, len(CONDITIONS) - 0.3)
        ax.set_yscale("symlog", linthresh=2, linscale=0.8)
        ax.set_yticks([0, 2, 4, 7, 12, 20, 40])
        ax.set_yticklabels(["0", "2", "4", "7", "12", "20", "40"])
        ax.set_ylim(0, 44)
        clean_axes(ax, "y")
    axes[0].set_ylabel("EditSize 行数，对数刻度")
    fig.suptitle("分支子集 EditSize 分布与中位数", fontsize=11)
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--results",
        default=str(ROOT / "RECORD" / "analysis" / "main_results.csv"),
    )
    parser.add_argument(
        "--episodes",
        default=str(ROOT / "RECORD" / "tables" / "episode_level.csv"),
    )
    parser.add_argument(
        "--output",
        default=str(ROOT / "RECORD" / "analysis" / "figures"),
    )
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    setup_style()
    results = pd.read_csv(args.results)
    episodes = pd.read_csv(args.episodes)
    repair_success_figure(results, output / "repair_success.png")
    edit_size_figure(episodes, output / "edit_size.png")
    print(f"wrote {output / 'repair_success.png'} and {output / 'edit_size.png'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
