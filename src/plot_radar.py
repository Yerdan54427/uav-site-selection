from math import pi
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from data_utils import DATA_FILE, INDICATORS, add_total_score, load_and_validate_data
from plot_config import configure_matplotlib

OUTPUT_FILE = Path(__file__).resolve().parents[1] / "figures" / "radar_chart.png"

configure_matplotlib()


def create_radar_chart(df, output_file=OUTPUT_FILE):
    """Create and save a radar chart for the top 2 candidates."""
    # Sort by total score and keep the top 2 candidates.
    top_two = df.sort_values(by="total_score", ascending=False).head(2)

    # Create evenly spaced angles for the radar chart.
    angles = [2 * pi * index / len(INDICATORS) for index in range(len(INDICATORS))]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={"polar": True})

    # Draw one polygon for each of the top 2 candidates.
    for _, row in top_two.iterrows():
        values = row[INDICATORS].tolist()
        values += values[:1]  # Repeat the first value to close the polygon.

        ax.plot(angles, values, linewidth=2, label=row["candidate"])
        ax.fill(angles, values, alpha=0.15)

    ax.set_title("Radar Chart of Top 2 UAV Site Candidates", pad=20)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(INDICATORS)
    ax.set_ylim(0, 5)
    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1))

    output_file.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Radar chart saved to: {output_file}")


def main():
    # Read the candidate data from the CSV file and validate it.
    df = load_and_validate_data(DATA_FILE)
    df = add_total_score(df)
    create_radar_chart(df)


if __name__ == "__main__":
    main()
