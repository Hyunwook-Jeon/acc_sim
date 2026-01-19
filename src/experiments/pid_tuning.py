from src.adas.pid_acc import PIDACC
from src.experiments.runner import run_simulation
from src.ml.ml_acc_controller import MLACCController


controller = PIDACC(kp=0.8, ki=0.03, kd=0.2)

scenario = {
    "ego_init_speed": 20.0,
    "lead_init_speed": 15.0,
    "initial_gap": 40.0
}

df = run_simulation(controller, scenario)

mean_error = (df["time_headway"] - 1.5).abs().mean()
print("Mean TH Error:", mean_error)
