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

import logging

# Debugging Levels
# DEBUG: Detailed information, typically of interest only when diagnosing problems.
# INFO: Confirmation that things are working as expected.
# WARNING: An indication that something unexpected happened or indicative of some problem in the near future(e.g. ‘disk space low’). The software is still working as expected.
# ERROR: Due to a more serious problem, the software has not been able to perform some function.
# CRITICAL: A very serious error, indicating that the program itself may be unable to continue running.

def set_log_level(level):
    """Set the logging level based on the specified string"""
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level}")
    logging.basicConfig(level=numeric_level,
                        format='%(asctime)s - %(levelname)s - %(message)s')

# ******************************************* Arguments Sections
def setup_arguments():

    # Initialize the argument parser
    ap = argparse.ArgumentParser()
    
    ##################### Debugging arguments.
    # Add the debug mode for more verbose output in terminal.
    ap.add_argument("-d", "--debug", type=bool, default=False, help="Debug mode for more verbose output.")

    # Add time to the output file argument
    ap.add_argument("-t", "--timestamp", type=bool, default=False, help="Output append time to file name")

    # Add time to the output file argument
    ap.add_argument("-p", "--mirror", type=bool, default=False, help="Flip the image to mirror your perspective.")

    # Add the preferred fps rate
    ap.add_argument("-z","--rate", type=float, default=0, help="Frame rate of the video")

    # Add an option to record the video
    ap.add_argument("-r","--record", type=bool, default=False, help="Record the video")

    # Add an option to load a video file instead of a camera.
    ap.add_argument("-f","--filename", type=str, default="", help="Load a video file instead of a camera.")

    # Add an option to run Mediapipe without additional processing.
    ap.add_argument("-m","--media", type=bool, default=False, help="Run Mediapipe without additional processing.")

    # Add an option to run Mediapipe without additional processing.
    ap.add_argument("-n","--media_noface", type=bool, default=False, help="Run Mediapipe without additional processing.")

    ##################### Output arguments.
    
    # Add the output file argument
    ap.add_argument("-o", "--output", type=str,
                    default="saved_frame_data", help="Output file name")
    
    # Add time to the output file argument
    ap.add_argument("-t", "--timestamp", type=bool, default=False,
                    help="Output append time to file name")
    
    # Add an option to record the video
    ap.add_argument("-r", "--record", type=str, default="",
                    help="Record the video only")

    # Add an option to record the video with mediapipe content.
    ap.add_argument("-rp", "--record_media", type=str, default="",
                    help="Record the video only  with mediapipe content.")

    # Add an option to load a video file instead of a camera.
    ap.add_argument("-f", "--filename", type=str, default="",
                    help="Load a video file instead of a camera.")

    ##################### Format Arguments.
    
    # Add the interval argument
    ap.add_argument("-i", "--interval", type=int, default=10, help="Save Frame at interval of x frames.")

    # Add time to the output file argument
    ap.add_argument("-m", "--mirror", type=bool, default=False, help="Flip the image to mirror your perspective.")

    # Add the preferred fps rate
    ap.add_argument("-z","--rate", type=float, default=0, help="Frame rate of the video")

    return ap
# ******************************************* End Arguments Sections

def main():
    global fps, fps_count, fps_rate, start_time, dataframe, file_time

    ap = setup_arguments()
    # Parse the arguments
    args = vars(ap.parse_args())

    # Variables
    fps_rate = 0
    cap = None
    mode = None
    frame_size = None
    # For webcam input:
    # Start of the main program or loop
    try:
        if(args['debug'] == True):            
            set_log_level("DEBUG")
        else:
            set_log_level("INFO")

        logging.info("Starting to write information.")
        fps_rate = args['rate']
        filename = ""
        filename = args['filename']
        #filename = "../videos/S02-0302-F-move kettle.MP4"
        #filename = "../videos/S02-0302-SL-move kettle-2.MP4"
        #filename = "../videos/S02-0302-O-move kettle.MP4"

        cap, mode, fps_rate, frame_size = setup_video_capture(filename=filename,fps_rate=fps_rate)
        
        logging.info(f"Mode = {mode}")
        logging.info(f"Accepted FPS= {fps_rate}")
        logging.info(f"Frame Size= {frame_size}")
    except Exception as e:
        logging.error(f"Failed to read video or camera options. {e}")
        return 1


    if(frame_size == None):
        logging.error(f"Failed to identify a camera setting. {e}")

    # Run Mediapipe Main
    mediapose_main(args, cap, mode, frame_size, fps_rate)

    # Clean up the resources for the camera and windows.
    cap.release()
    cv2.destroyAllWindows()
    logging.info("Finished writing information. (End of Program)")   
   

if __name__ == '__main__':
    main()
