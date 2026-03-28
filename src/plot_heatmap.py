from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_heatmap(score_data, output_path):
    """Create and save a heatmap of candidate scores."""
    fig, ax = plt.subplots(figsize=(9, 4.5))
    image = ax.imshow(score_data.values, cmap="YlGnBu", aspect="auto")

    ax.set_title("UAV Site Candidate Score Heatmap")
    ax.set_xticks(range(len(score_data.columns)))
    ax.set_xticklabels(score_data.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(score_data.index)))
    ax.set_yticklabels(score_data.index)

    for row_index in range(len(score_data.index)):
        for column_index in range(len(score_data.columns)):
            ax.text(
                column_index,
                row_index,
                score_data.iloc[row_index, column_index],
                ha="center",
                va="center",
                color="black",
            )

    fig.colorbar(image, ax=ax, label="Score")
    fig.tight_layout()

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
