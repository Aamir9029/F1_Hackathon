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

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "condition": self.condition,
            "duration_s": self.duration_s,
            "acceleration_multiplier": self.acceleration_multiplier,
            "deceleration_multiplier": self.deceleration_multiplier
        }