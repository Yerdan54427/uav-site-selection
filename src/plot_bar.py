from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_bar(total_scores, output_path):
    """Create and save a bar chart of weighted total scores."""
    sorted_scores = total_scores.sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(sorted_scores.index, sorted_scores.values, color="steelblue")

    ax.set_title("Weighted Total Score by Candidate")
    ax.set_xlabel("Candidate")
    ax.set_ylabel("Weighted Total Score")
    ax.set_xticks(range(len(sorted_scores.index)))
    ax.set_xticklabels(sorted_scores.index, rotation=30, ha="right")

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.05,
            f"{height:.2f}",
            ha="center",
            va="bottom",
        )

    fig.tight_layout()

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
