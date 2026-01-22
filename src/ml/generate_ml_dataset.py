import random
import pandas as pd

from src.adas.pid_acc import PIDACC
from src.experiments.runner import run_simulation

pid = PIDACC(kp=0.8, ki=0.03, kd=0.2)

all_data = []

for _ in range(50):  # 시나리오 50개
    scenario = {
        "ego_init_speed": random.uniform(10, 30),
        "lead_init_speed": random.uniform(5, 25),
        "initial_gap": random.uniform(20, 60)
    }

    df = run_simulation(pid, scenario)
    all_data.append(df)

dataset = pd.concat(all_data, ignore_index=True)
dataset.to_csv("data/ml_dataset.csv", index=False)
