from pathlib import Path

from data_utils import DATA_FILE, prepare_data, rank_candidate_pairs
from plot_bar import create_bar_chart
from plot_heatmap import create_heatmap
from plot_radar import create_radar_chart


FIGURES_DIR = Path(__file__).resolve().parents[1] / "figures"


def main():
    df = prepare_data(DATA_FILE)
    pair_ranking = rank_candidate_pairs(df)
    best_pair = pair_ranking.iloc[0]

    ranking_display = df[["candidate", "total_score"]].copy()
    ranking_display["total_score"] = ranking_display["total_score"].map(lambda score: f"{score:.2f}")

    pair_display = pair_ranking[["pair_name", "distance_m", "spacing_adjustment", "pair_score"]].copy()
    pair_display["distance_m"] = pair_display["distance_m"].map(lambda distance: f"{distance:.0f}")
    pair_display["spacing_adjustment"] = pair_display["spacing_adjustment"].map(
        lambda adjustment: f"{adjustment:+.2f}"
    )
    pair_display["pair_score"] = pair_display["pair_score"].map(lambda score: f"{score:.2f}")

    print("校园无人机单点候选排名")
    print(ranking_display.to_string(index=False))
    print()
    print("双点组合排名（已加入间距修正）")
    print(pair_display.to_string(index=False))
    print()
    print("最终推荐双点组合")
    print(f"候选点：{best_pair['pair_name']}")
    print(f"基础组合分：{best_pair['base_pair_score']:.2f}")
    print(f"两点间距：{best_pair['distance_m']:.0f} m")
    print(f"间距修正：{best_pair['spacing_adjustment']:+.2f}")
    print(f"最终组合分：{best_pair['pair_score']:.2f}")

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    create_heatmap(df, FIGURES_DIR / "heatmap.png")
    create_bar_chart(df, FIGURES_DIR / "bar_chart.png")
    create_radar_chart(df, FIGURES_DIR / "radar_chart.png", selected_pair=best_pair)


if __name__ == "__main__":
    main()
