import json
from src.physics.kinematics import get_max_corner_speed, get_distance_to_reach_speed

def run_level_1_simulation(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    car = data['car']
    segments = data['track']['segments']
    
    # Simple Strategist Logic for Level 1
    # 1. Determine max safe speed for all corners first
    safe_speeds = {}
    for seg in segments:
        if seg['type'] == 'corner':
            # Level 1: Assume base friction is 1.0 for now
            safe_speeds[seg['id']] = get_max_corner_speed(1.0, seg['radius_m'], car['crawl_constant_m/s'])

    # 2. Generate actions for straights
    actions = []
    for i, seg in enumerate(segments):
        if seg['type'] == 'straight':
            target_speed = car['max_speed_m/s']
            
            # Look ahead: how much must we slow down for the NEXT segment?
            next_seg = segments[i+1] if i+1 < len(segments) else None
            if next_seg and next_seg['type'] == 'corner':
                exit_speed = safe_speeds[next_seg['id']]
                
                # Use Physicist's math to find braking distance
                # Distance = (v_final^2 - v_initial^2) / (2 * a)
                braking_dist = get_distance_to_reach_speed(target_speed, exit_speed, car['brake_m/se2'])
                
                print(f"Segment {seg['id']} (Straight): Target {target_speed}m/s, must start braking {braking_dist:.2f}m before the corner.")
                
                actions.append({
                    "id": seg['id'],
                    "target_m/s": target_speed,
                    "brake_start_m_before_next": round(braking_dist, 2)
                })
    
    return actions

if __name__ == "__main__":
    results = run_level_1_simulation('data/mock_level.json')
    print("\nGenerated Strategist Actions:", json.dumps(results, indent=2))
