import pandas as pd

from src.sim.world import World
from src.vehicle.model import Vehicle


def run_simulation(
    controller,
    scenario,
    sim_time=20.0,
    dt=0.1
):
    """
    controller : PIDACC 또는 ML Controller
    scenario   : dict (초기 조건)
    return     : pandas DataFrame (ML dataset)
    """

    world = World(dt=dt)

    ego = Vehicle(
        x=0.0,
        speed=scenario["ego_init_speed"]
    )

    lead = Vehicle(
        x=scenario["initial_gap"],
        speed=scenario["lead_init_speed"]
    )

    world.add_vehicle(ego)
    world.add_vehicle(lead)

    logs = []

    steps = int(sim_time / dt)

    for _ in range(steps):
        headway = world.get_headway(ego)

        accel = controller.compute_acceleration(
            ego, headway, dt
        )

        ego.accelerate(accel)
        lead.accelerate(scenario.get("lead_accel", 0.0))

        world.step()

        if headway:
            logs.append({
                "time": world.time,
                "ego_speed": ego.speed,
                "lead_speed": lead.speed,
                "distance": headway["distance"],
                "relative_speed": headway["relative_speed"],
                "time_headway": headway["time_headway"],
                "accel": accel
            })

    return pd.DataFrame(logs)
