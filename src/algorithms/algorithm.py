from src.physics.kinematics import get_distance_to_reach_speed, get_max_corner_speed


def _get_value(mapping, *keys, default=None):
    for key in keys:
        if key in mapping:
            return mapping[key]
    return default


def _extract_car_stats(car):
    return {
        "max_speed": _get_value(car, "max_speed_m/s", "max_speed_mps", default=50.0),
        "accel": _get_value(car, "accel_m/se2", "accel_mps2", default=5.0),
        "brake": _get_value(car, "brake_m/se2", "brake_mps2", default=5.0),
        "crawl": _get_value(car, "crawl_constant_m/s", "crawl_constant_mps", default=1.0),
    }


def _calculate_peak_speed(entry_speed, corner_speed, straight_length, accel_rate, brake_rate, max_speed):
    if accel_rate <= 0 or brake_rate <= 0:
        return max_speed

    accel_term = 1.0 / (2.0 * accel_rate)
    brake_term = 1.0 / (2.0 * brake_rate)
    denominator = accel_term + brake_term

    if denominator <= 0:
        return max_speed

    numerator = straight_length + (entry_speed**2) * accel_term + (corner_speed**2) * brake_term
    peak_speed_sq = max(0.0, numerator / denominator)
    return min(max_speed, peak_speed_sq**0.5)


def plan_straight_action(car, straight, next_segment, entry_speed, tyre_friction):
    """Return the action for a straight and the speed leaving the segment."""

    stats = _extract_car_stats(car)
    max_speed = stats["max_speed"]
    accel = stats["accel"]
    brake = stats["brake"]
    crawl = stats["crawl"]
    length = straight["length_m"]

    next_corner_speed = None
    if next_segment and next_segment["type"] == "corner" and "radius_m" in next_segment:
        next_corner_speed = min(max_speed, get_max_corner_speed(tyre_friction, next_segment["radius_m"], crawl))

    if next_corner_speed is not None:
        distance_to_max = get_distance_to_reach_speed(entry_speed, max_speed, accel)
        braking_from_max = get_distance_to_reach_speed(next_corner_speed, max_speed, brake)

        if distance_to_max + braking_from_max <= length:
            target_speed = max_speed
            brake_start = braking_from_max
        else:
            target_speed = _calculate_peak_speed(
                entry_speed,
                next_corner_speed,
                length,
                accel,
                brake,
                max_speed,
            )
            brake_start = get_distance_to_reach_speed(next_corner_speed, target_speed, brake)

        exit_speed = next_corner_speed
    else:
        target_speed = max_speed
        brake_start = 0.0
        exit_speed = target_speed

    action = {
        "id": straight["id"],
        "type": "straight",
        "target_m/s": round(target_speed, 3),
        "brake_start_m_before_next": round(brake_start, 3),
    }

    return action, exit_speed


def handle_corner(car, corner, entry_speed, safe_corner_speed=None):
    """Return the corner action and the speed leaving the corner."""

    exit_speed = entry_speed if safe_corner_speed is None else min(entry_speed, safe_corner_speed)
    action = {
        "id": corner["id"],
        "type": "corner",
    }

    return action, exit_speed