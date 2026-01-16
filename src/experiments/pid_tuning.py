from adas.pid_acc import PIDACC
from experiments.runner import run_simulation

pid = PIDACC(kp=0.8, ki=0.03, kd=0.2)

scenario = {
    "ego_init_speed": 20.0,
    "lead_init_speed": 15.0,
    "initial_gap": 40.0
}

df = run_simulation(pid, scenario)

mean_error = (df["time_headway"] - 1.5).abs().mean()
print("Mean TH Error:", mean_error)
