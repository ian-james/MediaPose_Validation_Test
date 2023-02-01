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

# Function: calc_shoulder_flexion
# Intention: Calculates the shoulder flexion based on the elbow and shoulder position.
# Limitations: Degree of visibility
# Params: Elbow and Shoulder MediaPipe Landmarks or NormalizedLandmarks
# Error Result: An empty object
# Success Result: An estimate of the shoulder flexsion.
def calc_shoulder_flexion(elbow, shoulder_center):
    shoulder_flexion = {}
    try:
        shoulder_flexion = elbow.y - shoulder_center.y
        # Calculate shoulder flexion
        shoulder_flexion = math.degrees(math.atan2(shoulder_center.x - elbow.x, shoulder_center.y - elbow.y))
        #print("Calculated SF", shoulder_flexion)
    except Exception as e:
        print("An error occurred while trying to calculate shoulder flexion:", e)
    return shoulder_flexion

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
            'flexion_left' : calc_shoulder_flexion(elbow_left,shoulder_left),
            'abduction_left' : calc_shoulder_abduction(elbow_left, shoulder_left),
            'extension_left' : calc_shoulder_extension(elbow_left, shoulder_left),
            'internal_rotation_left' : calc_shoulder_internal_rotation(wrist_left,shoulder_left),
            'external_rotation_left' : calc_shoulder_external_rotation(wrist_left, shoulder_left),
            'shoulder_right_gh_joint': calc_shoulder_gh_joint(shoulder_right,hip_right),
            'flexion_right' : calc_shoulder_flexion(elbow_right,shoulder_right),
            'abduction_right' : calc_shoulder_abduction(elbow_right, shoulder_right),
            'extension_right' : calc_shoulder_extension(elbow_right, shoulder_right),
            'internal_rotation_right' : calc_shoulder_internal_rotation(wrist_right,shoulder_right),
            'external_rotation_right' : calc_shoulder_external_rotation(wrist_right, shoulder_right)
        }


# Function to identify landmarks we are not tracking.
# Return List of PoseLandmark Enum
def get_non_tracked_landmarks(landmarks):
    TOTAL_LANDMARKS = 33
    return [ x for x in range(0,TOTAL_LANDMARKS) if x not in landmarks ]

# Default: Selects Left than Right positions of (shoulder, elbow, wrist,  hip)
def get_landmark_ids_list():
    return [
    PoseLandmark.LEFT_SHOULDER,
    PoseLandmark.RIGHT_SHOULDER,
    PoseLandmark.LEFT_ELBOW,
    PoseLandmark.RIGHT_ELBOW,
    PoseLandmark.LEFT_WRIST,
    PoseLandmark.RIGHT_WRIST,
    PoseLandmark.LEFT_HIP,
    PoseLandmark.RIGHT_HIP
    ]

# Retrieve a single landmark from the MediaPipe Landmarks
def get_landmark(landmarks, landmark_id):
    for idx, landmark in enumerate(landmarks.landmark):
        if(idx ==  landmark_id):
            return landmark
    return None

# Select Multiple landmarks from Mediapose
# Default: Selects Left than Right positions of (shoulder, elbow, wrist,  hip)
# TODO: Magic Numbers changed to PoseLandmark(Enum)
def get_landmarks(landmarks, landmark_list=get_landmark_ids_list()):
    return [landmark for idx, landmark in enumerate(landmarks.landmark) if idx in landmark_list]

# Helpler function to display shoulder text information.
def display_shoulder(image,x,y,shoulder_name, angle):
    font = cv2.FONT_HERSHEY_SIMPLEX
    print("Shoulder ", shoulder_name, " = ", angle)
    cv2.putText(image, f"{shoulder_name}: {angle:.2f}", (x, y), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

def hide_landmarks(landmarks, hide_ids):
    for idx, landmark in enumerate(landmarks):
        if idx in hide_ids:
            landmark.visibility = 0

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
