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

    # def test_calc_shoulder_flexion_invalid_input_types(self):
    #     # Test case with None passed as input
    #     elbow = None
    #     shoulder_center = Landmark(1, 1)
    #     hip = Landmark(2, 2)
    #     result = calc_shoulder_flexion(elbow, shoulder_center, hip)
    #     self.assertEqual(result, None)

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

    def test_calc_shoulder_flexion_0_degrees(self):
        
        # Elbow at Hip
        elbow = Landmark(1, 0.5)
        shoulder_center = Landmark(1, 1)
        hip = Landmark(1.0, 0.5)     
        # GENERATED:  180.0
        # GENERATED_180:  0.0
        # MY FLEXION:  0.0
        
        # Default Position
        # elbow = Landmark(1, 0.8)
        # shoulder_center = Landmark(1, 1)
        # hip = Landmark(1.0, 0.5)       
        # GENERATED:  180.0
        # GENERATED_180:  0.0
        # MY FLEXION:  0.0 
        
        # # To measure 90 degrees at a front angle we need the wrist value
        # elbow = Landmark(1, 1.0)
        # shoulder_center = Landmark(1, 1)
        # hip = Landmark(1.0, 0.5)
        # GENERATED:  90.0
        # GENERATED_180:  90.0
        # MY FLEXION:  0.0
        # # This gave 90 for both Generated and 180-generated.
        
        # # To measure 135 degrees at a front angle we need the wrist value
        # elbow = Landmark(1, 1.2)
        # shoulder_center = Landmark(1, 1)
        # hip = Landmark(1.0, 0.5)
        # GENERATED:  0.0
        # GENERATED_180:  180.0
        # MY FLEXION:  0.0

        # # To measure 135 degrees at a front angle we need the wrist value
        # elbow = Landmark(1, 1.5)
        # shoulder_center = Landmark(1, 1)
        # hip = Landmark(1.0, 0.5)
        # # GENERATED:  0.0
        # GENERATED_180:  180.0
        # MY FLEXION:  0.0
        
        # Test Real Case
        shoulder_center = Landmark(0.635440230369568,-0.39703568816185)
        elbow = Landmark(0.623615562915802,0.30449962615966797)
        hip = Landmark(1.16331684589386,0.5461454391479492)
        
        # Other shoulder
        # 0.999508440494537
        # 0.999508440494537
        # -0.550378143787384
        # (0.6330910921096802
        #  0.467012792825699
        #  0.146625891327858

        left_result = 0.146625891327858
        right_result = 0.046268031001091
        
        shoulder_center = Landmark(0.6122, 0.569)
        elbow = Landmark(0.60, 0.88)
        wrist = Landmark(0.53, 1.11)
        hip = Landmark(0.60, 1.13)
        # Flexion of 1.58
        
        gen_value = calculate_shoulder_flexion_generated(shoulder_center, elbow, hip)
        print("GENERATED: ",gen_value )
        print("GENERATED_180: ", 180-gen_value)
        self.assertEqual(calc_shoulder_flexion(elbow, shoulder_center, hip), 0)
        

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

