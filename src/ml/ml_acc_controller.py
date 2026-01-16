import joblib
import numpy as np

class MLACCController:
    def __init__(self, model_path):
        self.model = joblib.load(model_path)

    def compute_acceleration(self, ego, headway, dt):
        if headway is None:
            return 0.0

        X = [[
            ego.speed,
            headway["distance"],
            headway["relative_speed"],
            headway["time_headway"]
        ]]

        accel = self.model.predict(X)[0]

        # 🔒 안전장치 (필수)
        return float(np.clip(accel, -3.0, 2.0))
