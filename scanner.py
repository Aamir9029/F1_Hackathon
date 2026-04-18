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

    def to_dict(self) -> dict:
        """Serializes the full Telemetry object back to the canonical JSON format."""
        return {
            "car": self.car.to_dict(),
            "race": self.race.to_dict(),
            "track": self.track.to_dict(),
            "tyres": {
                "properties": {
                    compound: props.to_dict()
                    for compound, props in self.tyre_properties.items()
                }
            },
            "available_sets": [ts.to_dict() for ts in self.available_sets],
            "weather": {
                "conditions": [wc.to_dict() for wc in self.weather_conditions]
            }
        }

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

    # Serialize back to canonical JSON format and write to file
    base_name = os.path.splitext(os.path.basename(target_file))[0]
    output_file = f"parsed_{base_name}.json"
    with open(output_file, 'w') as f:
        json.dump(race_weekend.to_dict(), f, indent=2)
    print(f"Parsed telemetry written to '{output_file}'")
