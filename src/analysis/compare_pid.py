import pandas as pd

df = pd.read_csv("pid_tuning_results.csv")

best = df.sort_values("score").iloc[0]
worst = df.sort_values("score").iloc[-1]

print("Best PID:")
print(best)

print("\nWorst PID:")
print(worst)
