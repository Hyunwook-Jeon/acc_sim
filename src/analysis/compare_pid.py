from pathlib import Path

import pandas as pd


def main():
    base_dir = Path(__file__).resolve().parents[2]
    csv_path = base_dir / "results/pid_gain_sweep.csv"

    df = pd.read_csv(csv_path)

    best = df.sort_values("mean_th_error").iloc[0]
    worst = df.sort_values("mean_th_error").iloc[-1]

    print("Best PID (min mean_th_error):")
    print(best)

    print("\nWorst PID (max mean_th_error):")
    print(worst)


if __name__ == "__main__":
    main()
