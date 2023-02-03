import unittest
import math
from shoulder_calculations import *

import unittest
import math

# Calculated
# External Rotationn
# def calc_shoulder_external_rotation(wrist,shoulder_center):

class Landmark:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class TestShoulderExternalRotation(unittest.TestCase):

    def test_calc_external_rotation_invalid_input_types(self):
        # Test case with None passed as input
        shoulder_center = Landmark(1, 1)
        result = calc_shoulder_external_rotation(None, shoulder_center)
        self.assertEqual(result, None)

    # def test_shoulder_external_rotation_90(self):
    #     wrist = (0,0)
    #     shoulder_center = (1,1)
    #     self.assertEqual(math.degrees(math.atan2(wrist.y - shoulder_center.y, wrist.x - shoulder_center.x)), 90)
    #     self.assertEqual(calc_shoulder_external_rotation(wrist, shoulder_center), 90)

    # def test_shoulder_external_rotation_120(self):
    #     wrist = (0,0)
    #     shoulder_center = (math.sqrt(3),1)
    #     self.assertEqual(math.degrees(math.atan2(wrist.y - shoulder_center.y, wrist.x - shoulder_center.x)), 120)
    #     self.assertEqual(calc_shoulder_external_rotation(wrist, shoulder_center), 120)

    # def test_shoulder_external_rotation_150(self):
    #     wrist = (0,0)
    #     shoulder_center = (2,0)
    #     self.assertEqual(math.degrees(math.atan2(wrist.y - shoulder_center.y, wrist.x - shoulder_center.x)), 150)
    #     self.assertEqual(calc_shoulder_external_rotation(wrist, shoulder_center), 150)

    # def test_shoulder_external_rotation_0(self):
    #     wrist = (0,0)
    #     shoulder_center = (0,1)
    #     self.assertEqual(math.degrees(math.atan2(wrist.y - shoulder_center.y, wrist.x - shoulder_center.x)), 0)
    #     self.assertEqual(calc_shoulder_external_rotation(wrist, shoulder_center), 0)

    # def test_shoulder_external_rotation_30(self):
    #     wrist = (0,0)
    #     shoulder_center = (math.sqrt(3)/2,0.5)
    #     self.assertEqual(math.degrees(math.atan2(wrist.y - shoulder_center.y, wrist.x - shoulder_center.x)), 30)
    #     self.assertEqual(calc_shoulder_external_rotation(wrist, shoulder_center), 30)

    # def test_shoulder_external_rotation_60(self):
    #     wrist = (0,0)
    #     shoulder_center = (1,0)
    #     self.assertEqual(math.degrees(math.atan2(wrist.y - shoulder_center.y, wrist.x - shoulder_center.x)), 60)
    #     self.assertEqual(calc_shoulder_external_rotation(wrist, shoulder_center), 60)

if __name__ == '__main__':
    unittest.main()