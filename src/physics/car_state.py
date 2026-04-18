from .resources import (
    calculate_total_straight_fuel, 
    get_straight_degradation, 
    get_braking_degradation, 
    get_corner_degradation,
    get_current_friction
)
from .data_models import get_tyre_specs

class CarState:
    def __init__(self, initial_fuel, initial_tyre_set, car_config):
        self.fuel = initial_fuel
        self.tyre_set = initial_tyre_set # Expecting a dict with {'id', 'compound', 'degradation'}
        self.car_config = car_config
        
        self.total_time = 0.0
        self.is_limp_mode = False
        self.is_crawl_mode = False
        self.total_distance = 0.0

    def apply_straight(self, segment_data, solve_result, tyre_deg_rate, weather_mults):
        """
        Updates the car state after a straight segment.
        solve_result: (d_accel, d_cruise, d_brake, segment_time) from kinematics
        """
        d_accel, d_cruise, d_brake, segment_time = solve_result
        length = segment_data['length_m']
        
        # 1. Update Time and Distance
        self.total_time += segment_time
        self.total_distance += length
        
        # 2. Calculate and subtract fuel
        # Level 1/2: entry speed is v_initial, exit is v_exit
        # For simplicity in this state tracker, we assume we know the speeds from the solver
        # Note: In a real simulation, we'd pass the actual speeds here
        
        # 3. Update Tyre Degradation
        # Degradation = Straight + Braking
        deg_straight = get_straight_degradation(tyre_deg_rate, length)
        # For Level 4, braking degradation is significant
        # we'll need the speeds from the solver to be perfect
        
        self.tyre_set['degradation'] += deg_straight
        
        # 4. Check for Blowout or Empty Fuel -> Limp Mode
        if self.tyre_set['degradation'] >= 1.0 or self.fuel <= 0:
            self.is_limp_mode = True

    def apply_pit_stop(self, pit_time, new_tyre_set=None, refuel_amount=0):
        self.total_time += pit_time
        if new_tyre_set:
            self.tyre_set = new_tyre_set
            self.is_limp_mode = False # Pitting fixes Limp Mode
        
        self.fuel = min(self.car_config['fuel_tank_capacity_l'], self.fuel + refuel_amount)
        if self.fuel > 0 and self.tyre_set['degradation'] < 1.0:
            self.is_limp_mode = False

    def get_current_friction(self, weather_condition):
        base, mult, _ = get_tyre_specs(self.tyre_set['compound'], weather_condition)
        return get_current_friction(base, self.tyre_set['degradation'], mult)
