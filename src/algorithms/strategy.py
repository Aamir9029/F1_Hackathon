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


def simulate_lap(car, track_segments, tyre_friction, fuel, tyre_health):
    actions = []
    current_speed = 0.0

    # Track state
    current_fuel = fuel
    current_tyre_health = tyre_health

    for i, segment in enumerate(track_segments):
        next_segment = track_segments[i + 1] if i + 1 < len(track_segments) else None

        if current_fuel <= 0:
            raise Exception("Out of fuel ❌")

        if segment["type"] == "straight":
            action, current_speed = plan_straight_action(
                car,
                segment,
                next_segment,
                current_speed,
                tyre_friction
            )
            actions.append(action)

            # Fuel consumption (simple model)
            current_fuel -= segment["length_m"] * 0.0005

            # Tyre degradation (straight)
            current_tyre_health -= 0.0001 * segment["length_m"]

            current_tyre_health = max(0.5, current_tyre_health)

        elif segment["type"] == "corner":
            action, current_speed = handle_corner(
                car,
                segment,
                current_speed,
                tyre_friction * current_tyre_health
            )
            actions.append(action)

            # Fuel consumption (corner)
            current_fuel -= segment["length_m"] * 0.0003

            # Tyre degradation (corner heavier)
            current_tyre_health -= 0.0003 * segment["length_m"]

            current_tyre_health = max(0.5, current_tyre_health)

    return actions


def build_strategy_with_pit(input_data):
    car = input_data["car"]
    race = input_data.get("race", {"laps": 1})
    track = input_data["track"]

    tyre_friction = _extract_tyre_friction(input_data)
    initial_tyre_id = 1  # you can change later

    fuel = car.get("initial_fuel", car.get("fuel_tank_capacity", 100))
    tyre_health = 1.0
    tyre_id = 1

    laps_output = []

    for lap_num in range(1, race["laps"] + 1):

        pit_enter = False

        # Simple pit rule: pit if tyre health too low or fuel too low
        if tyre_health < 0.65 or fuel < 20:
            pit_enter = True
            tyre_health = 1.0
            fuel = car.get("fuel_tank_capacity", 100)
            tyre_id += 1

        segment_actions = simulate_lap(
            car,
            track["segments"],
            tyre_friction,
            fuel,
            tyre_health
        )

        # Rough carry-over (simulate consumption per lap)
        fuel -= 10
        tyre_health -= 0.1

        lap_plan = {
            "lap": lap_num,
            "segments": segment_actions,
            "pit": {
                "enter": pit_enter
            }
        }

        laps_output.append(lap_plan)

    return {
        "initial_tyre_id": initial_tyre_id,
        "laps": laps_output
    }


def build_strategy(input_data):
    return build_strategy_with_pit(input_data)
