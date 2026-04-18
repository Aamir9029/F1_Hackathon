from src.algorithms.algorithm import handle_corner, plan_straight_action
from src.physics import get_current_friction


def _extract_tyre_friction(input_data):
    tyres = input_data.get("tyres", {})
    available_sets = tyres.get("available_sets", [])

    if available_sets:
        first_set = available_sets[0]
        compound = first_set.get("compound")
        tyre_properties = tyres.get("properties", {}).get(compound, {})
        base_friction = tyre_properties.get("base_friction", tyre_properties.get("friction", 0.9))
        degradation = first_set.get("degradation", 0.0)
        return get_current_friction(base_friction, degradation, 1.0)

    return 0.9


def simulate_lap(car, track_segments, tyre_friction):
    actions = []
    current_speed = 0.0

    for i, segment in enumerate(track_segments):
        next_segment = track_segments[i + 1] if i + 1 < len(track_segments) else None

        if segment["type"] == "straight":
            action, current_speed = plan_straight_action(
                car,
                segment,
                next_segment,
                current_speed,
                tyre_friction
            )
            actions.append(action)

        elif segment["type"] == "corner":
            action, current_speed = handle_corner(segment, current_speed, tyre_friction)
            actions.append(action)

    return actions


def build_level1_strategy(input_data):
    car = input_data["car"]
    race = input_data.get("race", {"laps": 1})
    track = input_data["track"]

    tyre_friction = _extract_tyre_friction(input_data)
    initial_tyre_id = 1  # you can change later

    laps_output = []

    for lap_num in range(1, race["laps"] + 1):

        segment_actions = simulate_lap(
            car,
            track["segments"],
            tyre_friction
        )

        lap_plan = {
            "lap": lap_num,
            "segments": segment_actions,
            "pit": {
                "enter": False
            }
        }

        laps_output.append(lap_plan)

    return {
        "initial_tyre_id": initial_tyre_id,
        "laps": laps_output
    }


def build_strategy(input_data):
    return build_level1_strategy(input_data)
