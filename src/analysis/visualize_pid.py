from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main():
    base_dir = Path(__file__).resolve().parents[2]
    csv_path = base_dir / "results/pid_gain_sweep.csv"

    df = pd.read_csv(csv_path)

    # Ki 고정하고 Kp-Kd 관계 시각화
    ki_fixed = 0.05
    df_k = df[df["ki"] == ki_fixed]

    pivot = df_k.pivot(
        index="kp",
        columns="kd",
        values="mean_th_error",
    )

    plt.figure(figsize=(8, 6))
    plt.imshow(pivot, origin="lower")
    plt.colorbar(label="Mean TH Error")

    plt.xticks(range(len(pivot.columns)), pivot.columns)
    plt.yticks(range(len(pivot.index)), pivot.index)

    plt.xlabel("Kd")
    plt.ylabel("Kp")
    plt.title(f"PID Gain Sweep Heatmap (Ki={ki_fixed})")

    plt.show()


if __name__ == "__main__":
    main()
