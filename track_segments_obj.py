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

@dataclass
class Track:
    name: str
    segments: List[Segment]

    @classmethod
    def from_dict(cls, data: dict):
        segments = [Segment.from_dict(seg) for seg in data.get("segments", [])]
        return cls(name=data.get("name", ""), segments=segments)