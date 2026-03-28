from pathlib import Path

import pandas as pd

from plot_bar import plot_bar
from plot_heatmap import plot_heatmap
from plot_radar import plot_radar


DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "candidate_scores.csv"
FIGURES_DIR = Path(__file__).resolve().parents[1] / "figures"

# Simple weights for each evaluation criterion.
WEIGHTS = {
    "safety": 0.30,
    "accessibility": 0.20,
    "open_space": 0.20,
    "obstacle_clearance": 0.20,
    "noise_impact": 0.10,
}


def load_data(csv_path):
    """Load the candidate score dataset from a CSV file."""
    df = pd.read_csv(csv_path)
    df = df.set_index("candidate")
    return df


def calculate_weighted_scores(score_data, weights):
    """Calculate the weighted total score for each candidate."""
    weight_series = pd.Series(weights)
    return score_data.mul(weight_series, axis=1).sum(axis=1)


def main():
    score_data = load_data(DATA_FILE)
    weighted_scores = calculate_weighted_scores(score_data, WEIGHTS)
    ranked_data = score_data.loc[weighted_scores.sort_values(ascending=False).index]

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    plot_heatmap(score_data, FIGURES_DIR / "score_heatmap.png")
    plot_bar(weighted_scores, FIGURES_DIR / "weighted_total_scores.png")
    plot_radar(ranked_data, FIGURES_DIR / "top_2_radar_chart.png")

    print("Figures saved to:")
    print(FIGURES_DIR / "score_heatmap.png")
    print(FIGURES_DIR / "weighted_total_scores.png")
    print(FIGURES_DIR / "top_2_radar_chart.png")


if __name__ == "__main__":
    main()
