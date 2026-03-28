from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from data_utils import DATA_FILE, add_total_score, load_and_validate_data


OUTPUT_FILE = Path(__file__).resolve().parents[1] / "figures" / "bar_chart.png"


def create_bar_chart(df, output_file=OUTPUT_FILE):
    """Create and save a bar chart from candidate total scores."""
    # Sort candidates from highest score to lowest score.
    df = df.sort_values(by="total_score", ascending=False).reset_index(drop=True)

    # Create the bar chart.
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(df["candidate"], df["total_score"], color="steelblue")

    ax.set_title("Campus UAV Site Selection Ranking")
    ax.set_xlabel("Candidate Sites")
    ax.set_ylabel("Total Weighted Score")

    # Show the score above each bar.
    for bar, score in zip(bars, df["total_score"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.03,
            f"{score:.2f}",
            ha="center",
            va="bottom",
        )

    output_file.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Bar chart saved to: {output_file}")


def main():
    # Read the candidate data from the CSV file and validate it.
    df = load_and_validate_data(DATA_FILE)
    df = add_total_score(df)
    create_bar_chart(df)


if __name__ == "__main__":
    main()
