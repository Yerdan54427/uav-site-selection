from math import pi
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_radar(score_data, output_path):
    """Create and save a radar chart for the top 2 candidates."""
    top_two = score_data.head(2)
    categories = list(top_two.columns)
    angles = [2 * pi * index / len(categories) for index in range(len(categories))]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={"polar": True})

    for candidate_name, row in top_two.iterrows():
        values = row.tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=2, label=candidate_name)
        ax.fill(angles, values, alpha=0.15)

    ax.set_title("Radar Chart for Top 2 Candidates", pad=20)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_ylim(0, 10)
    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1))

    fig.tight_layout()

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
