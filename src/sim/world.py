class World:
    def __init__(self, dt=0.1):
        self.dt = dt
        self.time = 0.0
        self.vehicles = []

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def step(self):
        for v in self.vehicles:
            v.update(self.dt)
        self.time += self.dt

    def get_headway(self, ego):
        # ego 앞에 있는 차량들만 필터
        front_vehicles = [
            v for v in self.vehicles
            if v.x > ego.x
        ]

        # 앞차가 없으면 None
        if not front_vehicles:
            return None

        # 가장 가까운 앞차 선택
        lead = min(front_vehicles, key=lambda v: v.x)

        # 거리 계산 (차량 길이 고려)
        distance = lead.x - ego.x - lead.length
        distance = max(distance, 0.0)

        # 상대 속도 (+면 ego가 더 빠름)
        relative_speed = ego.speed - lead.speed

        # Time Headway 계산
        if ego.speed > 0:
            time_headway = distance / ego.speed
        else:
            time_headway = float("inf")

        return {
            "lead_vehicle": lead,
            "distance": distance,
            "relative_speed": relative_speed,
            "time_headway": time_headway
        }
