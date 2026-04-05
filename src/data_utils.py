from itertools import combinations
from pathlib import Path

import pandas as pd


DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "candidate_scores.csv"
PAIR_DISTANCE_FILE = Path(__file__).resolve().parents[1] / "data" / "candidate_pair_distances.csv"

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

PAIR_DISTANCE_COLUMNS = ["candidate_a", "candidate_b", "distance_m"]
PAIR_SPACING_WEIGHT = 0.35
PAIR_SPACING_SCORE_BREAKPOINTS = [
    (150, 1),
    (300, 2),
    (500, 3),
    (700, 4),
    (float("inf"), 5),
]


def load_and_validate_data(csv_path=DATA_FILE):
    """Read the single-candidate scoring table and validate score ranges."""
    df = pd.read_csv(csv_path)

    if "candidate" not in df.columns:
        raise ValueError("CSV 文件缺少必需的 candidate 列。")

    missing_columns = [column for column in INDICATORS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"CSV 文件缺少必需的评分列：{', '.join(missing_columns)}")

    for column in INDICATORS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

        invalid_rows = df[df[column].isna()]["candidate"].tolist()
        if invalid_rows:
            raise ValueError(
                f"评分列 '{column}' 存在非数字数据，对应候选点为：{', '.join(invalid_rows)}"
            )

        out_of_range_rows = df[(df[column] < 1) | (df[column] > 5)]["candidate"].tolist()
        if out_of_range_rows:
            raise ValueError(
                f"评分列 '{column}' 的分值必须在 1 到 5 之间，异常候选点为："
                f"{', '.join(out_of_range_rows)}"
            )

    return df


def add_total_score(df):
    """Add weighted single-candidate scores and sort descending."""
    result = df.copy()
    result["total_score"] = sum(result[column] * weight for column, weight in WEIGHTS.items())
    result["total_score"] = result["total_score"].round(2)
    return result.sort_values(by="total_score", ascending=False).reset_index(drop=True)


def prepare_data(csv_path=DATA_FILE):
    """Read, validate, and score the single-candidate table."""
    df = load_and_validate_data(csv_path)
    return add_total_score(df)


def pair_spacing_score(distance_m):
    """Convert pairwise distance in meters into a 1-5 spacing score."""
    for upper_bound, score in PAIR_SPACING_SCORE_BREAKPOINTS:
        if distance_m <= upper_bound:
            return score

    raise ValueError(f"无法为距离 {distance_m} 计算间距评分。")


def pair_spacing_adjustment(spacing_score):
    """Map the spacing score to a centered reward/penalty adjustment."""
    return round((spacing_score - 3) * PAIR_SPACING_WEIGHT, 2)


def _normalize_pair(candidate_a, candidate_b):
    return tuple(sorted((candidate_a, candidate_b)))


def load_and_validate_pair_distances(candidates, csv_path=PAIR_DISTANCE_FILE):
    """Read the pairwise distance table and verify coverage for all pairs."""
    pair_df = pd.read_csv(csv_path)

    missing_columns = [column for column in PAIR_DISTANCE_COLUMNS if column not in pair_df.columns]
    if missing_columns:
        raise ValueError(f"组合距离文件缺少必需列：{', '.join(missing_columns)}")

    pair_df["distance_m"] = pd.to_numeric(pair_df["distance_m"], errors="coerce")
    invalid_rows = pair_df[pair_df["distance_m"].isna()]
    if not invalid_rows.empty:
        raise ValueError("组合距离文件存在非数字距离值。")

    non_positive_rows = pair_df[pair_df["distance_m"] <= 0]
    if not non_positive_rows.empty:
        raise ValueError("组合距离文件中的距离必须大于 0。")

    valid_candidates = set(candidates)
    referenced_candidates = set(pair_df["candidate_a"]) | set(pair_df["candidate_b"])
    invalid_candidates = sorted(referenced_candidates - valid_candidates)
    if invalid_candidates:
        raise ValueError(
            "组合距离文件存在未出现在候选点评分表中的候选点："
            f"{', '.join(invalid_candidates)}"
        )

    same_point_rows = pair_df[pair_df["candidate_a"] == pair_df["candidate_b"]]
    if not same_point_rows.empty:
        raise ValueError("组合距离文件不允许同一个候选点和自己组成一对。")

    pair_df["pair_key"] = pair_df.apply(
        lambda row: _normalize_pair(row["candidate_a"], row["candidate_b"]),
        axis=1,
    )

    duplicate_keys = pair_df[pair_df["pair_key"].duplicated()]["pair_key"].tolist()
    if duplicate_keys:
        duplicate_labels = [" + ".join(pair_key) for pair_key in duplicate_keys]
        raise ValueError(f"组合距离文件存在重复组合：{', '.join(duplicate_labels)}")

    expected_pairs = {_normalize_pair(*pair) for pair in combinations(candidates, 2)}
    provided_pairs = set(pair_df["pair_key"])

    missing_pairs = sorted(expected_pairs - provided_pairs)
    if missing_pairs:
        missing_labels = [" + ".join(pair_key) for pair_key in missing_pairs]
        raise ValueError(f"组合距离文件缺少候选点组合：{', '.join(missing_labels)}")

    extra_pairs = sorted(provided_pairs - expected_pairs)
    if extra_pairs:
        extra_labels = [" + ".join(pair_key) for pair_key in extra_pairs]
        raise ValueError(f"组合距离文件包含多余组合：{', '.join(extra_labels)}")

    pair_df["spacing_score"] = pair_df["distance_m"].map(pair_spacing_score)
    pair_df["spacing_adjustment"] = pair_df["spacing_score"].map(pair_spacing_adjustment)
    return pair_df


def rank_candidate_pairs(df, pair_distance_path=PAIR_DISTANCE_FILE):
    """Score every candidate pair and rank them from best to worst."""
    pair_df = load_and_validate_pair_distances(df["candidate"].tolist(), pair_distance_path).copy()
    score_lookup = df.set_index("candidate")["total_score"]

    pair_df["candidate_a_score"] = pair_df["candidate_a"].map(score_lookup)
    pair_df["candidate_b_score"] = pair_df["candidate_b"].map(score_lookup)
    pair_df["base_pair_score"] = (
        pair_df["candidate_a_score"] + pair_df["candidate_b_score"]
    ).round(2)
    pair_df["pair_score"] = (
        pair_df["base_pair_score"] + pair_df["spacing_adjustment"]
    ).round(2)
    pair_df["pair_name"] = pair_df["candidate_a"] + " + " + pair_df["candidate_b"]

    return pair_df.sort_values(
        by=["pair_score", "base_pair_score", "distance_m"],
        ascending=[False, False, False],
    ).reset_index(drop=True)


def select_best_candidate_pair(df, pair_distance_path=PAIR_DISTANCE_FILE):
    """Return the highest-ranked candidate pair with spacing adjustment."""
    ranked_pairs = rank_candidate_pairs(df, pair_distance_path=pair_distance_path)
    return ranked_pairs.iloc[0]
