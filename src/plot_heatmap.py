from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from data_utils import DATA_FILE, INDICATORS, load_and_validate_data
from plot_config import COLOR_PALETTE, DISPLAY_LABELS, TITLE_PREFIX, configure_matplotlib


OUTPUT_FILE = Path(__file__).resolve().parents[1] / "figures" / "heatmap.png"

# 在创建图形之前，先应用统一的字体和颜色设置。
configure_matplotlib()


def create_heatmap(df, output_file=OUTPUT_FILE):
    """根据评分数据生成热力图并保存到文件。"""
    # 直接使用 data_utils 中定义好的指标顺序，
    # 这样即使 CSV 列顺序变化，图里的指标顺序也不会乱。
    heatmap_data = df.set_index("candidate")[INDICATORS]
    display_labels = [DISPLAY_LABELS[column] for column in INDICATORS]

    # 创建热力图。
    # vmin 和 vmax 把颜色范围固定在 1 到 5，
    # 这样不同数据下颜色深浅仍然具有一致含义。
    fig, ax = plt.subplots(figsize=(10.5, 5.4))
    image = ax.imshow(heatmap_data.values, cmap="GnBu", aspect="auto", vmin=1, vmax=5)

    # 把代码字段名换成更适合展示的中文标签。
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

            # 深色格子用白字，浅色格子用深色字，
            # 这样数字在不同背景下都更容易看清。
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

    # 颜色条用来说明颜色和评分高低之间的对应关系。
    colorbar = fig.colorbar(image, ax=ax, label="评分")
    colorbar.outline.set_edgecolor(COLOR_PALETTE["grid"])

    # 去掉外框线，让整体画面更简洁。
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
