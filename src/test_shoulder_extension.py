import unittest
import math
from shoulder_calculations import *

import unittest
import math

# Calculated
# calc_shoulder_extension(elbow, shoulder_center)

class Landmark:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class TestShoulderExtension(unittest.TestCase):

    def test_calc_external_rotation_invalid_input_types(self):
        # Test case with None passed as input
        shoulder_center = Landmark(1, 1)
        result = calc_shoulder_extension(None, shoulder_center)
        self.assertEqual(result, None)

    # def test_normal_case(self):
    #     elbow = Landmark(0, 0)
    #     shoulder_center = Landmark(1, 1)
    #     result = calc_shoulder_extension(elbow, shoulder_center)
    #     self.assertAlmostEqual(result, 135.0, delta=0.1)

    # def test_shoulder_center_below_elbow(self):
    #     elbow = Landmark(0, 1)
    #     shoulder_center = Landmark(1, 0)
    #     result = calc_shoulder_extension(elbow, shoulder_center)
    #     self.assertAlmostEqual(result, 45.0, delta=0.1)

    # def test_elbow_below_shoulder_center(self):
    #     elbow = Landmark(1, 0)
    #     shoulder_center = Landmark(0, 1)
    #     result = calc_shoulder_extension(elbow, shoulder_center)
    #     self.assertAlmostEqual(result, 225.0, delta=0.1)

    # def test_input_does_not_cause_error(self):
    #     elbow = Landmark(0, 0)
    #     shoulder_center = Landmark(0, 0)
    #     result = calc_shoulder_extension(elbow, shoulder_center)
    #     self.assertEqual(result, {})

    # def test_shoulder_extension_0():
    #     elbow = Landmark(0,0)
    #     shoulder_center = Landmark(0,1)
    #     result = calc_shoulder_extension(elbow, shoulder_center)
    #     assert result == 0.0, f'Expected 0.0, but got {result}'

    # def test_shoulder_extension_30():
    #     elbow = Landmark(0.5, 0.5)
    #     shoulder_center = Landmark(0, 1)
    #     result = calc_shoulder_extension(elbow, shoulder_center)
    #     assert result == 30.0, f'Expected 30.0, but got {result}'

    # def test_shoulder_extension_60():
    #     elbow = Landmark(1, 0)
    #     shoulder_center = Landmark(0, 1)
    #     result = calc_shoulder_extension(elbow, shoulder_center)
    #     assert result == 60.0, f'Expected 60.0, but got {result}'

if __name__ == '__main__':
    unittest.main()

