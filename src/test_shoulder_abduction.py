import unittest
import math
from shoulder_calculations import *

import unittest
import math

# Calculated
# def calc_shoulder_abduction(elbow, shoulder_center):

class Landmark:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class TestShoulderAbduction(unittest.TestCase):
    def test_calc_external_rotation_invalid_input_types(self):
        # Test case with None passed as input
        shoulder_center = Landmark(1, 1)
        result = calc_shoulder_abduction(None, shoulder_center)
        self.assertEqual(result, None)

    # def test_shoulder_abduction_with_valid_input(self):
    #     elbow = Landmark(x=10, y=20)
    #     shoulder_center = Landmark(x=0, y=0)
    #     result = calc_shoulder_abduction(elbow, shoulder_center)
    #     self.assertAlmostEqual(result, math.degrees(math.atan2(20, 10)), delta=0.1)

    # def test_shoulder_abduction_with_elbow_at_shoulder_center(self):
    #     elbow = Landmark(x=0, y=0)
    #     shoulder_center = Landmark(x=0, y=0)
    #     result = calc_shoulder_abduction(elbow, shoulder_center)
    #     self.assertEqual(result, 0)

    # def test_shoulder_abduction_with_elbow_above_shoulder_center(self):
    #     elbow = Landmark(x=0, y=10)
    #     shoulder_center = Landmark(x=0, y=0)
    #     result = calc_shoulder_abduction(elbow, shoulder_center)
    #     self.assertEqual(result, 90)

    # def test_shoulder_abduction_with_elbow_below_shoulder_center(self):
    #     elbow = Landmark(x=0, y=-10)
    #     shoulder_center = Landmark(x=0, y=0)
    #     result = calc_shoulder_abduction(elbow, shoulder_center)
    #     self.assertEqual(result, -90)

    # def test_shoulder_abduction_with_elbow_to_the_right_of_shoulder_center(self):
    #     elbow = Landmark(x=10, y=0)
    #     shoulder_center = Landmark(x=0, y=0)
    #     result = calc_shoulder_abduction(elbow, shoulder_center)
    #     self.assertEqual(result, 0)

    # def test_shoulder_abduction_with_elbow_to_the_left_of_shoulder_center(self):
    #     elbow = Landmark(x=-10, y=0)
    #     shoulder_center = Landmark(x=0, y=0)
    #     result = calc_shoulder_abduction(elbow, shoulder_center)
    #     self.assertEqual(result, 180)

if __name__ == '__main__':
    unittest.main()

