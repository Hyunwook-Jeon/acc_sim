# src/experiments/pid_gain_sweep.py

import itertools
import csv
import os
from src.sim.world import World
from src.vehicle.model import Vehicle
from src.adas.pid_acc import PIDACC





KP_LIST = [0.3, 0.5, 0.8, 1.0]
KI_LIST = [0.01, 0.03, 0.05]
KD_LIST = [0.1, 0.2, 0.3]

SIM_TIME = 20.0
DT = 0.1
TARGET_TH = 1.5


def run_simulation(kp, ki, kd):
    world = World(dt=DT)

    ego = Vehicle(x=0.0, speed=20.0)
    lead = Vehicle(x=40.0, speed=22.0)

    acc = PIDACC(
        kp=kp,
        ki=ki,
        kd=kd,
        target_headway=TARGET_TH
    )

    world.add_vehicle(ego)
    world.add_vehicle(lead)

    th_error_sum = 0.0
    steps = int(SIM_TIME / DT)

    for _ in range(steps):
        headway = world.get_headway(ego)
        accel = acc.compute_acceleration(ego, headway, DT)

        ego.accelerate(accel)
        lead.accelerate(0.0)

        world.step()

        if headway:
            th_error = abs(headway["time_headway"] - TARGET_TH)
            th_error_sum += th_error

    return th_error_sum / steps


def main():
    os.makedirs("results", exist_ok=True)

    results = []

    for kp, ki, kd in itertools.product(KP_LIST, KI_LIST, KD_LIST):
        print(f"Running: KP={kp}, KI={ki}, KD={kd}")
        score = run_simulation(kp, ki, kd)
        results.append([kp, ki, kd, score])

    with open("results/pid_gain_sweep.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["kp", "ki", "kd", "mean_th_error"])
        writer.writerows(results)


if __name__ == "__main__":
    main()
