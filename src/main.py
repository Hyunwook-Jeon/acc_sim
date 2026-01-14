import matplotlib.pyplot as plt

from sim.world import World
from vehicle.model import Vehicle
from adas.pid_acc import PIDACC


def main():
    # =====================
    # 시뮬레이션 설정
    # =====================
    world = World(dt=0.1)

    ego = Vehicle(x=0.0, speed=10.0)
    lead = Vehicle(x=40.0, speed=8.0)

    acc = PIDACC(
        kp=0.9,
        ki=0.04,
        kd=0.25,
        target_headway=1.5
    )

    world.add_vehicle(ego)
    world.add_vehicle(lead)

    # =====================
    # 로그 저장
    # =====================
    time_log = []
    ego_speed_log = []
    lead_speed_log = []
    distance_log = []
    th_log = []
    accel_log = []

    # =====================
    # 시뮬레이션 루프
    # =====================
    for _ in range(200):
        headway = world.get_headway(ego)
        accel = acc.compute_acceleration(ego, headway, world.dt)

        ego.accelerate(accel)
        lead.accelerate(0.0)

        world.step()

        # 로그
        time_log.append(world.time)
        ego_speed_log.append(ego.speed)
        lead_speed_log.append(lead.speed)
        accel_log.append(accel)

        if headway:
            distance_log.append(headway["distance"])
            th_log.append(headway["time_headway"])
        else:
            distance_log.append(None)
            th_log.append(None)

        # 콘솔 출력
        if headway:
            print(
                f"t={world.time:.1f}s | "
                f"ego_v={ego.speed:.2f} | "
                f"dist={headway['distance']:.2f} | "
                f"TH={headway['time_headway']:.2f} | "
                f"a={accel:.2f}"
            )

    # =====================
    # 그래프
    # =====================

    # 속도
    plt.figure()
    plt.plot(time_log, ego_speed_log, label="Ego Speed")
    plt.plot(time_log, lead_speed_log, label="Lead Speed")
    plt.xlabel("Time [s]")
    plt.ylabel("Speed [m/s]")
    plt.legend()
    plt.grid()

    # Time Headway
    plt.figure()
    plt.plot(time_log, th_log, label="Time Headway")
    plt.axhline(1.5, linestyle="--", label="Target TH")
    plt.xlabel("Time [s]")
    plt.legend()
    plt.grid()

    # 가속도
    plt.figure()
    plt.plot(time_log, accel_log)
    plt.xlabel("Time [s]")
    plt.ylabel("Acceleration [m/s²]")
    plt.grid()

    plt.show()


if __name__ == "__main__":
    main()
