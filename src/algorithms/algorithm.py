from src.physics import (
    get_distance_to_reach_speed, 
    get_max_corner_speed, 
    solve_straight_segment,
    calculate_total_straight_fuel,
    get_straight_degradation,
    get_braking_degradation,
    get_corner_degradation
)

def _extract_car_stats(car):
    return {
        "max_speed": car.get("max_speed_m/s", 50.0),
        "accel": car.get("accel_m/se2", 5.0),
        "brake": car.get("brake_m/se2", 5.0),
        "crawl": car.get("crawl_constant_m/s", 1.0),
    }

def plan_straight_action(car_state, straight, next_segment, entry_speed, weather_data):
    """
    Uses Level 4 physics to plan a straight and track resource consumption.
    """
    stats = _extract_car_stats(car_state.car_config)
    max_speed = stats["max_speed"]
    accel = stats["accel"]
    brake = stats["brake"]
    crawl = stats["crawl"]
    
    # Get current friction for safety
    current_friction = car_state.get_current_friction(weather_data['condition'])
    
    # 1. Determine exit speed needed for the next corner
    next_corner_speed = max_speed
    if next_segment and next_segment["type"] == "corner":
        next_corner_speed = get_max_corner_speed(current_friction, next_segment["radius_m"], crawl)

    # 2. Solve the kinematics (Three-Phase: Accel, Cruise, Brake)
    # Applying weather multipliers from Level 3
    accel_mult = weather_data.get('acceleration_multiplier', 1.0)
    brake_mult = weather_data.get('deceleration_multiplier', 1.0)
    
    d_accel, d_cruise, d_brake, t_segment = solve_straight_segment(
        straight["length_m"], entry_speed, max_speed, next_corner_speed, 
        accel, brake, accel_mult, brake_mult
    )

    # 3. Calculate Resource Costs
    fuel_cost = calculate_total_straight_fuel(d_accel, d_cruise, d_brake, entry_speed, max_speed, next_corner_speed)
    
    # Tyre wear
    # Get degradation rate for this tyre/weather combo
    from src.physics.data_models import get_tyre_specs
    _, _, deg_rate = get_tyre_specs(car_state.tyre_set['compound'], weather_data['condition'])
    
    wear = get_straight_degradation(deg_rate, d_accel + d_cruise)
    wear += get_braking_degradation(max_speed, next_corner_speed, deg_rate)

    # 4. Update the Car State
    car_state.fuel -= fuel_cost
    car_state.tyre_set['degradation'] += wear
    car_state.total_time += t_segment
    
    if car_state.tyre_set['degradation'] >= 1.0 or car_state.fuel <= 0:
        car_state.is_limp_mode = True

    action = {
        "id": straight["id"],
        "type": "straight",
        "target_m/s": round(max_speed, 3),
        "brake_start_m_before_next": round(d_brake, 3),
    }

    return action, next_corner_speed

def handle_corner(car_state, corner, entry_speed, weather_data):
    """
    Level 4 Cornering: Constant speed, tracks wear and fuel.
    """
    length = corner["length_m"]
    radius = corner["radius_m"]
    
    # Constant speed through corner
    t_segment = length / entry_speed if entry_speed > 0 else 0
    
    # Resources
    fuel_cost = calculate_total_straight_fuel(0, length, 0, entry_speed, entry_speed, entry_speed)
    
    from src.physics.data_models import get_tyre_specs
    _, _, deg_rate = get_tyre_specs(car_state.tyre_set['compound'], weather_data['condition'])
    wear = get_corner_degradation(entry_speed, radius, deg_rate)
    
    # Update State
    car_state.fuel -= fuel_cost
    car_state.tyre_set['degradation'] += wear
    car_state.total_time += t_segment
    
    if car_state.tyre_set['degradation'] >= 1.0 or car_state.fuel <= 0:
        car_state.is_limp_mode = True

    action = {
        "id": corner["id"],
        "type": "corner",
    }
    return action, entry_speed
