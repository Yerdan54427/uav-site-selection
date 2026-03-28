from pathlib import Path

import pandas as pd


DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "candidate_scores.csv"

# Weights for each evaluation factor.
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
    # Read the candidate score data from the CSV file.
    df = pd.read_csv(DATA_FILE)

    # Multiply each score column by its weight and sum the results.
    weighted_scores = sum(df[column] * weight for column, weight in WEIGHTS.items())

    # Add the total score column and sort from highest to lowest.
    df["total_score"] = weighted_scores.round(2)
    df = df.sort_values(by="total_score", ascending=False).reset_index(drop=True)

    # Print the final ranking to the terminal.
    print("Campus UAV Site Selection Ranking")
    print(df[["candidate", "total_score"]].to_string(index=False))


if __name__ == "__main__":
    main()
