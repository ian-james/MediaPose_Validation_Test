
import cv2
import pandas as pd
import time
import json

from collections import OrderedDict
from datetime import datetime, timezone

from shoulder_calculations import *

import mediapipe as mp
from mediapipe.python.solutions.pose import PoseLandmark
from mediapipe.tasks.python.components.containers import Landmark
from mediapipe.python.solutions.drawing_utils import _normalized_to_pixel_coordinates

# MediaPipe Includes quick Access)
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

from landmark_helpers import *
from utils import *

# Enable writing to the image.
def enable_writing(image):
    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

# Disable writing to the image.
def disable_writing(image):
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Process the pose and return the results.
def process_pose(pose,image):
    results = pose.process(pose)
    return results

# Set the landmarks to not be visible.
def hide_landmarks(landmarks, hide_ids):
    for idx, landmark in enumerate(landmarks):
        if idx in hide_ids:
            landmark.visibility = 0

# Hide pose landmarks that are not tracked based on the results.
def hide_pose_landmarks(results):
    if(results.pose_landmarks):
        hide_landmarks(results.pose_landmarks.landmark,
                    get_non_tracked_landmarks(get_landmark_ids_list()))
        
# Draw the pose annotation on the image provided in mediapose style.
def draw_landmarks(image, results):
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

# Helpler function to display shoulder text information.
def display_shoulder_text(image, x, y, shoulder_name, angle):
    font = cv2.FONT_HERSHEY_SIMPLEX
    #print("Shoulder ", shoulder_name, " = ", angle)
    cv2.putText(image, f"{shoulder_name}: {angle:.2f}",
                (x, y), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    
# This function is used to display the shoulder calculations on the screen for either "left" or "right" shoulder.
def display_shoulder_calculations(image, shoulder_info, shoulder_str="left",start_x=10, start_y=10, y_offset=20):
    # Display Each of the calculations on the screen for now.
    x = start_x
    display_shoulder_text(image, x, start_y,
                     "flexion", shoulder_info['flexion_'+shoulder_str])
    display_shoulder_text(image, x, start_y-y_offset,
                     "abduction", shoulder_info['abduction_'+shoulder_str])
    display_shoulder_text(image, x, start_y-y_offset*2,
                     "extension", shoulder_info['extension_'+shoulder_str])
    display_shoulder_text(image, x, start_y-y_offset*3, "internal_rotation",
                     shoulder_info['internal_rotation_'+shoulder_str])
    display_shoulder_text(image, x, start_y-y_offset*4, "external_rotation",
                     shoulder_info['external_rotation_'+shoulder_str])

# This function is used to display the shoulder landmarks that we have added and are not included in the MediaPipe Pose.
def display_shoulder_additions(image, shoulder_info):
    # The data from MediaPipe is in a normalized position.
    # For now, we manually draw new landmarks, but likely can use landmarks function too.
    height, width = image.shape[:2]
    
    ncenter = _normalized_to_pixel_coordinates( shoulder_info['shoulder_center'].x, shoulder_info['shoulder_center'].y, width, height)
    cv2.circle( image, (ncenter[0], ncenter[1]), 5, (0, 255, 255), -1)

    # Left - GH Joint Drawing
    ncenter = _normalized_to_pixel_coordinates(
        shoulder_info['shoulder_left_gh_joint'].x, shoulder_info['shoulder_left_gh_joint'].y, width, height)
    #print(ncenter)
    cv2.circle(
        image, (ncenter[0], ncenter[1]), 5, (0, 255, 255), -1)

    # Right - GH Joint Drawings.
    ncenter = _normalized_to_pixel_coordinates(
        shoulder_info['shoulder_right_gh_joint'].x, shoulder_info['shoulder_right_gh_joint'].y, width, height)
    cv2.circle(
        image, (ncenter[0], ncenter[1]), 5, (0, 255, 255), -1)

def display_shoulder(image, results, shoulder_info):
    height, width = image.shape[:2]
    # Display the shoulder calculations on the screen.
    display_shoulder_calculations(image, shoulder_info, "left", 10, 10, 20)
    display_shoulder_calculations(image, shoulder_info, "right", 10, 200, 20)
    
    display_shoulder_calculations(image, shoulder_info, "left", height-10)
    display_shoulder_calculations(image, shoulder_info, "right", start_x=int(width*0.65), start_y=height-10)

    # Display the shoulder landmarks that we have added.
    display_shoulder_additions(image, shoulder_info)



