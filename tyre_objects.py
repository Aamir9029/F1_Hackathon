from dataclasses import dataclass
from typing import List

@dataclass
class TyreCompound:
    life_span: int
    dry_friction_multiplier: float
    cold_friction_multiplier: float
    light_rain_friction_multiplier: float
    heavy_rain_friction_multiplier: float
    dry_degradation: float
    cold_degradation: float
    light_rain_degradation: float
    heavy_rain_degradation: float

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def to_dict(self) -> dict:
        return {
            "life_span": self.life_span,
            "dry_friction_multiplier": self.dry_friction_multiplier,
            "cold_friction_multiplier": self.cold_friction_multiplier,
            "light_rain_friction_multiplier": self.light_rain_friction_multiplier,
            "heavy_rain_friction_multiplier": self.heavy_rain_friction_multiplier,
            "dry_degradation": self.dry_degradation,
            "cold_degradation": self.cold_degradation,
            "light_rain_degradation": self.light_rain_degradation,
            "heavy_rain_degradation": self.heavy_rain_degradation
        }

@dataclass
class TyreSet:
    ids: List[int]
    compound: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def to_dict(self) -> dict:
        return {"ids": self.ids, "compound": self.compound}