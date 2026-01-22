from src.experiments.runner import run_simulation
from src.ml.ml_acc_controller import MLACCController


def main():
    controller = MLACCController("models/ml_accel_model.pkl")
    scenario = {
        "ego_init_speed": 20,
        "lead_init_speed": 15,
        "initial_gap": 30,
    }
    df = run_simulation(controller, scenario)
    print(df.head())


if __name__ == "__main__":
    main()
