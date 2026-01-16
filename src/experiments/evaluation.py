import pandas as pd
import numpy as np

def evaluate_log(log_path):
    df = pd.read_csv(log_path)

    headway_error = df["headway"] - df["target_headway"]
    headway_rmse = np.sqrt(np.mean(headway_error**2))

    accel_rms = np.sqrt(np.mean(df["ego_accel"]**2))

    collision = int((df["distance"] <= 0).any())

    score = (
        1.0 * headway_rmse
        + 0.5 * accel_rms
        + 100.0 * collision
    )

    metrics = {
        "headway_rmse": headway_rmse,
        "accel_rms": accel_rms,
        "collision": collision
    }

    return score, metrics
