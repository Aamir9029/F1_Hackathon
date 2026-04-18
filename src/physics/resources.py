from .constants import K_BASE, K_DRAG, K_STRAIGHT, K_BRAKING, K_CORNER

def calculate_fuel_usage(v_initial, v_final, distance):
    """
    Formula: F_used = (K_base + K_drag * ((v_i + v_f)/2)^2) * distance
    """
    avg_speed = (v_initial + v_final) / 2
    return (K_BASE + K_DRAG * (avg_speed**2)) * distance

def get_straight_degradation(tyre_degradation_rate, length):
    return tyre_degradation_rate * length * K_STRAIGHT

def get_braking_degradation(v_initial, v_final, tyre_degradation_rate):
    """
    Formula: ((v_i/100)^2 - (v_f/100)^2) * K_BRAKING * degradation_rate
    """
    return ((v_initial/100)**2 - (v_final/100)**2) * K_BRAKING * tyre_degradation_rate

def get_corner_degradation(speed, radius, tyre_degradation_rate):
    """
    Formula: K_CORNER * (speed^2 / radius) * degradation_rate
    """
    if radius == 0: return 0
    return K_CORNER * (speed**2 / radius) * tyre_degradation_rate

def get_current_friction(base_friction, total_degradation, weather_multiplier):
    """
    Formula: friction = (base - total_degradation) * weather_multiplier
    """
    return (base_friction - total_degradation) * weather_multiplier
