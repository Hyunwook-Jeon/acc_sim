class AdaptiveCruiseControl:
    def __init__(self,
                 target_speed=12.0,
                 min_headway=1.5):
        self.target_speed = target_speed
        self.min_headway = min_headway

    def compute_acceleration(self, ego, headway, dt=None):
        if headway is None:
            # 앞차 없음 → 목표 속도로 가속
            if ego.speed < self.target_speed:
                return 1.0
            else:
                return 0.0

        distance = headway["distance"]
        rel_speed = headway["relative_speed"]
        th = headway["time_headway"]

        # 너무 가까움 → 강한 감속
        if th < self.min_headway:
            return -2.0

        # 접근 중 → 완만 감속
        if rel_speed > 0:
            return -1.0

        # 여유 있음 → 목표 속도로 가속
        if ego.speed < self.target_speed:
            return 0.5

        return 0.0
