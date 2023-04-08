from enum import Enum
from collections import OrderedDict
from datetime import datetime, timezone

import logging
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


def copy_csv_to_excel(csv_file, excel_file):
    # Copy the CSV file to an Excel file    
    try:
        df = pd.read_csv(csv_file, sep="\t")
        df.to_excel(excel_file, index=False, header=True)
    except Exception as e:
        logging.error("Error copying CSV to Excel: " + str(e))



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

# This section manages the data collection.


def setup_frame_data(fps_count):
    # This section manages the data collection.
    odict = OrderedDict()
    odict['fps_count'] = fps_count
    odict['timestamp'] = datetime.now(
        timezone.utc).isoformat()
    return odict

# This section manages the data collection.
def stores_frame_data(shoulder_info, fps_count):
    # This section manages the data collection.
    odict = setup_frame_data(fps_count)
    frame = extract_pose_frames(shoulder_info)
    odict.update(frame)
    return odict

def save_to_csv(df, frame_data, output_file):
    """
    Appends or saves new data to an Excel file using pandas DataFrame.

    :param df: pandas DataFrame to append to, or an empty DataFrame to create
    :param frame_data: list of dictionaries representing rows to append
    :param output_file: name of the output Excel file
    :param interval: interval at which to save data (0 to save after each append)
    """
    # TODO: Fix this so that it's appending and not overwriting.

    sep = "\t"
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame()
    if df.empty:
        df = pd.DataFrame(frame_data)
        df.to_csv(output_file, index=False, header=True,sep=sep)
    else:
        df = df.append(frame_data, ignore_index=True)
        #if interval == 0 or len(df) % interval == 0:
        df.to_csv(output_file, index=False, header=True, sep=sep)
    return df

def write_snapshot_image(filename, image):
    # Write the image to a file
    status = cv2.imwrite(filename, image)
    return status

def handle_keyboard(image):
    # Allow some keyboard actions
    # p-Pause
    # esc-exit
    key = cv2.waitKey(1)
    if key == ord('p'):
        cv2.waitKey(3000)
    elif(key == ord('s')):
        file_time = time.strftime("%Y_%m_%d-%H_%M_%S_")
        write_snapshot_image(file_time, image)      
        pass
    elif(key==ord('d')):
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


def draw_fps(image, fps):
    # Draw the FPS on the image
    cv2.putText(image, "FPS: {:.2f}".format(fps), (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


def draw_mediapipe(pose, image, total_frames, media_noface):

    disable_writing(image)
    results = process_pose(pose, image)

    # Draw the pose annotation on the image.
    enable_writing(image)

    if(media_noface):
        hide_pose_landmarks(results)

    # Draw all landmarks ( TODO: This might become more shoulder based.)
    draw_landmarks(image, results)

    frame = setup_frame_data(total_frames)
    return frame


def draw_mediapipe_extended(pose, image, total_frames, should_flip):

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

        # Display 2D text on the screen.
        display_shoulder_text(image, shoulder_info)

    return frame


def open_recording_file(record_file, frame_size, fps, location="../records/"):
    # Define the codec and create a VideoWriter object
    # Allow Recording only if the user previously specified a file name.
    out_record_media = None
    if(record_file != ""):
        absolute_path = os.path.abspath(location)
        create_directory(absolute_path)
        full_path = os.path.join(absolute_path, record_file)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out_record_media = cv2.VideoWriter(full_path, fourcc, fps, frame_size)
    return out_record_media

def mediapose_main(args, cap, mode, frame_size, fps):

    df = None
    total_frames = 0
    check_fps = False
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

    with FPS() as fps, mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
                       
            success, image = cap.read()
            fps.update()

            if(out_record):
                out_record.write(image)

            if not success:
                # If loading a video, use 'break' instead of 'continue'.
                logging.debug("Ignoring empty camera frame.")
                continue

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
                    pose, image, total_frames, should_flip)

            frame_data.append(frame)           

            cv2.imshow('MediaPipe Pose', image)
            if(out_record_media):
                out_record_media.write(image)
                
            df = save_to_csv(df, frame_data, output_full_file)
            if(not handle_keyboard()):                                
                break

    if(out_record_media):
        out_record_media.release()

    if(out_record):
        out_record.release()
        
    logging.info("Writing excel file from the CSV file.")    
    # Make a copy of Excel    
    copy_csv_to_excel(output_full_file, add_extension(path_to_file, ".xlsx"))
