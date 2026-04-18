from src.algorithms.algorithm import handle_corner, plan_straight_action
from src.physics import CarState, get_total_pit_stop_time

def simulate_lap(car_state, track_segments, weather_data):
    """
    Simulates a single lap, updating the car_state.
    """
    actions = []
    # Entry speed for first segment: 0 m/s for Lap 1, otherwise assume constant carry-over
    # Note: Real sim would track speed across laps
    current_speed = 0.0 if car_state.total_distance == 0 else 20.0 

    for i, segment in enumerate(track_segments):
        next_segment = track_segments[i + 1] if i + 1 < len(track_segments) else None

        if car_state.is_limp_mode:
            # Handle Limp Mode: constant slow speed, no strategy
            action = {
                "id": segment["id"],
                "type": segment["type"],
                "target_m/s": 20.0,
                "brake_start_m_before_next": 0.0
            }
            actions.append(action)
            car_state.total_time += segment["length_m"] / 20.0
            continue

        if segment["type"] == "straight":
            action, current_speed = plan_straight_action(
                car_state, segment, next_segment, current_speed, weather_data
            )
            actions.append(action)

        elif segment["type"] == "corner":
            action, current_speed = handle_corner(
                car_state, segment, current_speed, weather_data
            )
            actions.append(action)

    return actions

def build_strategy(input_data):
    car_config = input_data["car"]
    race_config = input_data["race"]
    track = input_data["track"]
    
    # Initialize Physics State
    initial_fuel = car_config.get("initial_fuel_l", 150.0)
    initial_tyre = {"id": 1, "compound": "Soft", "degradation": 0.0}
    
    state = CarState(initial_fuel, initial_tyre, car_config)
    
    laps_output = []
    num_laps = race_config["laps"]
    
    # Weather - for Level 4, we'd look this up in input_data['weather']
    # Default to dry for now
    weather_data = {"condition": "dry", "acceleration_multiplier": 1.0, "deceleration_multiplier": 1.0}

    for lap_num in range(1, num_laps + 1):
        
        # 1. Decision: Should we pit?
        pit_enter = False
        if state.tyre_set['degradation'] > 0.85 or state.fuel < 30:
            pit_enter = True
            
            # Physicist's Pit Stop Calculation
            pit_time = get_total_pit_stop_time(
                refuel_amount_l=50.0, # Strategy: top up 50L
                refuel_rate_lps=race_config.get('pit_refuel_rate_l/s', 5.0),
                tyre_swap_time_s=race_config.get('pit_tyre_swap_time_s', 5.0),
                base_pit_time_s=race_config.get('base_pit_stop_time_s', 20.0)
            )
            
            # Update state with new resources
            new_tyre = {"id": state.tyre_set['id'] + 1, "compound": "Soft", "degradation": 0.0}
            state.apply_pit_stop(pit_time, new_tyre, refuel_amount=50.0)

        # 2. Run the actual lap simulation
        segment_actions = simulate_lap(state, track["segments"], weather_data)

        lap_plan = {
            "lap": lap_num,
            "segments": segment_actions,
            "pit": {
                "enter": pit_enter
            }
        }
        
        if pit_enter:
            lap_plan["pit"]["tyre_change_set_id"] = state.tyre_set['id']
            lap_plan["pit"]["fuel_refuel_amount_l"] = 50.0

        laps_output.append(lap_plan)

    return {
        "initial_tyre_id": 1,
        "laps": laps_output
    }
