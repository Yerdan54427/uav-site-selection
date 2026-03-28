from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from data_utils import DATA_FILE, INDICATORS, load_and_validate_data
from plot_config import COLOR_PALETTE, DISPLAY_LABELS, TITLE_PREFIX, configure_matplotlib


OUTPUT_FILE = Path(__file__).resolve().parents[1] / "figures" / "heatmap.png"

configure_matplotlib()


def create_heatmap(df, output_file=OUTPUT_FILE):
    """Create and save a heatmap from the score columns."""
    # Use the defined evaluation indicators in a fixed order.
    heatmap_data = df.set_index("candidate")[INDICATORS]
    display_labels = [DISPLAY_LABELS[column] for column in INDICATORS]

    # Create the heatmap figure.
    fig, ax = plt.subplots(figsize=(10.5, 5.4))
    image = ax.imshow(heatmap_data.values, cmap="GnBu", aspect="auto", vmin=1, vmax=5)

    # Set axis labels.
    ax.set_title(f"{TITLE_PREFIX}评分热力图", pad=14, fontsize=14, fontweight="bold")
    ax.set_xticks(range(len(heatmap_data.columns)))
    ax.set_xticklabels(display_labels, rotation=28, ha="right")
    ax.set_yticks(range(len(heatmap_data.index)))
    ax.set_yticklabels(heatmap_data.index)
    ax.tick_params(length=0)

    # Show the numeric score inside each cell.
    for row_index in range(len(heatmap_data.index)):
        for column_index in range(len(heatmap_data.columns)):
            score = heatmap_data.iloc[row_index, column_index]
            text_color = "white" if image.norm(score) > 0.55 else COLOR_PALETTE["text"]
            ax.text(
                column_index,
                row_index,
                score,
                ha="center",
                va="center",
                color=text_color,
                fontweight="bold",
            )

    # Add a colorbar to explain the colors.
    colorbar = fig.colorbar(image, ax=ax, label="评分")
    colorbar.outline.set_edgecolor(COLOR_PALETTE["grid"])

    for spine in ax.spines.values():
        spine.set_visible(False)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_file, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    print(f"Heatmap saved to: {output_file}")


def main():
    # Read the CSV file, validate it, and generate the heatmap.
    df = load_and_validate_data(DATA_FILE)
    create_heatmap(df)


if __name__ == "__main__":
    main()
