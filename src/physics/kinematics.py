import math
from .constants import GRAVITY

def get_max_corner_speed(tyre_friction, radius, crawl_constant):
    """
    Formula: max_corner_speed = sqrt(tyre_friction * gravity * radius) + crawl_constant
    """
    return math.sqrt(tyre_friction * GRAVITY * radius) + crawl_constant

def get_time_to_reach_speed(v_initial, v_final, acceleration):
    """
    Formula: time = (final_speed - initial_speed) / acceleration
    """
    if acceleration == 0:
        return 0 if v_initial == v_final else float('inf')
    return abs(v_final - v_initial) / acceleration

def get_distance_to_reach_speed(v_initial, v_final, acceleration):
    """
    Formula: distance = (final_speed^2 - initial_speed^2) / (2 * acceleration)
    """
    if acceleration == 0:
        return 0
    return abs(v_final**2 - v_initial**2) / (2 * acceleration)


def get_time_for_straight(v_entry, v_target, length, accel, decel, brake_start_m):
    """
    Simulates travel through a straight segment with three phases:
      1. Accelerate from v_entry toward v_target
      2. Cruise at constant speed
      3. Brake from brake_start_m before the end of the straight

    Spec note: If v_target < v_entry, the car continues at v_entry (no
    deceleration until the brake point).

    Args:
        v_entry:        Speed entering the straight (m/s)
        v_target:       Desired target speed for the straight (m/s)
        length:         Total length of the straight segment (m)
        accel:          Constant acceleration rate (m/s^2)
        decel:          Constant braking deceleration rate (m/s^2, positive)
        brake_start_m:  Distance before the end of the straight to begin braking (m)

    Returns:
        (total_time, exit_speed) — time in seconds and speed at end of straight in m/s
    """
    # Spec: if target < entry speed, car continues at entry speed
    effective_target = max(v_entry, v_target)

    # Distance available before braking begins
    d_before_brake = length - brake_start_m

    # Edge case: brake point is at or before the start of the straight
    if d_before_brake <= 0:
        v_exit_sq = v_entry**2 - 2 * decel * length
        v_exit = math.sqrt(max(v_exit_sq, 0))
        time = get_time_to_reach_speed(v_entry, v_exit, decel)
        return (time, v_exit)

    # --- Phase 1: Acceleration ---
    d_accel_needed = get_distance_to_reach_speed(v_entry, effective_target, accel)

    if d_accel_needed <= d_before_brake:
        # Reach target speed before brake point
        v_at_brake = effective_target
        t_accel = get_time_to_reach_speed(v_entry, effective_target, accel)

        # --- Phase 2: Cruise at constant speed ---
        d_cruise = d_before_brake - d_accel_needed
        t_cruise = d_cruise / effective_target if effective_target > 0 else 0
    else:
        # Cannot reach target speed — accelerate for all of d_before_brake
        v_at_brake = math.sqrt(v_entry**2 + 2 * accel * d_before_brake)
        t_accel = get_time_to_reach_speed(v_entry, v_at_brake, accel)

        # No cruise phase
        t_cruise = 0

    # --- Phase 3: Braking ---
    v_exit_sq = v_at_brake**2 - 2 * decel * brake_start_m
    v_exit = math.sqrt(max(v_exit_sq, 0))
    t_brake = get_time_to_reach_speed(v_at_brake, v_exit, decel)

    return (t_accel + t_cruise + t_brake, v_exit)


def get_time_for_corner(speed, length):
    """
    Corners are traversed at constant speed (no acceleration/deceleration).

    Args:
        speed:  Constant speed through the corner (m/s)
        length: Arc length of the corner (m)

    Returns:
        Time to traverse the corner in seconds.
    """
    if speed <= 0:
        return float('inf')
    return length / speed
