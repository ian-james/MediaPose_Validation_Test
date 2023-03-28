from enum import Enum
from collections import OrderedDict
from datetime import datetime, timezone

from fps_timer import FPS

# MediaPipe Includes
import mediapipe as mp
from mediapipe.python.solutions.pose import PoseLandmark
from mediapipe.tasks.python.components.containers import Landmark
from mediapipe.python.solutions.drawing_utils import _normalized_to_pixel_coordinates

from shoulder_calculations import *
from shoulder_display import *
from landmark_helpers import *

# MediaPipe Includes quick Access)
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

def get_shoulder_info(results):
    # Get the shoulder info for the current frame  
    shoulder_info = {}
    try:
        # Setup the landmarks to an easy local structure to query.
        landmarks = results.pose_landmarks
        # Calculate new positions and angles.
        shoulder_landmarks = get_landmarks(landmarks)

        debug_print("Print Shoulder Information")
        shoulder_info = get_shoulder_info(landmarks)
        debug_print(shoulder_info)
    except:
        debug_print("FAILED SHOULDER INFORMATION")
        pass
    
    return shoulder_info


def stores_frame_data(shoulder_info, frame_data, fps_count):
    # This section manages the data collection.
    odict = OrderedDict()
    odict['fps_count'] = fps_count
    odict['timestamp'] = datetime.now(timezone.utc)
    frame = extract_pose_frames(shoulder_info)
    odict.update(frame)
    frame_data.append(odict)

def save_to_excel(frame_data, args, file_time):
    # Save the frame data to an Excel file every interval
    # Applies the name changes, and sets timestamp column for export.
    if len(frame_data) % args['interval'] == 0:
        df = pd.DataFrame(frame_data)

        # Remove Timezone for Excel writer
        if('timestamp' in df):
            df['timestamp'] = df['timestamp'].dt.tz_localize(None)
            df['timestamp']

        # Write the DataFrame to an Excel file
        filename = args['output']
        if(args['timestamp']):
            filename = file_time + filename

        df.to_excel(filename, index=False)


def handle_keyboard(shoulder_info):
    # Allow some keyboard actions
    # p-Pause
    # esc-exit
    key = cv2.waitKey(5)
    if key == ord('p'):
        cv2.waitKey(3000)
    elif(key == ord('s')):
        le = LandmarkError("shoulder_flexion", 0.0,
                            5.0, calc_shoulder_flexion)
        left_landmark = le.extract_landmarks(shoulder_info)
        if(le.error_in_range()):
            print("Error is in range")
        else:
            print("Not in range")
    elif key & 0xFF == 27:
        return False
    return True

def draw_image(image,mode):
    # Flip the image horizontally for a selfie-view display.
    # Note: If we already flipped, we don't need to again.
    # Majority of the time the image will already have been flipped.
    # So this protect against errors in the calculations section.
    if(mode == VideoMode.CAMERA):
        image = cv2.flip(image, 1)    
    cv2.imshow('MediaPipe Pose',image)

def mediapose_main(args, cap, mode):
    
    frame_data = pd.DataFrame()
    file_time = time.strftime("%Y_%m_%d-%H_%M_%S_")
    check_fps = False
    
    with FPS() as fps, mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success, image = cap.read()
            fps.update()
            
            if not success:
                debug_print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            
            if(check_fps == False):
                debug_print("FPS: {}".format(fps.get_fps()))
                #check_fps = True
            else:
                                
                disable_writing(image)            
                
                results = process_pose(pose,image)
                            
                enable_writing(image)
                # Draw the pose annotation on the image.
                
                hide_pose_landmarks(results)

                # Draw all landmarks ( TODO: This might become more shoulder based.)
                draw_landmarks(image, results)
                            
                if(args['mirror'] or (mode == VideoMode.CAMERA)):
                    image = cv2.flip(image, 1)
                    
                shoulder_info = get_shoulder_info(results)
                    
                # This section manages the data collection.
                stores_frame_data(shoulder_info, frame_data)
                
                # This section manages the text display in 2D.
                # Note: MediaPose evaluates the model in a different virtual space and the images needs to be flipped horizontal.
                #       to enable use to put text on the screen.
                #       They refer to this a returning to selfie-mode.   
            
                # Display Each of the calculations on the screen for now.
                display_shoulder(image, results)
                    
                save_to_excel(frame_data, args, file_time)
            
                if( handle_keyboard() == False):
                    break 
                        
            draw_image(image,mode)                                
                      
           
        
       
