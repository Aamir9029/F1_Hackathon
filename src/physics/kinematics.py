import math
from .constants import GRAVITY

def get_max_corner_speed(tyre_friction, radius, crawl_constant):
    """
    Formula: max_corner_speed = sqrt(tyre_friction * gravity * radius) + crawl_constant
    """
    effective_friction = max(0.0, tyre_friction)
    effective_radius = max(0.0, radius)
    return math.sqrt(effective_friction * GRAVITY * effective_radius) + crawl_constant

def get_time_to_reach_speed(v_initial, v_final, acceleration):
    if acceleration == 0:
        return 0 if v_initial == v_final else float('inf')
    return abs(v_final - v_initial) / acceleration

def get_distance_to_reach_speed(v_initial, v_final, acceleration):
    if acceleration == 0:
        return 0
    return abs(v_final**2 - v_initial**2) / (2 * acceleration)

def solve_straight_segment(length, v_entry, v_target, v_exit, accel, brake, accel_mult=1.0, brake_mult=1.0):
    """
    Calculates the breakdown of a straight segment, applying weather multipliers.
    """
    effective_accel = accel * accel_mult
    effective_brake = brake * brake_mult
    
    d_accel = get_distance_to_reach_speed(v_entry, v_target, effective_accel)
    d_brake = get_distance_to_reach_speed(v_target, v_exit, effective_brake)
    
    if d_accel + d_brake > length:
        d_cruise = 0
        d_accel = length * (effective_accel / (effective_accel + effective_brake))
        d_brake = length - d_accel
        v_peak = math.sqrt(v_entry**2 + 2 * effective_accel * d_accel)
        
        t_accel = get_time_to_reach_speed(v_entry, v_peak, effective_accel)
        t_brake = get_time_to_reach_speed(v_peak, v_exit, effective_brake)
        return d_accel, 0, d_brake, (t_accel + t_brake)

    d_cruise = length - d_accel - d_brake
    t_accel = get_time_to_reach_speed(v_entry, v_target, effective_accel)
    t_cruise = d_cruise / v_target if v_target > 0 else 0
    t_brake = get_time_to_reach_speed(v_target, v_exit, effective_brake)
    
    return d_accel, d_cruise, d_brake, (t_accel + t_cruise + t_brake)

def get_time_for_corner(speed, length):
    """
    Corners are traversed at constant speed.
    """
    if speed <= 0:
        return float('inf')
    return length / speed
