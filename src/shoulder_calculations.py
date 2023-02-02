import math
from mediapipe.python.solutions.pose import PoseLandmark
from mediapipe.tasks.python.components.containers import Landmark

from landmark_helpers import *

# Notes:
# Angles Information
# Reference https://content.iospress.com/media/bmr/2018/31-4/bmr-31-4-bmr140203/bmr-31-bmr140203-g002.jpg?width=755
# Shoulder Flexion along x-axis 0 at rest, 180 straight,
# Shoulder Extension 60 backward, 0 at rest
# Elbow Flexion (along x-axis) 90 at rest, 0 bend elbow, 60 full curl

# Internal Rotation - 0 arm straight out and wrist up, 90 by side wrist up,
# External Rotation - 0 arm straight out 0 and 90 straight up.

# Horizontal Abduction and Adduction (y-axis rotation, arm straight along x-axis thumb- rest 0, straight arm in-front thumb up 90)
# Abduction and Adjuction (z-axis rotation arm down by side is rest 0, straight out to side is 90, above head palm out 180)


# Function: calc_shoulder_gh_joint
# Intention: Estimate the position of the position of the GH-Joint
# Limitations: This calculation is an estimate based on shoulder and hip locations
#              This estimation is based on 25% of the distance between hip and shoulder.
# Params: Shoulder and Hip Media Landmarks or NormalizedLandmarks
# Error Result: An empty object
# Success Result: A GH-Joint Estimate Position (Landmark)
def calc_shoulder_gh_joint(shoulder, hip):
    shoulder_gh = {}
    try:
        x = (shoulder.x + hip.x) / 2
        y = (shoulder.y + hip.y) / 2
        z  = (shoulder.z + hip.z) / 2
        shoulder_gh = Landmark( (shoulder.x + x) / 2,
                                    (shoulder.y + y)  / 2,
                                    (shoulder.z + z)/2
        )
        #print("Shoulder_GH",shoulder_gh)
    except:
        print("Could not calculate the shoulder GH Joint.")
    return shoulder_gh

# Function: calc_shoulder_center
# Intention: Estimate the center position between the two shoulders.
# Limitations: None
# Params: Left and Right Shoulder MediaPipe Landmarks or NormalizedLandmarks
# Error Result: An empty object
# Success Result: The center of the two shoudlers Estimate Position (Landmark)
def calc_shoulder_center(shoulder_left, shoulder_right):
    shoulder_center = {}
    try:
        shoulder_center = Landmark( (shoulder_left.x + shoulder_right.x) / 2,
                                    (shoulder_left.y + shoulder_right.y) / 2,
                                    (shoulder_left.z + shoulder_right.z) / 2
        )
        #print("Shoulder_Center",shoulder_center)
    except:
        print("Could not calculate the shoulder center.")
    return shoulder_center

def calc_shoulder_flexion(elbow, shoulder_center, hip):
    """
    Calculates the shoulder flexion angle given the elbow, shoulder center, and hip landmarks.

    Args:
        elbow (Landmark): The landmark for the elbow.
        shoulder_center (Landmark): The landmark for the shoulder center.
        hip (Landmark): The landmark for the hip.

    Returns:
        float: The shoulder flexion angle in degrees, or None if an error occurred.
    """

    try:
        # Calculate the vectors from the hip to the elbow and from the hip to the shoulder center
        elbow_vector = (elbow.x - hip.x, elbow.y - hip.y)
        shoulder_center_vector = (shoulder_center.x - hip.x, shoulder_center.y - hip.y)

        # Calculate the dot product of the two vectors
        dot_product = elbow_vector[0] * shoulder_center_vector[0] + elbow_vector[1] * shoulder_center_vector[1]

        # Calculate the lengths of the two vectors
        elbow_vector_length = math.sqrt(elbow_vector[0] ** 2 + elbow_vector[1] ** 2)
        shoulder_center_vector_length = math.sqrt(shoulder_center_vector[0] ** 2 + shoulder_center_vector[1] ** 2)

        # Calculate the cosine of the angle between the two vectors
        cosine_angle = dot_product / (elbow_vector_length * shoulder_center_vector_length)

        # Calculate the shoulder flexion angle
        shoulder_flexion = math.degrees(math.acos(cosine_angle))
        return shoulder_flexion
    except Exception as e:
        print("An error occurred while trying to calculate shoulder flexion:", e)
    return {}

# Function: calc_shoulder_abduction
# Intention: Calculates the shoulder abduction based on the elbow and shoulder position.
# Limitations: Degree of visibility
# Params: Elbow and Shoulder MediaPipe Landmarks or NormalizedLandmarks
# Error Result: An empty object
# Success Result: An estimate of the shoulder abduction
def calc_shoulder_abduction(elbow, shoulder_center):
    shoulder_abduction = {}
    try:
        # Suggest Wrist - Elbow
        shoulder_abduction =  math.degrees(math.atan2(elbow.y - shoulder_center.y, elbow.x - shoulder_center.x))
        #print("Calculated SA", shoulder_abduction)
    except Exception as e:
        print("An error occurred while trying to calculate shoulder abudction:", e)
    return shoulder_abduction

# Function: calc_shoulder_extension
# Intention: Calculates the shoulder extension based on the elbow and shoulder position.
# Limitations: Degree of visibility
# Params: Elbow and Shoulder MediaPipe Landmarks or NormalizedLandmarks
# Error Result: An empty object
# Success Result: An estimate of the shoulder extension
def calc_shoulder_extension(elbow, shoulder_center):
    shoulder_extension = {}
    try:
        # Calculate shoulder extension
        shoulder_extension = 180 - math.degrees(math.atan2(shoulder_center.x - elbow.x, shoulder_center.y - elbow.y))
        #print("CALCULATED SE", shoulder_extension)
    except Exception as e:
        print("An error occurred while trying to calculate shoulder flexion:", e)
    return shoulder_extension

# Function: calc_shoulder_internal_rotation
# Intention: Calculates the internal rotation based on the wrist and shoulder
# Limitations: Degree of visibility
# Params: wrist and Shoulder MediaPipe Landmarks or NormalizedLandmarks
# Error Result: An empty object
# Success Result: An estimate of shoulder internal rotation
def calc_shoulder_internal_rotation(wrist,shoulder_center):
    shoulder_internal_rotation = {}
    try:
        # Calculate shoulder internal rotation
        shoulder_internal_rotation =  math.degrees(math.atan2(wrist.y - shoulder_center.y, wrist.x - shoulder_center.x))
        #print("CALCULATED IR", shoulder_internal_rotation)
    except Exception as e:
        print("An error occurred while trying to calculate shoulder internal rotation:", e)
    return shoulder_internal_rotation

# Function: calc_shoulder_external_rotation
# Intention: Calculates the external rotation based on the wrist and shoulder
# Limitations: Degree of visibility
# Params: wrist and Shoulder MediaPipe Landmarks or NormalizedLandmarks
# Error Result: An empty object
# Success Result: An estimate of shoulder external rotation
def calc_shoulder_external_rotation(wrist,shoulder_center):
    shoulder_external_rotation = {}
    try:
        shoulder_external_rotation = 180 - math.degrees(math.atan2(wrist.y - shoulder_center.y, wrist.x - shoulder_center.x))
        #print("CALCULATED ER", shoulder_external_rotation)
    except Exception as e:
        print("An error occurred while trying to calculate shoulder external rotation:", e)
    return shoulder_external_rotation


# Function: get_shoulder_info
# Intention: Identifies MediaPose landmarks and calculates the positions and rotation values.
# Limitations: Level of estimation needs to be determined.
# Params: All MediaPipe Landmarks or NormalizedLandmarks
# Error Result: Those positions and information that could be estimate will have data.
#               Remaining elements will have empty objects.
# Success Result: A dictionary of shoulder landmarks and calculations.
def get_shoulder_info(landmarks):
    shoulder_left = {}
    shoulder_right = {}
    shoulder_center = {}

    #print("GET SHOULDER INFORMATION")
    shoulder_left = get_landmark(landmarks,PoseLandmark.LEFT_SHOULDER)
    shoulder_right = get_landmark(landmarks,PoseLandmark.RIGHT_SHOULDER)
    #print("Shoulder received")

    elbow_left = get_landmark(landmarks,PoseLandmark.LEFT_ELBOW)
    elbow_right = get_landmark(landmarks,PoseLandmark.RIGHT_ELBOW)
    #print("Elbow received")

    wrist_left = get_landmark(landmarks,PoseLandmark.LEFT_WRIST)
    wrist_right = get_landmark(landmarks,PoseLandmark.RIGHT_WRIST)
    #print("Wrist Received")

    hip_left = get_landmark(landmarks,PoseLandmark.LEFT_HIP)
    hip_right = get_landmark(landmarks,PoseLandmark.RIGHT_HIP)

    return {
            'shoulder_left':shoulder_left,
            'shoulder_right':shoulder_right,
            'shoulder_center': calc_shoulder_center(shoulder_left,shoulder_right),
            'shoulder_left_gh_joint': calc_shoulder_gh_joint(shoulder_left,hip_left),
            'flexion_left' : calc_shoulder_flexion(elbow_left,shoulder_left,hip_left),
            'abduction_left' : calc_shoulder_abduction(elbow_left, shoulder_left),
            'extension_left' : calc_shoulder_extension(elbow_left, shoulder_left),
            'internal_rotation_left' : calc_shoulder_internal_rotation(wrist_left,shoulder_left),
            'external_rotation_left' : calc_shoulder_external_rotation(wrist_left, shoulder_left),
            'shoulder_right_gh_joint': calc_shoulder_gh_joint(shoulder_right,hip_right),
            'flexion_right' : calc_shoulder_flexion(elbow_right,shoulder_right,hip_right),
            'abduction_right' : calc_shoulder_abduction(elbow_right, shoulder_right),
            'extension_right' : calc_shoulder_extension(elbow_right, shoulder_right),
            'internal_rotation_right' : calc_shoulder_internal_rotation(wrist_right,shoulder_right),
            'external_rotation_right' : calc_shoulder_external_rotation(wrist_right, shoulder_right)
        }
