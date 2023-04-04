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
        shoulder_info = get_shoulder_calculations(landmarks)
        debug_print(shoulder_info)
    except:
        debug_print("FAILED SHOULDER INFORMATION")
        pass

    return shoulder_info


def stores_frame_data(shoulder_info, frame_data, fps_count):
    # This section manages the data collection.
    odict = OrderedDict()
    odict['fps_count'] = fps_count
    odict['timestamp'] = datetime.now(
        timezone.utc).replace(microsecond=0).isoformat()
    frame = extract_pose_frames(shoulder_info)
    odict.update(frame)
    frame_data.append(odict)

def save_to_csv(df, frame_data, output_file, interval=0):
    """
    Appends or saves new data to an Excel file using pandas DataFrame.

    :param df: pandas DataFrame to append to, or an empty DataFrame to create
    :param frame_data: list of dictionaries representing rows to append
    :param output_file: name of the output Excel file
    :param interval: interval at which to save data (0 to save after each append)
    """
    file_ext = ".csv"
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame()
    if df.empty:
        df = pd.DataFrame(frame_data)
        df.to_csv(output_file + file_ext, index=False, header=True, sep="\t")
    else:
        df = df.append(frame_data, ignore_index=True)
        #if interval == 0 or len(frame_data) % interval == 0:
        df.to_csv(output_file + file_ext, index=False, header=not df.index.size, mode='a')
    return df

def handle_keyboard():
    # Allow some keyboard actions
    # p-Pause
    # esc-exit
    key = cv2.waitKey(5)
    if key == ord('p'):
        cv2.waitKey(3000)
    elif(key == ord('s')):
        pass
        # le = LandmarkError("shoulder_flexion", 0.0,
        #                     5.0, calc_shoulder_flexion)
        # left_landmark = le.extract_landmarks(shoulder_info)
        # if(le.error_in_range()):
        #     print("Error is in range")
        # else:
        #     print("Not in range")
    elif key & 0xFF == 27:
        return False
    return True

def mediapose_main(args, cap, mode):

    check_fps = True
    # Write the DataFrame to an Excel file
    file_time = time.strftime("%Y_%m_%d-%H_%M_%S_")
    output_file = file_time + args['output'] if(args['timestamp']) else args['output']
    df = None
    needs_flip = args['mirror'] or (mode == VideoMode.CAMERA)
    with FPS() as fps, mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success, image = cap.read()
            fps.update()

            if not success:
                # If loading a video, use 'break' instead of 'continue'.
                debug_print("Ignoring empty camera frame.")                
                continue

            should_flip = needs_flip
            
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            if(check_fps == False):
                debug_print("FPS: {}".format(fps.get_fps()))
                #check_fps = True
            else:

                frame_data = []
                disable_writing(image)

                results = process_pose(pose, image)

                # Draw the pose annotation on the image.
                enable_writing(image)
                hide_pose_landmarks(results)

                # Draw all landmarks ( TODO: This might become more shoulder based.)
                draw_landmarks(image, results)           

                shoulder_info = get_shoulder_info(results)

                if(shoulder_info):
                    # This section manages the data collection.
                    stores_frame_data( shoulder_info, frame_data, fps.num_frames)

                    # This section manages the text display in 2D.
                    # Note: MediaPose evaluates the model in a different virtual space and the images needs to be flipped horizontal.
                    #       to enable use to put text on the screen.
                    #       They refer to this a returning to selfie-mode.                    
                    display_shoulder_positions(image, shoulder_info)

                    # Display 2D text on the screen.
                    # Display Each of the calculations on the screen for now.
                    # Flip the image horizontally for a selfie-view display.
                    if(should_flip):
                        image = cv2.flip(image, 1)
                        should_flip = False
                    
                    display_shoulder_text(image, results, shoulder_info,needs_flip)
                    df = save_to_csv(df, frame_data, output_file, interval=0)
                else:
                    print("Not shoulder info")

                if(handle_keyboard() == False):
                    save_to_csv(df, frame_data, output_file, interval=0)
                    break

            # Flip the image horizontally for a selfie-view display.
            # Flipping the image for 2D/3D differences in display positions.
            if( should_flip):
                image = cv2.flip(image, 1)
            cv2.imshow('MediaPipe Pose', image)    
