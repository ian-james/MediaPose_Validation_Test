from collections import OrderedDict
from datetime import datetime, timezone

import logging
from fps_timer import FPS
from camera_utils import *
from file_utils import *

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

# This section manages the data collection.
def stores_frame_data(shoulder_info, fps_count):
    # This section manages the data collection.
    odict = setup_frame_data(fps_count)
    frame = extract_pose_frames(shoulder_info)
    odict.update(frame)
    return odict

def get_shoulder_info(results):
    # Get the shoulder info for the current frame
    shoulder_info = {}
    try:
        # Setup the landmarks to an easy local structure to query.
        landmarks = results.pose_landmarks
        # Calculate new positions and angles.
        shoulder_landmarks = get_landmarks(landmarks)
        logging.debug("Print Shoulder Information")
        
        shoulder_info = get_shoulder_calculations(landmarks)
        logging.debug(shoulder_info)
    except:
        logging.debug("FAILED SHOULDER INFORMATION")
        pass

    return shoulder_info

def handle_keyboard(image):
    # Allow some keyboard actions
    # p-Pause
    # esc-exit
    key = cv2.waitKey(1)
    if key == ord('p'):
        cv2.waitKey(3000)
    elif(key == ord('s')):        
        snapshot_file =  time.strftime("%Y_%m_%d-%H_%M_%S_") + "_snapshot.png"        
        write_snapshot_image(get_file_path(snapshot_file), image)      
        pass    
    elif key & 0xFF == 27:
        return False
    return True

def draw_mediapipe(pose, image, total_frames, media_noface):

    disable_writing(image)
    results = process_pose(pose, image)

    # Draw the pose annotation on the image.
    enable_writing(image)

    if(media_noface):
        hide_pose_landmarks(results)

    # Draw all landmarks ( TODO: This might become more shoulder based.)
    draw_landmarks(image, results)
    shoulder_info = get_shoulder_info(results)

    frame = setup_frame_data(total_frames)
    if(shoulder_info):
        # This section manages the data collection.
        frame = stores_frame_data(shoulder_info, total_frames)
  
    return frame


def draw_mediapipe_extended(pose, image, total_frames, display_calculations = False):

    frame = setup_frame_data(total_frames)
    disable_writing(image)

    results = process_pose(pose, image)

    # Draw the pose annotation on the image.
    enable_writing(image)
    hide_pose_landmarks(results)

    # Draw all landmarks
    draw_landmarks(image, results)
    shoulder_info = get_shoulder_info(results)

    if(shoulder_info):
        # This section manages the data collection.
        frame = stores_frame_data(shoulder_info, total_frames)

        # This section manages the text display in 2D.
        # Note: MediaPose evaluates the model in a different virtual space and the images needs to be flipped horizontal.
        #       to enable use to put text on the screen.
        #       They refer to this a returning to selfie-mode.
        display_shoulder_positions(image, shoulder_info)

        if(display_calculations):
            # Display 2D text on the screen.
            display_shoulder_text(image, shoulder_info)

    return frame

def mediapose_main(args, cap, mode, frame_size, fps, check_fps = False):

    df = None
    total_frames = 0    
    # Write the DataFrame to an Excel file
    file_time = time.strftime("%Y_%m_%d-%H_%M_%S_")
    output_filename = file_time + args['output'] if(args['timestamp']) else args['output']
    path_to_file = get_file_path(output_filename, "../records/")
    output_full_file = add_extension(path_to_file)
    
    needs_flip = args['mirror'] or (mode == VideoMode.CAMERA)

    media_only = args['media']
    media_noface = args['media_noface']
    # Define the codec and create a VideoWriter object
    # Allow Recording only if the user previously specified a file name.
    out_record = open_recording_file(args['record'], frame_size, fps)
    out_record_media = open_recording_file(
        args['record_media'], frame_size, fps)

    # The first frame indicates if the camera or video is working.
    with FPS() as fps, mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.8) as pose:
        while cap.isOpened():
                       
            success, image = cap.read()
            fps.update()           

            if not success:   
                if(mode == VideoMode.VIDEO):
                    logging.info("Finished the video.")
                    break
                else:
                    logging.info("Ignoring empty camera frame.")
                    continue                    
            
            if(out_record):
                out_record.write(image)
          
            should_flip = needs_flip
            total_frames += 1            
            keep_working = True
            frame_data = []

            # Check for the multiple types of display.
            # Display the camera and the FPS.
            # Display mediapipe without additional calcualtions.
            # Display mediapipe with additional calculations.
            if(check_fps == True):
                frame = setup_frame_data(total_frames)
                tfps = fps.get_fps()
                frame['fps'] = tfps
                logging.debug("FPS: {}".format(tfps))
                image, should_flip = flip_image(image, should_flip)
                draw_fps(image, tfps)

            elif(media_only):
                frame = draw_mediapipe(
                    pose, image, total_frames, media_noface)
            else:
                # Do our version of the pose estimation.
                frame = draw_mediapipe_extended(
                    pose, image, total_frames, args['display'])

            frame_data.append(frame)           

            cv2.imshow('MediaPipe Pose', image)
            if(out_record_media):
                out_record_media.write(image)
                
            df = save_to_csv(df, frame_data, output_full_file)
            save_key_columns(df, add_extension(path_to_file + "_keycols"))
            if(not handle_keyboard(image)):                                
                break

    if(out_record_media):
        out_record_media.release()

    if(out_record):
        out_record.release()
        
    logging.info("Writing excel file from the CSV file.")    
    # Make a copy of Excel    
    copy_csv_to_excel(output_full_file, add_extension(path_to_file, ".xlsx"))
