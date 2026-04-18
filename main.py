import json
import sys
import os
from scanner import Telemetry
from src.physics.kinematics import (
    get_max_corner_speed,
    get_distance_to_reach_speed,
    get_time_for_straight,
    get_time_for_corner
)
from src.scoring.score import (
    calculate_level1_score,
    calculate_level2_score,
    calculate_level3_score,
    calculate_level4_score
)

from src.algorithms.strategy import build_strategy


def run_level_1_simulation(json_path):
    race_weekend = Telemetry.load_from_json(json_path)
    car = race_weekend.car
    segments = race_weekend.track.segments
    num_laps = race_weekend.race.laps

    # Simple Strategist Logic for Level 1
    # 1. Determine max safe speed for all corners first
    safe_speeds = {}
    for seg in segments:
        if seg.type == 'corner':
            # Level 1: Assume base friction is 1.0 for now
            safe_speeds[seg.id] = get_max_corner_speed(1.0, seg.radius_m, car.crawl_constant_m_s)

    # 2. Build the segment actions for a single lap (reused each lap for Level 1)
    lap_segments = []
    for i, seg in enumerate(segments):
        if seg.type == 'straight':
            target_speed = car.max_speed_m_s
            seg_action = {
                "id": seg.id,
                "type": "straight",
                "target_m/s": target_speed
            }

            # Look ahead: how much must we slow down for the NEXT segment?
            next_seg = segments[i+1] if i+1 < len(segments) else None
            if next_seg and next_seg.type == 'corner':
                exit_speed = safe_speeds[next_seg.id]

                # Use Physicist's math to find braking distance
                # Distance = (v_final^2 - v_initial^2) / (2 * a)
                braking_dist = get_distance_to_reach_speed(target_speed, exit_speed, car.brake_m_se2)
                seg_action["brake_start_m_before_next"] = round(braking_dist, 2)

            lap_segments.append(seg_action)
        else:
            # Corner segments are pass-through
            lap_segments.append({
                "id": seg.id,
                "type": "corner"
            })

    # 3. Build the full race output with all laps
    initial_tyre_id = race_weekend.available_sets[0].ids[0] if race_weekend.available_sets else 1

    laps = []
    for lap_num in range(1, num_laps + 1):
        laps.append({
            "lap": lap_num,
            "segments": lap_segments,
            "pit": {
                "enter": False
            }
        })

    output = {
        "initial_tyre_id": initial_tyre_id,
        "laps": laps
    }

    return output, race_weekend


def simulate_race_time(strategy: dict, race_weekend) -> float:
    """
    Simulates the total race time by replaying the strategy through
    the physics engine.

    Returns:
        Total race time in seconds.
    """
    car = race_weekend.car
    segments = race_weekend.track.segments

    # Build a lookup from segment id -> segment object
    seg_lookup = {seg.id: seg for seg in segments}

    total_time = 0.0
    current_speed = 0.0  # Race starts at 0 m/s

    for lap in strategy["laps"]:
        for seg_action in lap["segments"]:
            seg_id = seg_action["id"]
            seg_obj = seg_lookup[seg_id]

            if seg_action["type"] == "straight":
                target_speed = seg_action.get("target_m/s", car.max_speed_m_s)
                brake_start = seg_action.get("brake_start_m_before_next", 0.0)

                seg_time, exit_speed = get_time_for_straight(
                    v_entry=current_speed,
                    v_target=target_speed,
                    length=seg_obj.length_m,
                    accel=car.accel_m_se2,
                    decel=car.brake_m_se2,
                    brake_start_m=brake_start
                )
                total_time += seg_time
                current_speed = exit_speed

            elif seg_action["type"] == "corner":
                # Corner is taken at constant entry speed
                seg_time = get_time_for_corner(current_speed, seg_obj.length_m)
                total_time += seg_time
                # Speed stays constant through corners

    return total_time


def detect_level(json_path: str) -> int:
    """
    Detects the level number from the input filename.
    Defaults to 1 if it can't be determined.
    """
    basename = os.path.basename(json_path)
    name = os.path.splitext(basename)[0]

    # Try to extract the number from the filename (e.g. "1.txt" -> 1, "3.txt" -> 3)
    try:
        return int(name)
    except ValueError:
        return 1


if __name__ == "__main__":
    target_file = '1.txt' if len(sys.argv) < 2 else sys.argv[1]

    if not os.path.exists(target_file):
        print(f"Error: Could not find telemetry file '{target_file}'.")
        sys.exit(1)

    # Build strategy
    strategy, race_weekend = run_level_1_simulation(target_file)

    # Simulate race time
    total_race_time = simulate_race_time(strategy, race_weekend)
    time_ref = race_weekend.race.time_reference_s
    level = detect_level(target_file)

    # Calculate score based on detected level
    if level == 1:
        score = calculate_level1_score(time_ref, total_race_time)
    elif level in (2, 3):
        # Fuel tracking not yet implemented — use 0 as placeholder
        fuel_used = 0.0
        fuel_cap = race_weekend.race.fuel_soft_cap_limit_l
        score = calculate_level2_score(time_ref, total_race_time, fuel_used, fuel_cap)
    elif level == 4:
        fuel_used = 0.0
        fuel_cap = race_weekend.race.fuel_soft_cap_limit_l
        total_degradation = 0.0
        blowouts = 0
        score = calculate_level4_score(time_ref, total_race_time, fuel_used, fuel_cap, total_degradation, blowouts)
    else:
        score = calculate_level1_score(time_ref, total_race_time)

    # Write JSON output
    json_output_file = f"output_{level}.json"
    with open(json_output_file, 'w') as f:
        json.dump(strategy, f, indent=2)

    # Write score txt file
    score_output_file = f"level{level}_score.txt"
    with open(score_output_file, 'w') as f:
        f.write(f"Score: {score:.2f}\n")
        f.write(f"Race Time: {total_race_time:.2f}s\n")

    # Print summary
    print(f"Level:           {level}")
    print(f"Race Time:       {total_race_time:.2f}s")
    print(f"Reference Time:  {time_ref:.2f}s")
    print(f"Score:           {score:.2f}")
    print(f"JSON output:     {json_output_file}")
    print(f"Score output:    {score_output_file}")
