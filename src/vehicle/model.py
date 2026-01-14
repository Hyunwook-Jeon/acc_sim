class Vehicle:
    def __init__(
        self,
        x=0.0,
        y=0.0,
        speed=0.0,
        heading=0.0
    ):
        """
        x, y      : 차량 위치 (m)
        speed     : 차량 속도 (m/s)
        heading   : 진행 방향 (rad)
        """
        self.x = x
        self.y = y
        self.speed = speed
        self.heading = heading

        self.accel = 0.0   # m/s^2
        self.length = 4.5 # 차량 길이 (m)

    def update(self, dt):
        """
        시간 dt 동안 차량 상태 업데이트
        """
        # 속도 업데이트
        self.speed += self.accel * dt
        self.speed = max(self.speed, 0.0)  # 음수 방지

        # 위치 업데이트
        self.x += self.speed * dt

    def accelerate(self, accel):
        """가속 명령"""
        self.accel = accel

    def brake(self, decel):
        """감속 명령 (양수 입력)"""
        self.accel = -abs(decel)

    def stop(self):
        self.accel = 0.0
