import os
import cv2
import time
import logging
from enum import Enum

class VideoMode(Enum):
    CAMERA = 0
    VIDEO = 1

def flip_image(image, should_flip):
    if(should_flip):
        image = cv2.flip(image, 1)
        should_flip = False        
    return image, should_flip

def add_extension(filename, extension=".csv"):
    basename, ext = os.path.splitext(filename)
    if ext == extension:
        return filename
    else:
        return filename + extension

def get_file_path(output_file, location="../records/"):
    # This section manages the data collection.
    absolute_path = os.path.abspath(location)
    create_directory(absolute_path)
    full_path = os.path.join(absolute_path, output_file)
    return full_path

def create_directory(directory_path):
    """
    Creates a directory at the given path if it doesn't already exist.

    Parameters:
        directory_path (str): The path to the directory to create.

    Returns:
        None
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def setup_video_capture(filename="", fps_rate=30):
    # Check if the user chose a video file
    # Ask the user to input the video file name
    mode = VideoMode.VIDEO
    if( not filename ):
        filename = input("Enter the video file name (or enter to use camera): ").strip()

    if(not filename):
        # Open the video mode
        # Find Camera to find the right camera.
        # This is a hack to find the right camera when multiple cameras are connected.
        filename = 2
        #find_camera()
        mode = VideoMode.CAMERA

    cap = cv2.VideoCapture(filename)
    if(not cap.isOpened()):
        raise ("FAILED TO LOAD VIDEO filename= '", filename,"'")
    else:
        max_fps = cap.get(cv2.CAP_PROP_FPS)
        logging.info(f"MAX FPS= {max_fps}")
        
        if(fps_rate == 0):
            fps_rate = max_fps
        else:
            cap.set(cv2.CAP_PROP_FPS, fps_rate)

    # Get the input video size and frame rate
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    logging.info(f"Width = {width}")
    logging.info(f"Height= {height}")

    return cap, mode, fps_rate, (width, height)

# calculate the frames per second of the running video stream.
def calculate_fps():
    global fps, fps_count, start_time
    fps_count += 1
    if (time.time() - start_time) > 1:
        fps = fps_count
        fps_count = 0
        start_time = time.time()
    return fps

# Display the FPS on the screen.
def display_fps(image, fps):
    cv2.putText(image, "FPS: {:.2f}".format(
        fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# Find the camera index.
def find_camera():
    cams_test = 100
    for i in range(0, cams_test):
        cap = cv2.VideoCapture(i)
        test, frame = cap.read()
        if test:
            logging.debug(f"i : {str(i)} /// result: {str(test)}")
            pass
