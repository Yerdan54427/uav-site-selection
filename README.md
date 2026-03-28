# UAV Site Selection

A small Python project for evaluating UAV takeoff and landing site candidates on a campus.

The project reads a CSV file of candidate scores, calculates a weighted total score, and generates three figures:

1. A score heatmap
2. A weighted total score bar chart
3. A radar chart for the top 2 candidates

Generated figures are saved in the `figures/` folder.

## Project Structure

```text
uav-site-selection/
  README.md
  requirements.txt
  .gitignore
  data/
    candidate_scores.csv
  figures/
  src/
    main.py
    plot_heatmap.py
    plot_bar.py
    plot_radar.py
```

## Setup

```bash
pip install -r requirements.txt
```

## Run

From the project root:

```bash
python src/main.py
```

After running, the generated figures will appear in `figures/`.

## Input Data

The CSV file should include:

- One `candidate` column
- Several scoring columns with numeric values

This project includes a simple sample dataset in `data/candidate_scores.csv`.
