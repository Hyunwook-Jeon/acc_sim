from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


def main():
    base_dir = Path(__file__).resolve().parents[2]
    dataset_path = base_dir / "data/ml_dataset.csv"
    model_dir = base_dir / "models"
    model_path = model_dir / "ml_accel_model.pkl"

    if not dataset_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {dataset_path}. "
            "Run `python -m src.ml.generate_ml_dataset` first."
        )

    df = pd.read_csv(dataset_path)

    feature_cols = [
        "ego_speed",
        "distance",
        "relative_speed",
        "time_headway",
    ]
    target_col = "accel"

    X = df[feature_cols]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    rmse = mean_squared_error(y_test, preds, squared=False)
    r2 = r2_score(y_test, preds)

    model_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)

    print("Model saved:", model_path)
    print(f"RMSE: {rmse:.4f}")
    print(f"R2: {r2:.4f}")


if __name__ == "__main__":
    main()
