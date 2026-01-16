import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def main():
    BASE_DIR = Path(__file__).resolve().parents[2]
    CSV_PATH = BASE_DIR / "results/pid_gain_sweep.csv"

    df = pd.read_csv(CSV_PATH)

    # 🔹 kd 하나 고정
    KD_FIXED = 0.2
    df = df[df["kd"] == KD_FIXED]

    heatmap_data = df.pivot(
        index="ki",
        columns="kp",
        values="mean_th_error"
    )

    plt.figure(figsize=(10, 6))
    sns.heatmap(
        heatmap_data,
        cmap="viridis",
        annot=True,
        fmt=".3f"
    )

    plt.title(f"PID Gain Sweep Heatmap (kd={KD_FIXED})")
    plt.xlabel("Kp")
    plt.ylabel("Ki")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
