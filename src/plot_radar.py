from math import pi
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from data_utils import DATA_FILE, INDICATORS, prepare_data, select_best_candidate_pair
from plot_config import (
    COLOR_PALETTE,
    SHORT_DISPLAY_LABELS,
    TITLE_PREFIX,
    configure_matplotlib,
)

OUTPUT_FILE = Path(__file__).resolve().parents[1] / "figures" / "radar_chart.png"

configure_matplotlib()


def create_radar_chart(df, output_file=OUTPUT_FILE, selected_pair=None):
    """Create a radar chart for the recommended two-site combination."""
    if len(df) < 2:
        raise ValueError("雷达图至少需要 2 个候选点才能进行比较。")

    if selected_pair is None:
        selected_pair = select_best_candidate_pair(df)

    selected_candidates = [selected_pair["candidate_a"], selected_pair["candidate_b"]]
    pair_df = df.set_index("candidate").loc[selected_candidates].reset_index()

    angles = [2 * pi * index / len(INDICATORS) for index in range(len(INDICATORS))]
    angles += angles[:1]
    display_labels = [SHORT_DISPLAY_LABELS[column] for column in INDICATORS]
    line_colors = [COLOR_PALETTE["primary"], COLOR_PALETTE["accent"]]

    fig, ax = plt.subplots(figsize=(7.4, 7.4), subplot_kw={"polar": True})

    for color, (_, row) in zip(line_colors, pair_df.iterrows()):
        values = row[INDICATORS].tolist()
        values += values[:1]

        ax.plot(angles, values, linewidth=2.4, color=color, label=row["candidate"])
        ax.fill(angles, values, color=color, alpha=0.14)

    ax.set_title(f"{TITLE_PREFIX}推荐双点组合雷达图", pad=22, fontsize=14, fontweight="bold")
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(display_labels)
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["1", "2", "3", "4", "5"], color="#6b7c93")
    ax.grid(color=COLOR_PALETTE["grid"], linewidth=0.9)
    ax.spines["polar"].set_color(COLOR_PALETTE["grid"])
    ax.legend(loc="upper right", bbox_to_anchor=(1.12, 1.10), frameon=False)

    fig.text(
        0.5,
        0.02,
        (
            f"两点间距：{selected_pair['distance_m']:.0f} m    "
            f"间距修正：{selected_pair['spacing_adjustment']:+.2f}    "
            f"组合总分：{selected_pair['pair_score']:.2f}"
        ),
        ha="center",
        color=COLOR_PALETTE["text"],
    )

    output_file.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(output_file, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    print(f"Radar chart saved to: {output_file}")


def main():
    df = prepare_data(DATA_FILE)
    create_radar_chart(df)


if __name__ == "__main__":
    main()
