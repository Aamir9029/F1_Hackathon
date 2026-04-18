from dataclasses import dataclass

# --- 5. Weather Objects ---
@dataclass
class WeatherCondition:
    id: int
    condition: str
    duration_s: float
    acceleration_multiplier: float
    deceleration_multiplier: float

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)