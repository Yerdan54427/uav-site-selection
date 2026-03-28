from pathlib import Path

import pandas as pd


# DATA_FILE 指向整个项目默认使用的输入 CSV 文件。
DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "candidate_scores.csv"

# INDICATORS 同时定义了：
# 1. CSV 中必须存在的评分列
# 2. 后续图表中指标的固定显示顺序
# 把它们集中写在这里可以避免前后不一致。
INDICATORS = [
    "service_distance",
    "logistics_distance",
    "openness",
    "obstacle_risk",
    "crowd_risk",
    "route_access",
    "operation_convenience",
]

# WEIGHTS 保存整个项目统一使用的权重模型。
# 这里的键名必须与 CSV 中的指标列名完全一致。
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
    """读取 CSV 文件，并校验所有评分是否为 1 到 5 的数字。"""
    # 按原始内容读取 CSV 数据。
    df = pd.read_csv(csv_path)

    # candidate 列是必须的，因为终端排名和所有图表都要用它来显示候选点名称。
    if "candidate" not in df.columns:
        raise ValueError("CSV file is missing the required 'candidate' column.")

    # 检查是否缺少任何一个必需的评分指标列。
    missing_columns = [column for column in INDICATORS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"CSV file is missing required columns: {', '.join(missing_columns)}")

    for column in INDICATORS:
        # 把每个评分列都转换成数值。
        # 如果出现无法转换的文本，pandas 会把它变成 NaN，
        # 这样后面就能很方便地识别异常数据。
        df[column] = pd.to_numeric(df[column], errors="coerce")

        # 如果某些值无法转换为数字，就把对应候选点名字报出来，
        # 方便快速定位并修改 CSV。
        invalid_rows = df[df[column].isna()]["candidate"].tolist()
        if invalid_rows:
            raise ValueError(
                f"Column '{column}' contains non-numeric values for: {', '.join(invalid_rows)}"
            )

        # 本项目严格使用 1 到 5 的评分体系。
        # 如果数值超出范围，就直接报错停止，避免后续结果被异常值干扰。
        out_of_range_rows = df[(df[column] < 1) | (df[column] > 5)]["candidate"].tolist()
        if out_of_range_rows:
            raise ValueError(
                f"Column '{column}' must contain scores from 1 to 5. Invalid candidates: "
                f"{', '.join(out_of_range_rows)}"
            )

    return df


def add_total_score(df):
    """添加加权总分列，并返回按总分降序排序后的副本。"""
    # 先复制一份数据，避免直接修改原始 DataFrame，
    # 这样更安全，也更方便在其他地方重复使用原数据。
    result = df.copy()

    # 把每个指标分数乘以对应权重，再逐行求和，
    # 就得到每个候选点的最终加权总分。
    result["total_score"] = sum(result[column] * weight for column, weight in WEIGHTS.items())

    # 最终得分统一保留两位小数，既方便展示，也足够用于排序比较。
    result["total_score"] = result["total_score"].round(2)

    # 返回按总分从高到低排序后的结果。
    return result.sort_values(by="total_score", ascending=False).reset_index(drop=True)


def prepare_data(csv_path=DATA_FILE):
    """一次性完成数据读取、校验和总分计算。"""
    # 这个辅助函数把公共的数据预处理步骤打包起来，
    # 这样 main.py 和各个绘图脚本都可以直接复用。
    df = load_and_validate_data(csv_path)
    return add_total_score(df)
