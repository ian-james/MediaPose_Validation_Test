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
# ******************************************* Arguments Sections
def setup_arguments():

    # Initialize the argument parser
    ap = argparse.ArgumentParser()

    # Add the interval argument
    ap.add_argument("-i", "--interval", type=int, default=10, help="Interval between frame captures (in milliseconds)")

    # Add the output file argument
    ap.add_argument("-o", "--output", type=str, default="frame_data.xlsx", help="Output file name")

    # Add the debug mode for more verbose output in terminal.
    ap.add_argument("-d", "--debug", type=bool, default=True, help="Debug mode for more verbose output.")

    # Add time to the output file argument
    ap.add_argument("-t", "--timestamp", type=bool, default=False, help="Output append time to file name")

    # Add time to the output file argument
    ap.add_argument("-m", "--mirror", type=bool, default=False, help="Flip the image to mirror your perspective.")

    ap.add_argument("-r","--rate", type=float, default=0, help="Frame rate of the video")

    return ap

# ******************************************* End Arguments Sections

def main():
    global fps, fps_count, fps_rate, start_time, debug_mode, dataframe, file_time
    
    ap = setup_arguments()
    # Parse the arguments
    args = vars(ap.parse_args())
    
    # Variables    
    fps_rate = 0
    cap = None
    mode = None
    
    debug_mode = args['debug']
    
    ## Start of the main program or loop
    # For webcam input:
    try:
        fps_rate = args['rate']
        cap, mode, fps_rate = setup_video_capture(fps_rate=fps_rate)
        #filename = "")
        debug_print("Mode = ", mode)
        debug_print("Accepted FPS=", fps_rate)        
    except Exception as e:
        debug_print("Failed to read video or camera options.", e)
        exit(1)

    # Run Mediapipe Main
    mediapose_main(args,cap,mode)    

    # Clean up the resources for the camera and windows.
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
