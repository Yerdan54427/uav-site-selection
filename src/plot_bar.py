from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from data_utils import DATA_FILE, prepare_data
from plot_config import COLOR_PALETTE, TITLE_PREFIX, configure_matplotlib


OUTPUT_FILE = Path(__file__).resolve().parents[1] / "figures" / "bar_chart.png"

# 在创建图形之前，先应用统一的字体和颜色设置。
configure_matplotlib()


def create_bar_chart(df, output_file=OUTPUT_FILE):
    """根据候选点总分生成柱状图并保存到文件。"""
    # 这里再次排序，是为了保证这个函数在单独调用时也能稳定输出降序结果。
    df = df.sort_values(by="total_score", ascending=False).reset_index(drop=True)

    # 使用统一配色创建柱状图。
    fig, ax = plt.subplots(figsize=(8.6, 5.2))
    bars = ax.bar(
        df["candidate"],
        df["total_score"],
        color=COLOR_PALETTE["primary"],
        edgecolor=COLOR_PALETTE["secondary"],
        linewidth=1.2,
    )

    # 给柱子顶部预留一点空间，避免分数文字贴得太近。
    ax.set_title(f"{TITLE_PREFIX}综合评分柱状图", pad=14, fontsize=14, fontweight="bold")
    ax.set_xlabel("候选点")
    ax.set_ylabel("加权总分")
    ax.grid(axis="y", linestyle="--", linewidth=0.8, color=COLOR_PALETTE["grid"], alpha=0.9)
    ax.set_axisbelow(True)
    ax.set_ylim(0, max(df["total_score"]) + 0.6)

    # Show the score above each bar.
    for bar, score in zip(bars, df["total_score"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.08,
            f"{score:.2f}",
            ha="center",
            va="bottom",
            fontweight="bold",
            color=COLOR_PALETTE["text"],
        )

    # 去掉不必要的边框线，让注意力集中在柱子和数值上。
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_file, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    print(f"Bar chart saved to: {output_file}")


def main():
    # Read, validate, score, and sort the candidate data.
    df = prepare_data(DATA_FILE)
    create_bar_chart(df)


if __name__ == "__main__":
    main()
