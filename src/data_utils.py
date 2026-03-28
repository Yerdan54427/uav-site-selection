from pathlib import Path

import pandas as pd


DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "candidate_scores.csv"

INDICATORS = [
    "service_distance",
    "logistics_distance",
    "openness",
    "obstacle_risk",
    "crowd_risk",
    "route_access",
    "operation_convenience",
]

WEIGHTS = {
    "service_distance": 0.15,
    "logistics_distance": 0.15,
    "openness": 0.20,
    "obstacle_risk": 0.15,
    "crowd_risk": 0.15,
    "route_access": 0.10,
    "operation_convenience": 0.10,
}


def load_and_validate_data(csv_path=DATA_FILE):
    """Read the CSV file and validate that all scores are numeric values from 1 to 5."""
    df = pd.read_csv(csv_path)

    if "candidate" not in df.columns:
        raise ValueError("CSV file is missing the required 'candidate' column.")

    missing_columns = [column for column in INDICATORS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"CSV file is missing required columns: {', '.join(missing_columns)}")

    for column in INDICATORS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

        invalid_rows = df[df[column].isna()]["candidate"].tolist()
        if invalid_rows:
            raise ValueError(
                f"Column '{column}' contains non-numeric values for: {', '.join(invalid_rows)}"
            )

        out_of_range_rows = df[(df[column] < 1) | (df[column] > 5)]["candidate"].tolist()
        if out_of_range_rows:
            raise ValueError(
                f"Column '{column}' must contain scores from 1 to 5. Invalid candidates: "
                f"{', '.join(out_of_range_rows)}"
            )

    return df


def add_total_score(df):
    """Add a weighted total score column and return a sorted copy."""
    result = df.copy()
    result["total_score"] = sum(result[column] * weight for column, weight in WEIGHTS.items())
    result["total_score"] = result["total_score"].round(2)
    return result.sort_values(by="total_score", ascending=False).reset_index(drop=True)
