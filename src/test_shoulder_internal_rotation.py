import unittest
import math
from shoulder_calculations import *

import unittest
import math

# Calculated Internal Rotation
# def calc_shoulder_internal_rotation(wrist,shoulder_center):

class Landmark:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class TestShoulderInternalRotation(unittest.TestCase):

    def test_calc_internal_rotation_invalid_input_types(self):
        # Test case with None passed as input
        shoulder_center = Landmark(1, 1)
        result = calc_shoulder_internal_rotation(None, shoulder_center)
        self.assertEqual(result, None)

    # def test_calc_shoulder_internal_rotation_zero_degrees(self):
    #     wrist = Landmark(0, 0)
    #     shoulder_center = Landmark(0, 1)
    #     expected_result = 0
    #     self.assertAlmostEqual(calc_shoulder_internal_rotation(wrist, shoulder_center), expected_result, places=2)

    # def test_calc_shoulder_internal_rotation_45_degrees(self):
    #     wrist = Landmark(1, 1)
    #     shoulder_center = Landmark(0, 0)
    #     expected_result = 45
    #     self.assertAlmostEqual(calc_shoulder_internal_rotation(wrist, shoulder_center), expected_result, places=2)

    # def test_calc_shoulder_internal_rotation_60_degrees(self):
    #     wrist = Landmark(1, math.sqrt(3))
    #     shoulder_center = Landmark(0, 0)
    #     expected_result = 60
    #     self.assertAlmostEqual(calc_shoulder_internal_rotation(wrist, shoulder_center), expected_result, places=2)

    # def test_calc_shoulder_internal_rotation_90_degrees(self):
    #     wrist = Landmark(1, 0)
    #     shoulder_center = Landmark(0, 0)
    #     expected_result = 90
    #     self.assertAlmostEqual(calc_shoulder_internal_rotation(wrist, shoulder_center), expected_result, places=2)

if __name__ == '__main__':
    unittest.main()

