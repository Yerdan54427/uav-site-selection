from pathlib import Path

from plot_bar import create_bar_chart
from plot_heatmap import create_heatmap
from plot_radar import create_radar_chart
from data_utils import DATA_FILE, prepare_data


FIGURES_DIR = Path(__file__).resolve().parents[1] / "figures"


def main():
    # Read, validate, score, and sort the candidate data.
    df = prepare_data(DATA_FILE)

    # Print the final ranking to the terminal.
    print("Campus UAV Site Selection Ranking")
    print(df[["candidate", "total_score"]].to_string(index=False))

    # Generate all figures in the figures folder.
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    create_heatmap(df, FIGURES_DIR / "heatmap.png")
    create_bar_chart(df, FIGURES_DIR / "bar_chart.png")
    create_radar_chart(df, FIGURES_DIR / "radar_chart.png")


if __name__ == "__main__":
    main()
