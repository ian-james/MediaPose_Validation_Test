# Main Reference Starts at https://google.github.io/mediapipe/solutions/pose.html
# Author: Jamey Fraser
# Date: Jan 19th, 2023

# OpenCV Libary
import cv2
import math

# MediaPipe Includes
import mediapipe as mp
from mediapipe.python.solutions.pose import PoseLandmark
from mediapipe.tasks.python.components.containers import Landmark
from mediapipe.python.solutions.drawing_utils import _normalized_to_pixel_coordinates

from shoulder_calculations import *
from landmark_helpers import *

# MediaPipe Includes quick Access)
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# Demo Comments
# Calibrate in neutral position, where is the axis for their initial position.
# Consideration for the starting points between normal Range-of-Motion and patients.
# Further investigate depth as Z-Axis is calculated via ML. How accurate is it?
# Validations  - Gold standard against ours ( DartFish or OptiTrack etc)
# Standard starting position for exercises.
# Goals rely on evaluating tele-health types solutions based on quick assessment (guess-estimate)
# However, this has potential as low entry points for cost, setup, and now requires validation for accuracy.
# End Comments

# MediaPipe - Key Positions in the Landmarks Map
# 11- Left Shoudler
# 12 - Right Shoulder
# 13 - Left Elbow
# 14 - Right Elbow65
# 15 - Left Wrist
# 16 - Right Wrist
# ...
# 23 - Left Hip
# 24 - Right Hip

# Helpler function to display shoulder text information.
def display_shoulder(image,x,y,shoulder_name, angle):
    font = cv2.FONT_HERSHEY_SIMPLEX
    print("Shoulder ", shoulder_name, " = ", angle)
    cv2.putText(image, f"{shoulder_name}: {angle:.2f}", (x, y), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

## Start of the main program or loop
done = True
# For webcam input:
cap = cv2.VideoCapture(0)
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if(results.pose_landmarks):
        hide_landmarks(results.pose_landmarks.landmark,get_non_tracked_landmarks(get_landmark_ids_list()))

    # Draw all landmarks ( TODO: This might become more shoulder based.)
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

    ## Start of post-analysis mark-up
    # This section adds our new landmarks and text.
    f_image = None
    is_flipped = False
    try:
        # Setup the landmarks to an easy local structure to query.
        landmarks = results.pose_landmarks
    
        # Calculate new positions and angles.
        shoulder_landmarks = get_landmarks(landmarks)
        shoulder_info = get_shoulder_info(landmarks)
        #print("Print Shoulder Information")
        #print(shoulder_info)
    
        # Get the Image Shape to accuractly draw.
        height, width = image.shape[:2]
        #print("Display SHoulder Information")
        #print(height)
        #print(width)

        # The data from MediaPipe is in a normalized position.
        # For now, we manually draw new landmarks, but likely can use landmarks function too.
        ncenter = _normalized_to_pixel_coordinates(shoulder_info['shoulder_center'].x,shoulder_info['shoulder_center'].y,width,height)
        cv2.circle(image, (ncenter[0],ncenter[1]), 5, (0, 255, 255), -1)

        # Left - GH Joint Drawing
        ncenter = _normalized_to_pixel_coordinates(shoulder_info['shoulder_left_gh_joint'].x,shoulder_info['shoulder_left_gh_joint'].y,width,height)
        #print(ncenter)
        cv2.circle(image, (ncenter[0],ncenter[1]), 5, (0, 255, 255), -1)

        # Right - GH Joint Drawings.
        ncenter = _normalized_to_pixel_coordinates(shoulder_info['shoulder_right_gh_joint'].x,shoulder_info['shoulder_right_gh_joint'].y,width,height)
        cv2.circle(image, (ncenter[0],ncenter[1]), 5, (0, 255, 255), -1)

        # This section manages the text display in 2D.
        # Note: MediaPose evaluates the model in a different virtual space and the images needs to be flipped horizontal.
        #       to enable use to put text on the screen.
        #       They refer to this a returning to selfie-mode.

        # Flip the image for writing text in readable mode.
        f_image = cv2.flip(image, 1)
        is_flipped=True

        # Display Each of the calculations on the screen for now.
        x = 10
        display_shoulder(f_image,x,height-10,"flexion", shoulder_info['flexion_left'])
        display_shoulder(f_image,x,height-30,"abduction", shoulder_info['abduction_left'])
        display_shoulder(f_image,x,height-50,"extension", shoulder_info['extension_left'])
        display_shoulder(f_image,x,height-70,"internal_rotation", shoulder_info['internal_rotation_left'])
        display_shoulder(f_image,x,height-90,"external_rotation", shoulder_info['external_rotation_left'])

        x = int(width/1.5)
        display_shoulder(f_image,x,height-10,"flexion", shoulder_info['flexion_right'])
        display_shoulder(f_image,x,height-30,"abduction", shoulder_info['abduction_right'])
        display_shoulder(f_image,x,height-50,"extension", shoulder_info['extension_right'])
        display_shoulder(f_image,x,height-70,"internal_rotation", shoulder_info['internal_rotation_right'])
        display_shoulder(f_image,x,height-90,"external_rotation", shoulder_info['external_rotation_right'])
        print("***\n\n")
    except:
        print("FAILED SHOULDER INFORMATION")
        pass

    # Flip the image horizontally for a selfie-view display.
    # Note: If we already flipped, we don't need to again.
    # Majority of the time the image will already have been flipped.
    # So this protect against errors in the calculations section.
    if(not is_flipped):
        cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    else:
        cv2.imshow('MediaPipe Pose', f_image)

    # Allow some keyboard actions
    # p-Pause
    # esc-exit
    key = cv2.waitKey(5)
    if key == ord('p'):
        cv2.waitKey(3000)
    elif key & 0xFF == 27:
      break


# Clean up the rsources for the camera and windows.
cap.release()
cv2.destroyAllWindows()
