class PIDACC:
    def __init__(
        self,
        kp=0.8,
        ki=0.05,
        kd=0.2,
        target_headway=1.5,
        max_accel=2.0,
        max_decel=-3.0
    ):
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.target_headway = target_headway
        self.max_accel = max_accel
        self.max_decel = max_decel

        self.integral = 0.0
        self.prev_error = 0.0

    def compute_acceleration(self, ego, headway, dt):
        # 앞차 없으면 부드럽게 가속
        if headway is None:
            return 0.5

        # 제어 오차: (현재 TH - 목표 TH)
        error = headway["time_headway"] - self.target_headway

        # PID 항 계산
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt

        accel = (
            self.kp * error +
            self.ki * self.integral +
            self.kd * derivative
        )

        # 가속도 제한 (실차 느낌)
        accel = max(self.max_decel, min(self.max_accel, accel))

        self.prev_error = error
        return accel
