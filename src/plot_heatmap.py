from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from data_utils import DATA_FILE, load_and_validate_data
from plot_config import configure_matplotlib


OUTPUT_FILE = Path(__file__).resolve().parents[1] / "figures" / "heatmap.png"

configure_matplotlib()


def create_heatmap(df, output_file=OUTPUT_FILE):
    """Create and save a heatmap from the score columns."""
    # Keep only the score columns and use candidate names as row labels.
    score_columns = [column for column in df.columns if column not in ["candidate", "total_score"]]
    heatmap_data = df.set_index("candidate")[score_columns]

    # Create the heatmap figure.
    fig, ax = plt.subplots(figsize=(10, 5))
    image = ax.imshow(heatmap_data.values, cmap="YlGnBu", aspect="auto")

    # Set axis labels.
    ax.set_title("Campus UAV Site Selection Heatmap")
    ax.set_xticks(range(len(heatmap_data.columns)))
    ax.set_xticklabels(heatmap_data.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(heatmap_data.index)))
    ax.set_yticklabels(heatmap_data.index)

    # Show the numeric score inside each cell.
    for row_index in range(len(heatmap_data.index)):
        for column_index in range(len(heatmap_data.columns)):
            score = heatmap_data.iloc[row_index, column_index]
            ax.text(column_index, row_index, score, ha="center", va="center", color="black")

    # Add a colorbar to explain the colors.
    fig.colorbar(image, ax=ax, label="Score")

    output_file.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Heatmap saved to: {output_file}")


def main():
    # Read the CSV file, validate it, and generate the heatmap.
    df = load_and_validate_data(DATA_FILE)
    create_heatmap(df)


if __name__ == "__main__":
    main()
