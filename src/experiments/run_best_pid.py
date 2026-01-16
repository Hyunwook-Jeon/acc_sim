import pandas as pd
from pathlib import Path


def main():
    BASE_DIR = Path(__file__).resolve().parents[2]
    CSV_PATH = BASE_DIR / "results/pid_gain_sweep.csv"

    df = pd.read_csv(CSV_PATH)

    best_row = df.loc[df["mean_th_error"].idxmin()]

    print(" Best PID Gain Found")
    print(f"Kp = {best_row.kp}")
    print(f"Ki = {best_row.ki}")
    print(f"Kd = {best_row.kd}")
    print(f"Mean Throttle Error = {best_row.mean_th_error}")

    # 여기서 Vehicle / PIDController에 그대로 적용
    # pid = PIDController(best_row.kp, best_row.ki, best_row.kd)


if __name__ == "__main__":
    main()
