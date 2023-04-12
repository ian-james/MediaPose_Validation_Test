from enum import Enum
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
from mediapipe_main import draw_mediapipe
from mediapipe_main import draw_mediapipe_extended
from mediapipe_main import handle_keyboard

# TODO:
# Options for camera a single video with both mediapipe and extended calculations.

# check FPS will allow you to check the two videos with the FPS information.
# To compare the two videos
    #1 Play just the two videos.
        ## fps_check = True
        ## Alternatively

    # IF COMPARE MODE IS ON
    # normal, media
    # normal, extended (same video, media_only = False)
    # media, extended (same video, media_only = True)
    # media, media, (two different videos, media_only = True)
    # extended, extended ( two different videos, media_only = False
    


def setup_normal_frame(total_frames,fps,device=1):
    frame = setup_frame_data(total_frames)
    frame['fps'] = fps.get_fps()
    frame['video'] = device
    return frame

def comparative_main(args, main_cap, second_cap, check_fps=False):

    df = None
    total_frames = 0    
    # Write the DataFrame to an Excel file
    file_time = time.strftime("%Y_%m_%d-%H_%M_%S_")
    output_filename = file_time + args['output'] if(args['timestamp']) else args['output']
    path_to_file = get_file_path(output_filename, "../records/")
    output_full_file = add_extension(path_to_file)

    media_only = args['media']
    media_noface = args['media_noface']
    # Define the codec and create a VideoWriter object
    # Allow Recording only if the user previously specified a file name.
    out_record = open_recording_file(args['record'], (main_cap.width,main_cap.height), main_cap.fps_rate)
    out_record_media = open_recording_file(
        args['record_media'], (main_cap.width, main_cap.height), main_cap.fps_rate)

    # The first frame indicates if the camera or video is working.
    mdc= 0.7
    mtc = 0.7
    with FPS() as fps, mp_pose.Pose(min_detection_confidence=mdc, min_tracking_confidence=mtc) as pose1, \
        mp_pose.Pose(min_detection_confidence=mdc, min_tracking_confidence=mtc) as pose2:
        while main_cap.cap.isOpened() and second_cap.cap.isOpened():

            success1, image1 = main_cap.cap.read()
            success2, image2 = second_cap.cap.read()
            fps.update()

            if(not success1 or not success2):
                logging.info("Finished the video.")
                break

            should_flip = False
            total_frames += 1
            keep_working = True
            frame_data = []
            frame1 = None
            frame2 = None

            # Check for the multiple types of display.
            # Display the camera and the FPS.
            # Display mediapipe without additional calcualtions.
            # Display mediapipe with additional calculations.
            if(check_fps == True):
                frame1 = setup_normal_frame(total_frames,fps,1)
                logging.debug("FPS: {}".format(fps.get_fps()))
                image = cv2.hconcat([image1, image2])
                image, should_flip = flip_image(image, should_flip)
                draw_fps(image, fps.get_fps())
            elif(media_only):                
                if( args['compare_file'] == args['filename'] ):
                    # Same File with media only, do media vs extended.
                    frame1 = draw_mediapipe(pose1, image1, total_frames, media_noface)
                    frame1['video'] = 1
                    frame2 = draw_mediapipe_extended(pose2, image2, total_frames, False)
                    frame2['video'] = 2
                else:
                    # Different files with media only, do media vs media.           
                    frame1 = draw_mediapipe(pose1, image1, total_frames, media_noface)
                    frame2 = draw_mediapipe(pose2, image2, total_frames, media_noface)
                    frame2['video'] = 2

                image = cv2.hconcat([image1, image2])
            else:
                if( args['compare_file'] == args['filename'] ):
                    # Same File with extended only, Do normal vs extended.
                    frame1 = setup_normal_frame(total_frames,fps,1)
                    frame2 = draw_mediapipe_extended(pose2, image2, total_frames, args['display'])
                    frame2['video'] = 2
                else:
                    # Different File with extended only, Do extended vs extended.                    
                    frame1 = draw_mediapipe_extended(pose1, image1, total_frames, args['display'])
                    frame1['video'] = 1
                    frame2 = draw_mediapipe_extended(pose2, image2, total_frames, args['display'])
                    frame2['video'] = 2

                image = cv2.hconcat([image1, image2])

            if( frame1 ):
                frame_data.append(frame1)
            if( frame2 ):
                frame_data.append(frame2)

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
