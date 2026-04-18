from .constants import K_BASE, K_DRAG, K_STRAIGHT, K_BRAKING, K_CORNER

def calculate_fuel_usage(v_initial, v_final, distance):
    """
    Formula: F_used = (K_base + K_drag * ((v_i + v_f)/2)^2) * distance
    """
    avg_speed = (v_initial + v_final) / 2
    return (K_BASE + K_DRAG * (avg_speed**2)) * distance

def get_refuel_time(amount_l, refuel_rate_lps):
    """
    Formula: refuel_time = amount / rate
    """
    if refuel_rate_lps <= 0: return float('inf')
    return amount_l / refuel_rate_lps

def get_total_pit_stop_time(refuel_amount_l, refuel_rate_lps, tyre_swap_time_s, base_pit_time_s):
    """
    Formula: total_time = refuel_time + tyre_swap_time + base_pit_time
    """
    refuel_time = get_refuel_time(refuel_amount_l, refuel_rate_lps)
    return refuel_time + tyre_swap_time_s + base_pit_time_s

def calculate_total_straight_fuel(d_accel, d_cruise, d_brake, v_entry, v_target, v_exit):
    """
    Calculates fuel by breaking the straight into its 3 physical phases.
    """
    fuel_accel = calculate_fuel_usage(v_entry, v_target, d_accel)
    fuel_cruise = calculate_fuel_usage(v_target, v_target, d_cruise)
    fuel_brake = calculate_fuel_usage(v_target, v_exit, d_brake)
    return fuel_accel + fuel_cruise + fuel_brake

def get_straight_degradation(tyre_degradation_rate, length):
    return tyre_degradation_rate * length * K_STRAIGHT

def get_braking_degradation(v_initial, v_final, tyre_degradation_rate):
    return ((v_initial/100)**2 - (v_final/100)**2) * K_BRAKING * tyre_degradation_rate

def get_corner_degradation(speed, radius, tyre_degradation_rate):
    if radius == 0: return 0
    return K_CORNER * (speed**2 / radius) * tyre_degradation_rate

def get_current_friction(base_friction, total_degradation, weather_multiplier):
    return max(0.0, (base_friction - total_degradation) * weather_multiplier)
