
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
    results = pose.process(image)
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
def display_shoulder_text_property(image, x, y, shoulder_name, angle, hand_color=(255, 255, 255)):
    font = cv2.FONT_HERSHEY_SIMPLEX
    #print("Shoulder ", shoulder_name, " = ", angle)
    cv2.putText(image, f"{shoulder_name}: {angle:.2f}",(x, y), font, 0.5, hand_color, 2, cv2.LINE_AA)

# This function is used to display the shoulder calculations on the screen for either "left" or "right" shoulder.
def display_shoulder_text_angles(image, shoulder_info, shoulder_str="left",start_x=10, start_y=10, y_offset=20, hand_color=(255, 255, 255)):
    # Display Each of the calculations on the screen for now.
    x = start_x
    display_shoulder_text_property(image, x, start_y, "flexion", shoulder_info['flexion_'+shoulder_str], hand_color)
    display_shoulder_text_property(image, x, start_y-y_offset, "abduction",
                                   shoulder_info['abduction_'+shoulder_str],hand_color)
    display_shoulder_text_property(image, x, start_y-y_offset*2,"extension",
                                   shoulder_info['extension_'+shoulder_str], hand_color)
    display_shoulder_text_property(image, x, start_y-y_offset*3, "internal_rotation",
                                   shoulder_info['internal_rotation_'+shoulder_str], hand_color)
    display_shoulder_text_property(image, x, start_y-y_offset*4, "external_rotation",
                                   shoulder_info['external_rotation_'+shoulder_str], hand_color)

# This function is used to display the shoulder landmarks that we have added and are not included in the MediaPipe Pose.
# Note: Shoulder additions are estimated, so may occur outside of the image.
def display_shoulder_positions(image, shoulder_info):
    # The data from MediaPipe is in a normalized position.
    # For now, we manually draw new landmarks, but likely can use landmarks function too.
    height, width = image.shape[:2]

    ncenter = _normalized_to_pixel_coordinates( shoulder_info['shoulder_center'].x, shoulder_info['shoulder_center'].y, width, height)
    if(ncenter):
        cv2.circle( image, (ncenter[0], ncenter[1]), 5, (0, 255, 255), -1)

    # Left - GH Joint Drawing
    ncenter = _normalized_to_pixel_coordinates(
        shoulder_info['shoulder_left_gh_joint'].x, shoulder_info['shoulder_left_gh_joint'].y, width, height)
    if(ncenter):
        cv2.circle( image, (ncenter[0], ncenter[1]), 5, (0, 255, 255), -1)

    # Right - GH Joint Drawings.
    ncenter = _normalized_to_pixel_coordinates(
        shoulder_info['shoulder_right_gh_joint'].x, shoulder_info['shoulder_right_gh_joint'].y, width, height)

    if(ncenter):
        cv2.circle( image, (ncenter[0], ncenter[1]), 5, (0, 255, 255), -1)

# These colors are taken from the MediaPipe Pose drawing style.
def get_hand_color(get_left):
    if(get_left):
        return (231, 217, 0)
    else:
        return (0, 138, 255)

def display_shoulder_text(image, results, shoulder_info, swap_colors = False):
    x = 10
    y = 10
    y_offset=-20
    height, width = image.shape[:2]
    # Display the shoulder calculations on the screen.
    cleft = get_hand_color(not swap_colors )
    cright = get_hand_color(False or swap_colors)
    display_shoulder_text_angles(image, shoulder_info, "left", start_x=x, start_y=y, y_offset=y_offset,hand_color=cleft)
    display_shoulder_text_angles(image, shoulder_info, "right", start_x=int(
        width*0.75), start_y=y, y_offset=y_offset, hand_color=cright)
