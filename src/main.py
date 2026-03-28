from pathlib import Path

from plot_bar import create_bar_chart
from plot_heatmap import create_heatmap
from plot_radar import create_radar_chart
from data_utils import DATA_FILE, prepare_data


# 所有生成的图像都统一保存到项目根目录下的 figures 文件夹中。
FIGURES_DIR = Path(__file__).resolve().parents[1] / "figures"


def main():
    # prepare_data() 会一次性完成完整的数据预处理流程：
    # 1. 读取 CSV 文件
    # 2. 校验必需列和分数范围
    # 3. 计算加权总分
    # 4. 按总分从高到低排序
    df = prepare_data(DATA_FILE)

    # 为了让终端输出更直观，这里把总分格式化为保留两位小数。
    # 注意这里只是为了显示方便，不会影响后面绘图继续使用数值列。
    ranking_display = df[["candidate", "total_score"]].copy()
    ranking_display["total_score"] = ranking_display["total_score"].map(lambda score: f"{score:.2f}")

    print("Campus UAV Site Selection Ranking")
    print(ranking_display.to_string(index=False))

    # 在保存图表之前，先确保输出目录已经存在。
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    # 三张图都复用同一份已经校验和排序后的数据，
    # 这样可以保证所有图表基于完全一致的结果生成。
    create_heatmap(df, FIGURES_DIR / "heatmap.png")
    create_bar_chart(df, FIGURES_DIR / "bar_chart.png")
    create_radar_chart(df, FIGURES_DIR / "radar_chart.png")


if __name__ == "__main__":
    main()
