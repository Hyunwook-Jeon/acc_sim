import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt


CSV_FILE = Path(__file__).resolve().parents[2] / "results/pid_tuning_result.csv"
TARGET_TH = 1.5


def load_data(filename):
    time = []
    ego_speed = []
    lead_speed = []
    distance = []
    time_headway = []
    accel = []

    with open(filename, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            time.append(float(row["time"]))
            ego_speed.append(float(row["ego_speed"]))
            lead_speed.append(float(row["lead_speed"]))
            distance.append(float(row["distance"]))
            time_headway.append(float(row["time_headway"]))
            accel.append(float(row["accel"]))

    return time, ego_speed, lead_speed, distance, time_headway, accel


def compute_rms_error(th_list, target):
    error_sq = [(th - target) ** 2 for th in th_list]
    return math.sqrt(sum(error_sq) / len(error_sq))


def main():
    (
        time,
        ego_speed,
        lead_speed,
        distance,
        time_headway,
        accel,
    ) = load_data(CSV_FILE)

    rms_th_error = compute_rms_error(time_headway, TARGET_TH)

    print("===== PID ACC Performance =====")
    print(f"Target Time Headway : {TARGET_TH:.2f} s")
    print(f"RMS TH Error        : {rms_th_error:.4f} s")

    # =====================
    # Plot: Speed
    # =====================
    plt.figure()
    plt.plot(time, ego_speed, label="Ego Speed")
    plt.plot(time, lead_speed, label="Lead Speed")
    plt.xlabel("Time [s]")
    plt.ylabel("Speed [m/s]")
    plt.legend()
    plt.grid()

    # =====================
    # Plot: Time Headway
    # =====================
    plt.figure()
    plt.plot(time, time_headway, label="Time Headway")
    plt.axhline(TARGET_TH, linestyle="--", label="Target TH")
    plt.xlabel("Time [s]")
    plt.ylabel("Time Headway [s]")
    plt.legend()
    plt.grid()

    # =====================
    # Plot: Acceleration
    # =====================
    plt.figure()
    plt.plot(time, accel)
    plt.xlabel("Time [s]")
    plt.ylabel("Acceleration [m/s²]")
    plt.grid()

    plt.show()


if __name__ == "__main__":
    main()
