import numpy as np
import pandas as pd


def _get_first_present_column(df, candidates):
    for col in candidates:
        if col in df.columns:
            return col
    return None


def evaluate_log(log_path, target_headway=1.5):
    """
    로그 CSV를 평가하여 score와 metrics 반환.

    지원 컬럼:
      - headway/time_headway
      - accel/acceleration/ego_accel
      - target_headway (없으면 함수 인자 사용)
      - distance (충돌 판정용)
    """
    df = pd.read_csv(log_path)

    headway_col = _get_first_present_column(
        df, ["time_headway", "headway"]
    )
    accel_col = _get_first_present_column(
        df, ["accel", "acceleration", "ego_accel"]
    )

    if headway_col is None:
        raise ValueError("Headway column not found in log.")
    if accel_col is None:
        raise ValueError("Acceleration column not found in log.")

    target_series = (
        df["target_headway"]
        if "target_headway" in df.columns
        else target_headway
    )

    headway_error = df[headway_col] - target_series
    headway_rmse = np.sqrt(np.mean(headway_error**2))

    accel_rms = np.sqrt(np.mean(df[accel_col] ** 2))

    collision = int(
        (df["distance"] <= 0).any()
    ) if "distance" in df.columns else 0

    score = (
        1.0 * headway_rmse
        + 0.5 * accel_rms
        + 100.0 * collision
    )

    metrics = {
        "headway_rmse": headway_rmse,
        "accel_rms": accel_rms,
        "collision": collision,
    }

    return score, metrics
