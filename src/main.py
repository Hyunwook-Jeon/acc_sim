import math
import matplotlib.pyplot as plt
import numpy as np

from src.sim.world import World
from src.vehicle.model import Vehicle
from src.adas.pid_acc import PIDACC


# =====================
# 시뮬레이션 함수
# =====================
def run_simulation(kp, ki, kd, target_th=1.5, log=False):
    world = World(dt=0.1)

    ego = Vehicle(x=0.0, speed=10.0)
    lead = Vehicle(x=40.0, speed=8.0)

    acc = PIDACC(kp=kp, ki=ki, kd=kd, target_headway=target_th)

    world.add_vehicle(ego)
    world.add_vehicle(lead)

    th_errors = []
    accel_log = []

    time = []
    ego_v = []
    lead_v = []
    th_log = []

    for _ in range(200):
        headway = world.get_headway(ego)
        accel = acc.compute_acceleration(ego, headway, world.dt)

        ego.accelerate(accel)
        lead.accelerate(0.0)
        world.step()

        if headway:
            th_error = headway["time_headway"] - target_th
            th_errors.append(th_error)
            th_log.append(headway["time_headway"])
        else:
            th_log.append(None)

        accel_log.append(accel)

        if log:
            time.append(world.time)
            ego_v.append(ego.speed)
            lead_v.append(lead.speed)

    # 성능 지표
    th_avg = sum(abs(e) for e in th_errors) / len(th_errors)
    th_max = max(abs(e) for e in th_errors)
    rms_acc = math.sqrt(sum(a * a for a in accel_log) / len(accel_log))

    if log:
        return th_avg, th_max, rms_acc, time, ego_v, lead_v, th_log

    return th_avg, th_max, rms_acc


def main():
    # =====================
    # PID 후보
    # =====================
    kp_list = [0.4, 0.6, 0.8, 1.0]
    kd_list = [0.1, 0.2, 0.3]
    best_ki = 0.03

    # =====================
    # 히트맵용 Score 계산
    # =====================
    score_map = np.zeros((len(kp_list), len(kd_list)))

    w_avg, w_max, w_acc = 1.0, 2.0, 0.5

    for i, kp in enumerate(kp_list):
        for j, kd in enumerate(kd_list):
            avg, max_e, rms = run_simulation(kp, best_ki, kd)
            score = w_avg * avg + w_max * max_e + w_acc * rms
            score_map[i, j] = score

    # =====================
    # 히트맵 시각화
    # =====================
    plt.figure()
    plt.imshow(score_map, origin="lower")
    plt.colorbar(label="Score")
    plt.xticks(range(len(kd_list)), kd_list)
    plt.yticks(range(len(kp_list)), kp_list)
    plt.xlabel("Kd")
    plt.ylabel("Kp")
    plt.title("PID Gain Score Heatmap (Ki fixed)")
    plt.grid(False)

    # =====================
    # 최적 Gain 선택
    # =====================
    min_idx = np.unravel_index(np.argmin(score_map), score_map.shape)
    best_kp = kp_list[min_idx[0]]
    best_kd = kd_list[min_idx[1]]

    print(f"\n최적 Gain: Kp={best_kp}, Ki={best_ki}, Kd={best_kd}")

    # =====================
    # 최적 Gain 재시뮬레이션
    # =====================
    avg, max_e, rms, t, ego_v, lead_v, th = run_simulation(
        best_kp, best_ki, best_kd, log=True
    )

    # 속도
    plt.figure()
    plt.plot(t, ego_v, label="Ego")
    plt.plot(t, lead_v, label="Lead")
    plt.xlabel("Time [s]")
    plt.ylabel("Speed [m/s]")
    plt.legend()
    plt.grid()

    # Time Headway
    plt.figure()
    plt.plot(t, th)
    plt.axhline(1.5, linestyle="--", label="Target TH")
    plt.xlabel("Time [s]")
    plt.ylabel("Time Headway [s]")
    plt.legend()
    plt.grid()

    # 성능 요약
    print(
        f"TH_avg={avg:.3f}, TH_max={max_e:.3f}, RMS_acc={rms:.3f}"
    )

    plt.show()


if __name__ == "__main__":
    main()
