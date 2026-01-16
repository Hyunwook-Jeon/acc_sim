import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("pid_tuning_results.csv")

# Ki 고정하고 Kp-Kd 관계 시각화
Ki_fixed = 0.05
df_k = df[df["Ki"] == Ki_fixed]

pivot = df_k.pivot(
    index="Kp",
    columns="Kd",
    values="score"
)

plt.figure(figsize=(8, 6))
plt.imshow(pivot, origin="lower")
plt.colorbar(label="Score")

plt.xticks(range(len(pivot.columns)), pivot.columns)
plt.yticks(range(len(pivot.index)), pivot.index)

plt.xlabel("Kd")
plt.ylabel("Kp")
plt.title(f"PID Score Heatmap (Ki={Ki_fixed})")

plt.show()
