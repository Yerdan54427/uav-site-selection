from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "candidate_scores.csv"
OUTPUT_FILE = Path(__file__).resolve().parents[1] / "figures" / "bar_chart.png"

WEIGHTS = {
    "dorm_distance": 0.15,
    "logistics_distance": 0.15,
    "openness": 0.20,
    "obstacle_risk": 0.15,
    "crowd_risk": 0.15,
    "route_access": 0.10,
    "operation_convenience": 0.10,
}


def main():
    # Read the candidate data from the CSV file.
    df = pd.read_csv(DATA_FILE)

    # Compute the weighted total score for each candidate.
    df["total_score"] = sum(df[column] * weight for column, weight in WEIGHTS.items())

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

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUTPUT_FILE, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Bar chart saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
