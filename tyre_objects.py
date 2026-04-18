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

@dataclass
class TyreSet:
    ids: List[int]
    compound: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)