from dataclasses import dataclass
from typing import List, Optional

# --- 3. Track & Segment Objects ---
@dataclass
class Segment:
    id: int
    type: str
    length_m: float
    radius_m: Optional[float] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id", 0),
            type=data.get("type", ""),
            length_m=data.get("length_m", 0.0),
            radius_m=data.get("radius_m") # Will be None for straights
        )

    def to_dict(self) -> dict:
        d = {"id": self.id, "type": self.type, "length_m": self.length_m}
        if self.radius_m is not None:
            d["radius_m"] = self.radius_m
        return d

@dataclass
class Track:
    name: str
    segments: List[Segment]

    @classmethod
    def from_dict(cls, data: dict):
        segments = [Segment.from_dict(seg) for seg in data.get("segments", [])]
        return cls(name=data.get("name", ""), segments=segments)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "segments": [seg.to_dict() for seg in self.segments]
        }