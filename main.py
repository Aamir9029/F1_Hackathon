import json
import sys
import os
from scanner import Telemetry
import sys

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

    return output

if __name__ == "__main__":
    target_file = '1.txt' if len(sys.argv) < 2 else sys.argv[1]

    if not os.path.exists(target_file):
        print(f"Error: Could not find telemetry file '{target_file}'.")
        sys.exit(1)

    result = run_level_1_simulation(target_file)
    print(json.dumps(result, indent=2))
