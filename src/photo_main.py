# Main Reference Starts at https://google.github.io/mediapipe/solutions/pose.html
# Author: Jamey Fraser
# Date: Jan 19th, 2023

# OpenCV Libary
import cv2
import math
import pandas as pd
import argparse
import time
import json
from enum import Enum
from collections import OrderedDict
from datetime import datetime, timezone

from utils import *
from mediapipe_main import *
from camera_utils import *
from log import *

from comparative_main import comparative_main

# ******************************************* Arguments Sections
def setup_arguments():

    # Initialize the argument parser
    ap = argparse.ArgumentParser()

    # Debugging arguments.
    ap.add_argument("-l", "--log", type=str, default="info",
                    help="Set the logging level. (debug, info, warning, error, critical)")

    # Add an option to load a video file instead of a camera.
    # ../videos/tests/quick_flexion_test.mp4
    ap.add_argument("-f", "--filename", type=str, default="/home/james/Projects/mediapipe_demo/MediaPose_Validation_Test/videos/images/left_arm_above_head.png",
                    help="Load a photo file.")

    # Add the debug mode for more verbose output in terminal.
    # Add an option to run Mediapipe without additional processing.
    ap.add_argument("-m", "--media", action="store_true",
                    help="Run Mediapipe without additional processing.")

    # Add an option to run Mediapipe without additional processing.
    ap.add_argument("-n", "--media_noface", action="store_true",
                    help="Run Mediapipe without additional processing and no face.")

    # Add an option to set the minimum detection confidence
    ap.add_argument('-md', '--min_detection_confidence', type=float,
                    default=0.8, help="Minimum detection confidence.")

    # Add an option to set the minimum tracking confidence
    ap.add_argument('-mt', '--min_tracking_confidence', type=float,
                    default=0.8, help="Minimum tracking confidence.")

    # Output arguments.
    # Add the output file argument
    ap.add_argument("-o", "--output", type=str,
                    default="image_saved_frame_data", help="Output file name")

    # Add time to the output file argument
    ap.add_argument("-t", "--timestamp", action="store_true",
                    help="Output append time to file name")

    return ap
# ******************************************* End Arguments Sections


def display_images_side_by_side(image1, image2, img1Lbl = "Image 1", img2Lbl = "Image 2"):
    # Create two separate windows

    cv2.namedWindow(img1Lbl, cv2.WINDOW_NORMAL)
    cv2.namedWindow(img2Lbl, cv2.WINDOW_NORMAL)

    # Resize the windows to fit side-by-side
    size = image1.shape[0]
    x = 200
    y = 200
    cv2.resizeWindow(img1Lbl, size, size)
    cv2.resizeWindow(img2Lbl, size, size)

    # Move the windows next to each other
    # Based on the size of the window move them side by side
    cv2.moveWindow(img1Lbl, x, y)
    cv2.moveWindow(img2Lbl, x + size, y)

    # Display the images in separate windows
    cv2.imshow(img1Lbl, image1)
    cv2.imshow(img2Lbl, image2)

    # Wait for a key press to exit
    cv2.waitKey(0)

    # Destroy the windows
    cv2.destroyAllWindows()

def run_photo_analysis(image, media_only, media_noface, mdc, mtc):
    if(image is None):
        return None, None, None
    df = None
    original_image = image.copy()

    with mp_pose.Pose(min_detection_confidence=mdc, min_tracking_confidence=mtc) as pose:        
        if (media_only):            
            frame = draw_mediapipe(pose, image, 0, media_noface)
        else:
            # Do our version of the pose estimation.            
            frame = draw_mediapipe_extended(pose, image, 0, False)
            # Press 'q' to exit
        df = add_dataframe(df, frame)

    return original_image, image, df


def run_camera_analysis(image, media_only, media_noface, mdc, mtc):    
    df = None    
    if (image is None):
        return None, None
    
    with mp_pose.Pose(min_detection_confidence=mdc, min_tracking_confidence=mtc) as pose:
        if (media_only):
            frame = draw_mediapipe(pose, image, 0, media_noface)
        else:
            # Do our version of the pose estimation.            
            frame = draw_mediapipe_extended(pose, image, 0, False)

    return image, df

def main():
    global fps, fps_count, fps_rate, start_time, dataframe, file_time

    ap = setup_arguments()
    # Parse the arguments
    args = vars(ap.parse_args())

    print(args)
    try:
        set_log_level(args['log'])
        logging.info("Starting to write information.")

        filename = args['filename']
        print(filename)

        # Media pipe options.
        media_only = args['media']
        media_noface = args['media_noface']
        mdc = args['min_detection_confidence']
        mtc = args['min_tracking_confidence']
        
        df = None
        idf = None

        # Output options.
        output_full_file, path_to_file = setup_fullpath_to_timestamp_output(args["output"], args['timestamp'])

        image = open_image(filename)
        if(image is not None):
            original_image, image, df = run_photo_analysis(image, media_only, media_noface, mdc, mtc)

            display_images_side_by_side(original_image, image, "Original Image", "Processed Image")

            save_to_csv(df, output_full_file)
            idf = get_key_frames(df)
            save_to_csv(idf, add_extension(path_to_file + "_keycols"))

            while (cv2.waitKey(1) & 0xFF != ord('q')):
                continue
        else:
            raise("Failed to open image.")

    except Exception as e:
        logging.error(f"Failed to read image options. {e}")
        return 1

    # Clean up the resources for the camera and windows.
    cv2.destroyAllWindows()
    logging.info("Finished writing information. (End of Program)")

if __name__ == '__main__':
    main()
