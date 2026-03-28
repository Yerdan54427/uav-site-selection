from math import pi
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from data_utils import DATA_FILE, INDICATORS, prepare_data
from plot_config import (
    COLOR_PALETTE,
    SHORT_DISPLAY_LABELS,
    TITLE_PREFIX,
    configure_matplotlib,
)

OUTPUT_FILE = Path(__file__).resolve().parents[1] / "figures" / "radar_chart.png"

# 在创建图形之前，先应用统一的字体和颜色设置。
configure_matplotlib()


def create_radar_chart(df, output_file=OUTPUT_FILE):
    """根据前两名候选点生成雷达图并保存到文件。"""
    # 雷达图用于比较，因此至少要有两个候选点才有意义。
    if len(df) < 2:
        raise ValueError("雷达图至少需要 2 个候选点才能进行比较。")

    # 只取总分最高的前两名进行对比。
    top_two = df.sort_values(by="total_score", ascending=False).head(2)

    # 每个指标对应一个角度。
    # 最后把第一个角度再补一次，才能把雷达图多边形首尾闭合。
    angles = [2 * pi * index / len(INDICATORS) for index in range(len(INDICATORS))]
    angles += angles[:1]
    display_labels = [SHORT_DISPLAY_LABELS[column] for column in INDICATORS]
    line_colors = [COLOR_PALETTE["primary"], COLOR_PALETTE["accent"]]

    fig, ax = plt.subplots(figsize=(7.4, 7.2), subplot_kw={"polar": True})

    # Draw one polygon for each of the top 2 candidates.
    for color, (_, row) in zip(line_colors, top_two.iterrows()):
        values = row[INDICATORS].tolist()
        values += values[:1]  # Repeat the first value to close the polygon.

        ax.plot(angles, values, linewidth=2.4, color=color, label=row["candidate"])
        ax.fill(angles, values, color=color, alpha=0.14)

    # 使用较短的中文标签，避免雷达图一圈文字太拥挤。
    ax.set_title(f"{TITLE_PREFIX}前两名候选点雷达图", pad=22, fontsize=14, fontweight="bold")
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(display_labels)
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["1", "2", "3", "4", "5"], color="#6b7c93")
    ax.grid(color=COLOR_PALETTE["grid"], linewidth=0.9)
    ax.spines["polar"].set_color(COLOR_PALETTE["grid"])

    # 把图例放得稍微靠近一些，让它更像图表整体的一部分。
    ax.legend(loc="upper right", bbox_to_anchor=(1.12, 1.10), frameon=False)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_file, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    print(f"Radar chart saved to: {output_file}")


def main():
    # Read, validate, score, and sort the candidate data.
    df = prepare_data(DATA_FILE)
    create_radar_chart(df)


if __name__ == "__main__":
    main()
