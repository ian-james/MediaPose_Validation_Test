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
    
    ##################### Debugging arguments.
    ap.add_argument("-l", "--log", type=str, default="info", help="Set the logging level. (debug, info, warning, error, critical)")
    
    # Add an option to load a video file instead of a camera.
    #../videos/tests/quick_flexion_test.mp4
    ap.add_argument("-f", "--filename", type=str, default="../videos/tests/quick_flexion_test.mp4",
                    help="Load a video file instead of a camera.")
    
    # Compare two capture either videos or camera..
    ap.add_argument("-c", "--compare", action="store_true",
                    help="Compare two video mode")

    ap.add_argument("-cf", "--compare_file", type=str, default="../videos/quick_flexion_side_test.mp4",
                    help="Setup comparison mode where we compare two videos.")

    # Add the debug mode for more verbose output in terminal.
    # Add an option to run Mediapipe without additional processing.
    ap.add_argument("-m", "--media", action="store_true",
                    help="Run Mediapipe without additional processing.")

    # Add an option to run Mediapipe without additional processing.
    ap.add_argument("-n", "--media_noface", action="store_true",
                    help="Run Mediapipe without additional processing and no face.")
    
    ap.add_argument("-nd","--no_display", action="store_true", help="Run Mediapipe without dislaying the HUD/Overlay calculations.")
    
    # Add an option to run check flag for debugging.
    ap.add_argument('-fps', '--check_fps', action="store_true", help='Check FPS option.')
    
    # Add an option to set the minimum detection confidence
    ap.add_argument('-md', '--min_detection_confidence', type=float, default=0.8, help="Minimum detection confidence.")
                    
    # Add an option to set the minimum tracking confidence
    ap.add_argument('-mt', '--min_tracking_confidence', type=float,
                    default=0.8, help="Minimum tracking confidence.")
    
    ##################### Output arguments.    
    # Add the output file argument
    ap.add_argument("-o", "--output", type=str,
                    default="saved_frame_data", help="Output file name")
    
    # Add time to the output file argument
    ap.add_argument("-t", "--timestamp", action="store_true",
                    help="Output append time to file name")
       
    # Add an option to record the video
    ap.add_argument("-r", "--record", type=str, default="record_video.mp4",
                    help="Record the video only")

    # Add an option to record the video with mediapipe content.
    ap.add_argument("-rp", "--record_media", type=str, default="record_full.mp4",
                    help="Record the video only with mediapipe content.")
  
    ##################### Format Arguments.    
    # Add the interval argument
    ap.add_argument("-i", "--interval", type=int, default=10, help="Save Frame at interval of x frames.")
    
    # Add time to the output file argument
    ap.add_argument("-p", "--mirror", action="store_true", help="Flip the image to mirror your perspective.")

    # Add the preferred fps rate
    ap.add_argument("-z","--rate", type=float, default=0, help="Frame rate of the video")

    return ap
# ******************************************* End Arguments Sections

def main():
    global fps, fps_count, fps_rate, start_time, dataframe, file_time

    ap = setup_arguments()
    # Parse the arguments
    args = vars(ap.parse_args())
    
    print(args)

    main_cap = VideoCap_Info(None, 0, 0, 0, None)
    second_cap = VideoCap_Info(None, 0, 0, 0, None)
        
    # For webcam input:
    # Start of the main program or loop
    try:        
        set_log_level(args['log'])
        logging.info("Starting to write information.")
        fps_rate = args['rate']
        filename = ""
        filename = args['filename']   
        print(filename)     
        #filename = "../videos/S02-0302-SL-move kettle-2.MP4"
        #filename = "../videos/S02-0302-O-move kettle.MP4"
        #filename = "../videos/quick_flexion_side_test.mp4"            
        cap, mode, fps_rate, frame_size = setup_video_capture(filename=filename,fps_rate=fps_rate)        
        main_cap = VideoCap_Info(cap, fps_rate, frame_size[0], frame_size[1], mode)
        
        logging.info(f"Mode One = {mode}")        
        logging.info(f"Accepted FPS= {fps_rate}")
        
        if( args['compare'] ):
            scap,smode, sfps_rate, sframe_size = setup_video_capture(
                    filename=args['compare_file'], fps_rate=fps_rate)
            second_cap = VideoCap_Info(scap, sfps_rate, sframe_size[0], sframe_size[1], smode)                 
                
            if(main_cap.fps_rate != second_cap.fps_rate):
                logging.warning(f"FPS rates are different. Main FPS: {main_cap.fps_rate} Second FPS: {second_cap.fps_rate}")
            
            logging.info(f"Mode Two = {smode}")        
            logging.info(f"Accepted Two FPS= {sfps_rate}")
        
    except Exception as e:
        logging.error(f"Failed to read video or camera options. {e}")
        return 1

    if(frame_size == None):
        logging.error(f"Failed to identify a camera setting. {e}")

    # Run Mediapipe Main
    if(second_cap.cap == None):
        mediapose_main(args, cap, mode, frame_size, fps_rate)
    else:
        comparative_main(args, main_cap, second_cap)

    # Clean up the resources for the camera and windows.
    cap.release()
    cv2.destroyAllWindows()
    logging.info("Finished writing information. (End of Program)")   
   

if __name__ == '__main__':
    main()
