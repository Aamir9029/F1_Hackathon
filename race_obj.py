from dataclasses import dataclass

@dataclass
class Race:
    name: str
    laps: int
    base_pit_stop_time_s: float
    pit_tyre_swap_time_s: float
    pit_refuel_rate_l_s: float
    corner_crash_penalty_s: float
    pit_exit_speed_m_s: float
    fuel_soft_cap_limit_l: float
    starting_weather_condition_id: int
    time_reference_s: float

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data.get("name", ""),
            laps=data.get("laps", 0),
            base_pit_stop_time_s=data.get("base_pit_stop_time_s", 0.0),
            pit_tyre_swap_time_s=data.get("pit_tyre_swap_time_s", 0.0),
            pit_refuel_rate_l_s=data.get("pit_refuel_rate_l/s", 0.0),
            corner_crash_penalty_s=data.get("corner_crash_penalty_s", 0.0),
            pit_exit_speed_m_s=data.get("pit_exit_speed_m/s", 0.0),
            fuel_soft_cap_limit_l=data.get("fuel_soft_cap_limit_l", 0.0),
            starting_weather_condition_id=data.get("starting_weather_condition_id", 0),
            time_reference_s=data.get("time_reference_s", 0.0)
        )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "laps": self.laps,
            "base_pit_stop_time_s": self.base_pit_stop_time_s,
            "pit_tyre_swap_time_s": self.pit_tyre_swap_time_s,
            "pit_refuel_rate_l/s": self.pit_refuel_rate_l_s,
            "corner_crash_penalty_s": self.corner_crash_penalty_s,
            "pit_exit_speed_m/s": self.pit_exit_speed_m_s,
            "fuel_soft_cap_limit_l": self.fuel_soft_cap_limit_l,
            "starting_weather_condition_id": self.starting_weather_condition_id,
            "time_reference_s": self.time_reference_s
        }

