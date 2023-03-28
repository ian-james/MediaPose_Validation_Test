from mediapipe.python.solutions.pose import PoseLandmark
from mediapipe.tasks.python.components.containers import Landmark

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

def get_landmark_ids_left():
    return [
        PoseLandmark.LEFT_SHOULDER,
        PoseLandmark.LEFT_ELBOW,
        PoseLandmark.LEFT_WRIST,
        PoseLandmark.LEFT_HIP
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



