import unittest
import math
from shoulder_calculations import *

import unittest
import math

# Calculated Flexion
# def calc_shoulder_flexion(elbow, shoulder_center, hip):

class Landmark:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class TestShoulderFlexion(unittest.TestCase):

    def test_calc_shoulder_flexion_invalid_input_types(self):
        # Test case with None passed as input
        elbow = None
        shoulder_center = Landmark(1, 1)
        hip = Landmark(2, 2)
        result = calc_shoulder_flexion(elbow, shoulder_center, hip)
        self.assertEqual(result, None)

    # def test_calc_shoulder_flexion_negative_values(self):
    #     elbow = Landmark(-1, -1)
    #     shoulder_center = Landmark(1, 1)
    #     hip = Landmark(0, 0)
    #     self.assertEqual(calc_shoulder_flexion(elbow, shoulder_center, hip), 45)

    # def test_calc_shoulder_flexion_float_values(self):
    #     elbow = Landmark(0.5, 0.5)
    #     shoulder_center = Landmark(1.5, 1.5)
    #     hip = Landmark(1, 1)
    #     self.assertEqual(calc_shoulder_flexion(elbow, shoulder_center, hip), 45)

    # def test_calc_shoulder_flexion_upper_limit(self):
    #     elbow = Landmark(0, 0)
    #     shoulder_center = Landmark(-1, 0)
    #     hip = Landmark(0, 0)
    #     self.assertEqual(calc_shoulder_flexion(elbow, shoulder_center, hip), 180)

    # def test_calc_shoulder_flexion_common_issues(self):
    #     elbow = Landmark(0, 0)
    #     shoulder_center = Landmark(1, 1)
    #     hip = Landmark(0, 0)
    #     self.assertEqual(calc_shoulder_flexion(elbow, shoulder_center, hip), 45)

    #     elbow = Landmark(0, 0)
    #     shoulder_center = Landmark(0, 1)
    #     hip = Landmark(0, 0)
    #     self.assertEqual(calc_shoulder_flexion(elbow, shoulder_center, hip), 90)

    # def test_calc_shoulder_flexion_0_degrees(self):
    #     elbow = Landmark(0, 0)
    #     shoulder_center = Landmark(1, 0)
    #     hip = Landmark(0, 0)
    #     self.assertEqual(calc_shoulder_flexion(elbow, shoulder_center, hip), 0)

    # def test_calc_shoulder_flexion_45_degrees(self):
    #     elbow = Landmark(0, 0)
    #     shoulder_center = Landmark(math.sqrt(2)/2, math.sqrt(2)/2)
    #     hip = Landmark(0, 0)
    #     self.assertEqual(calc_shoulder_flexion(elbow, shoulder_center, hip), 45)

    # def test_calc_shoulder_flexion_60_degrees(self):
    #     elbow = Landmark(0, 0)
    #     shoulder_center = Landmark(math.sqrt(3)/2, 0.5)
    #     hip = Landmark(0, 0)
    #     self.assertEqual(calc_shoulder_flexion(elbow, shoulder_center, hip), 60)

    # def test_calc_shoulder_flexion_90_degrees(self):
    #     elbow = Landmark(0, 0)
    #     shoulder_center = Landmark(1, 0)
    #     hip = Landmark(0, 0)
    #     self.assertEqual(calc_shoulder_flexion(elbow, shoulder_center, hip), 90)

if __name__ == '__main__':
    unittest.main()

