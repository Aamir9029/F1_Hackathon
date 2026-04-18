import json
import sys

from src.algorithms.strategy import build_strategy

def run_level_1_simulation(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    return build_strategy(data)

if __name__ == "__main__":
    json_path = sys.argv[1] if len(sys.argv) > 1 else 'data/mock_level.json'
    results = run_level_1_simulation(json_path)
    print(json.dumps(results, indent=2))
