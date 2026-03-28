from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from data_utils import DATA_FILE, prepare_data
from plot_config import COLOR_PALETTE, TITLE_PREFIX, configure_matplotlib


OUTPUT_FILE = Path(__file__).resolve().parents[1] / "figures" / "bar_chart.png"

configure_matplotlib()


def create_bar_chart(df, output_file=OUTPUT_FILE):
    """Create and save a bar chart from candidate total scores."""
    # Sort candidates from highest score to lowest score.
    df = df.sort_values(by="total_score", ascending=False).reset_index(drop=True)

    # Create the bar chart.
    fig, ax = plt.subplots(figsize=(8.6, 5.2))
    bars = ax.bar(
        df["candidate"],
        df["total_score"],
        color=COLOR_PALETTE["primary"],
        edgecolor=COLOR_PALETTE["secondary"],
        linewidth=1.2,
    )

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
