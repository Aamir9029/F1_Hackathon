import unittest
from src.physics.kinematics import get_max_corner_speed, get_time_to_reach_speed, get_distance_to_reach_speed
from src.physics.resources import calculate_fuel_usage, get_current_friction

class TestPhysics(unittest.TestCase):

    def test_max_corner_speed_example(self):
        # Example from Page 7: friction 0.9, gravity 9.8, radius 50, crawl 10
        # Expected: 31 m/s
        speed = get_max_corner_speed(0.9, 50, 10)
        self.assertAlmostEqual(speed, 31.0, places=1)

    def test_fuel_usage_example(self):
        # Example from Page 6: v_i 50, v_f 70, distance 800
        # Expected: 0.40432 litres
        fuel = calculate_fuel_usage(50, 70, 800)
        self.assertAlmostEqual(fuel, 0.40432, places=5)

    def test_kinematics_time(self):
        # v_i 0, v_f 10, accel 2 -> time should be 5
        self.assertEqual(get_time_to_reach_speed(0, 10, 2), 5)

    def test_friction_calculation(self):
        # Example from Page 5: Soft tyre (1.8), degradation 0.5, dry weather (1.0)
        # Expected: 1.3
        friction = get_current_friction(1.8, 0.5, 1.0)
        self.assertEqual(friction, 1.3)

if __name__ == '__main__':
    unittest.main()
