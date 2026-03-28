from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "candidate_scores.csv"
OUTPUT_FILE = Path(__file__).resolve().parents[1] / "figures" / "heatmap.png"


def main():
    # Read the CSV file.
    df = pd.read_csv(DATA_FILE)

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

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUTPUT_FILE, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Heatmap saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
