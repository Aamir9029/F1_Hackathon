from dataclasses import dataclass
from typing import List, Dict
import json
import sys
import os
from car_obj import Car
from race_obj import Race
from track_segments_obj import Track
from tyre_objects import TyreCompound, TyreSet
from weather_objects import WeatherCondition

@dataclass
class Telemetry:
    car: Car
    race: Race
    track: Track
    tyre_properties: Dict[str, TyreCompound]
    available_sets: List[TyreSet]
    weather_conditions: List[WeatherCondition]

    @classmethod
    def load_from_json(cls, file_path: str):
        """Parses the JSON file and constructs the full object hierarchy."""
        with open(file_path, 'r') as file:
            raw_data = json.load(file)

        # Map Tyres dict
        tyres_raw = raw_data.get("tyres", {}).get("properties", {})
        tyre_props = {name: TyreCompound.from_dict(props) for name, props in tyres_raw.items()}

        # Map Available Sets list
        sets_raw = raw_data.get("available_sets", [])
        avail_sets = [TyreSet.from_dict(ts) for ts in sets_raw]

        # Map Weather list
        weather_raw = raw_data.get("weather", {}).get("conditions", [])
        weather_conds = [WeatherCondition.from_dict(wc) for wc in weather_raw]

        return cls(
            car=Car.from_dict(raw_data.get("car", {})),
            race=Race.from_dict(raw_data.get("race", {})),
            track=Track.from_dict(raw_data.get("track", {})),
            tyre_properties=tyre_props,
            available_sets=avail_sets,
            weather_conditions=weather_conds
        )

# --- Execution ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scanner.py <telemetry_file.txt>")
        sys.exit(1)
        
    target_file = sys.argv[1]
    
    if not os.path.exists(target_file):
        print(f"Error: The file '{target_file}' was not found in the project root.")
        sys.exit(1)

    # Load the telemetry into our strictly typed objects
    race_weekend = Telemetry.load_from_json(target_file)
    print(f"Target telemetry '{target_file}' successfully loaded!")
    
    # print("\n=== RACE ===")
    # for key, value in vars(race_weekend.race).items():
    #      print(f"  {key}: {value}")

    # print("\n=== CAR ===")
    # for key, value in vars(race_weekend.car).items():
    #     print(f"  {key}: {value}")
        
    # print("\n=== TRACK ===")
    # print(f"  Name: {race_weekend.track.name}")
    # print(f"  Total Segments: {len(race_weekend.track.segments)}")
    # for seg in race_weekend.track.segments:
    #     radius_str = f", radius: {seg.radius_m}m" if seg.radius_m else ""
    #     print(f"    Segment {seg.id}: {seg.type} (length: {seg.length_m}m{radius_str})")

    # print("\n=== TYRE COMPOUNDS ===")
    # for name, props in race_weekend.tyre_properties.items():
    #     print(f"  Compound: {name}")
    #     for key, value in vars(props).items():
    #         print(f"    {key}: {value}")

    # print("\n=== AVAILABLE TYRE SETS ===")
    # for t_set in race_weekend.available_sets:
    #     print(f"  Set IDs {t_set.ids} -> Compound: {t_set.compound}")

    # print("\n=== WEATHER CONDITIONS ===")
    # for weather in race_weekend.weather_conditions:
    #     print(f"  Condition ID {weather.id}: {weather.condition} (duration: {weather.duration_s}s)")
    #     for key, value in vars(weather).items():
    #         if key not in ['id', 'condition', 'duration_s']:
    #             print(f"    {key}: {value}")