from dataclasses import dataclass

@dataclass
class Car:
    max_speed_m_s: float
    accel_m_se2: float
    brake_m_se2: float
    limp_constant_m_s: float
    crawl_constant_m_s: float
    fuel_tank_capacity_l: float
    initial_fuel_l: float
    fuel_consumption_l_m: float

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            max_speed_m_s=data.get("max_speed_m/s", 0.0),
            accel_m_se2=data.get("accel_m/se2", 0.0),
            brake_m_se2=data.get("brake_m/se2", 0.0),
            limp_constant_m_s=data.get("limp_constant_m/s", 0.0),
            crawl_constant_m_s=data.get("crawl_constant_m/s", 0.0),
            fuel_tank_capacity_l=data.get("fuel_tank_capacity_l", 0.0),
            initial_fuel_l=data.get("initial_fuel_l", 0.0),
            fuel_consumption_l_m=data.get("fuel_consumption_l/m", 0.0)
        )
