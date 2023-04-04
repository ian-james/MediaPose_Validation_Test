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

# Demo Comments
# Calibrate in neutral position, where is the axis for their initial position.
# Consideration for the starting points between normal Range-of-Motion and patients.
# Further investigate depth as Z-Axis is calculated via ML. How accurate is it?
# Validations  - Gold standard against ours ( DartFish or OptiTrack etc)
# Standard starting position for exercises.
# Goals rely on evaluating tele-health types solutions based on quick assessment (guess-estimate)
# However, this has potential as low entry points for cost, setup, and now requires validation for accuracy.
# End Comments

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

    # Add the interval argument
    ap.add_argument("-i", "--interval", type=int, default=10, help="Interval between frame captures (in milliseconds)")

    # Add the output file argument
    ap.add_argument("-o", "--output", type=str, default="saved_frame_data", help="Output file name")

    # Add the debug mode for more verbose output in terminal.
    ap.add_argument("-d", "--debug", type=bool, default=False, help="Debug mode for more verbose output.")

    # Add time to the output file argument
    ap.add_argument("-t", "--timestamp", type=bool, default=False, help="Output append time to file name")

    # Add time to the output file argument
    ap.add_argument("-m", "--mirror", type=bool, default=False, help="Flip the image to mirror your perspective.")

    ap.add_argument("-r","--rate", type=float, default=0, help="Frame rate of the video")

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

    if(args['debug'] == True):
        set_log_level("DEBUG")
    else:
        set_log_level("INFO")

    logging.info("Starting to write information.")


    ## Start of the main program or loop
    # For webcam input:
    try:
        fps_rate = args['rate']
        filename = "" #"../videos/S02-0302-F-move kettle.MP4"
        cap, mode, fps_rate = setup_video_capture(filename=filename,fps_rate=fps_rate)
        #filename = "")
        logging.info(f"Mode = {mode}")
        logging.info(f"Accepted FPS= {fps_rate}")
    except Exception as e:
        logging.error(f"Failed to read video or camera options. {e}")
        exit(1)

    # Run Mediapipe Main
    mediapose_main(args,cap,mode)

    # Clean up the resources for the camera and windows.
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()